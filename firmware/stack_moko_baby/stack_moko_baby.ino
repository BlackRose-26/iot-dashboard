// Stack Moko Baby: outbound protocol-v2 client, 3 x 16x16 WS2812 panels.
// Physical button gameplay only. No inbound /start or raw-score upload API.
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <esp_timer.h>
#include <time.h>
#include "game_engine.h"
#include "transport_job.hpp"
#if __has_include("config.h")
#include "config.h"
#else
#include "config.example.h"
#endif
// Built with -DSTACK_HARDWARE_TEST=1 by scripts/flash-device.py --selftest.
// That build never opens the NVS journal, Wi-Fi or the backend.
#ifndef STACK_HARDWARE_TEST
#define STACK_HARDWARE_TEST 0
#endif

const char* RULES_HASH="f73ce2ee4d1f607b6ea97038a534c7521a9305ee9ada3e2d418029cf866a58a4";
constexpr int LED_PIN=18, BUTTON_PIN=27, STRIP_PIN=25, PIEZO_PIN=26;
Adafruit_NeoPixel leds(768,LED_PIN,NEO_GRB+NEO_KHZ800);
Preferences nvs;
JsonDocument saved;
StackGame game;
enum Mode { OFFLINE, WAITING, ARMED, COUNTDOWN, PLAYING, RESULT, HELD, FAULT };
Mode mode=OFFLINE;
uint64_t countdownAt=0, startAt=0, lastContact=0;
uint64_t finishedAt=0, volumeAt=0;
uint16_t pendingTrack=0;
bool volumeSet=false;
bool registered=false, startup=true, hadJournal=false, rotateBoot=false;
portMUX_TYPE inputLock=portMUX_INITIALIZER_UNLOCKED;
volatile uint64_t buttonEdge=0;
volatile uint32_t buttonEdges=0; // Raw falling edges, including bounce; diagnostics only.
void IRAM_ATTR buttonISR() {
  portENTER_CRITICAL_ISR(&inputLock);
  if (!buttonEdge) buttonEdge=esp_timer_get_time()/1000ULL;
  buttonEdges++;
  portEXIT_CRITICAL_ISR(&inputLock);
}
uint64_t lastHeartbeat=0, lastPoll=0, nextRequest=0;
uint32_t backoff=1000;

uint64_t uptime() { return esp_timer_get_time()/1000ULL; }
String uuid() {
  uint8_t b[16]; esp_fill_random(b,16); b[6]=(b[6]&15)|64; b[8]=(b[8]&63)|128;
  char out[37]; snprintf(out,sizeof(out),"%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x",
    b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13],b[14],b[15]);
  return String(out);
}
bool persist() {
  String value; serializeJson(saved,value);
  if (value.length()>10000 || nvs.putString("journal",value)!=value.length()) {
    mode=FAULT; Serial.println("Storage failed; cabinet held. Preserve journal."); return false;
  }
  return true;
}
void newBoot() {
  String previous=saved["registration"]["bootId"]|"";
  saved["registration"].clear();
  saved["registration"]["bootId"]=uuid();
  if (previous.length()) saved["registration"]["previousBootId"]=previous;
  else saved["registration"]["previousBootId"]=nullptr;
  saved["registration"]["storageId"]=saved["storageId"].as<String>();
  saved["registration"]["uptimeMs"]=uptime();
  saved["sequence"]=0;
  registered=false;
  persist();
}

// Explicit local-HTTP exception: Wokwi private gateway, loopback and the
// RFC 1918 ranges used by Android (192.168/10) and iPhone (172.20.10) hotspots.
bool privateHttp(const String& base) {
  if (base.startsWith("http://host.wokwi.internal:") || base.startsWith("http://192.168.") ||
      base.startsWith("http://10.") || base.startsWith("http://127.0.0.1:")) return true;
  if (!base.startsWith("http://172.")) return false;
  int second=base.substring(11).toInt();
  return second>=16 && second<=31;
}
// Plain-language hotspot diagnostics; never prints the password or token.
void wifiEvent(WiFiEvent_t event, WiFiEventInfo_t info) {
  static uint8_t lastReason=0;
  static uint64_t lastReport=0;
  if (event==ARDUINO_EVENT_WIFI_STA_GOT_IP) {
    lastReason=0;
    Serial.printf("Wi-Fi connected to \"%s\": IP %s, signal %d dBm, channel %d.\n",STACK_WIFI_SSID,
                  WiFi.localIP().toString().c_str(),WiFi.RSSI(),WiFi.channel());
  } else if (event==ARDUINO_EVENT_WIFI_STA_DISCONNECTED) {
    uint8_t reason=info.wifi_sta_disconnected.reason;
    uint64_t t=esp_timer_get_time()/1000ULL;
    if (reason==lastReason && t-lastReport<15000) return; // Retries repeat quickly.
    lastReason=reason; lastReport=t;
    if (reason==WIFI_REASON_NO_AP_FOUND)
      Serial.printf("Wi-Fi: hotspot \"%s\" not found. Use 2.4 GHz (iPhone: Maximize Compatibility), keep it on and check the name.\n",STACK_WIFI_SSID);
    else if (reason==WIFI_REASON_AUTH_FAIL || reason==WIFI_REASON_AUTH_EXPIRE ||
             reason==WIFI_REASON_4WAY_HANDSHAKE_TIMEOUT || reason==WIFI_REASON_HANDSHAKE_TIMEOUT)
      Serial.println("Wi-Fi: hotspot rejected the password. Rebuild with the current hotspot password.");
    else Serial.printf("Wi-Fi disconnected (reason %u); retrying.\n",reason);
  }
}

QueueHandle_t requests, replies;
bool inFlight=false;
bool pollAfterHeartbeat=false;
// Only this worker does blocking DNS, TLS and HTTP. It never touches game/NVS.
void networkTask(void*) {
  WiFiClient plain;
  WiFiClientSecure secure;
  secure.setCACert(STACK_ROOT_CA);
  secure.setHandshakeTimeout(10);
  HTTPClient http;
  http.setConnectTimeout(3000); http.setTimeout(3000);
  http.setReuse(true);
  http.setFollowRedirects(HTTPC_DISABLE_FOLLOW_REDIRECTS);
  for (;;) {
    RequestJob* job=nullptr;
    if (xQueueReceive(requests,&job,portMAX_DELAY)!=pdTRUE) continue;
    String base=STACK_API_BASE;
    bool tls=base.startsWith("https://");
    bool localHttp=STACK_ALLOW_LOCAL_HTTP && privateHttp(base);
    if (WiFi.status()==WL_CONNECTED && (tls || localHttp) &&
        (!tls || (strlen(STACK_ROOT_CA)>0 && time(nullptr)>1735689600))) {
      if (http.begin(tls ? static_cast<WiFiClient&>(secure) : static_cast<WiFiClient&>(plain),base+job->path)) {
        http.addHeader("X-Device-Token",STACK_DEVICE_TOKEN);
        http.addHeader("X-Device-Boot-Id",job->boot);
        http.addHeader("Content-Type","application/json");
        job->status=job->body.length()?http.POST(job->body):http.GET();
        if (job->status>0 && http.getSize()<=16384) job->response=http.getString();
        if (job->status<0) {
          char detail[96]={0};
          int tlsError=tls?secure.lastError(detail,sizeof(detail)):0;
          Serial.printf("Network request failed: HTTP transport %d, TLS %d.\n",job->status,tlsError);
        }
        http.end();
      }
    } else if (tls && time(nullptr)<=1735689600) {
      Serial.println("Waiting for network time before verified HTTPS.");
    }
    xQueueSend(replies,&job,portMAX_DELAY);
    vTaskDelay(1);
  }
}
void request(const char* kind, const char* path, JsonVariantConst payload=JsonVariantConst()) {
  auto* job=new RequestJob;
  job->kind=kind; job->path=path;
  job->boot=saved["registration"]["bootId"].as<String>();
  if (!payload.isNull()) serializeJson(payload,job->body);
  if (xQueueSend(requests,&job,0)!=pdTRUE) { delete job; mode=FAULT; return; }
  inFlight=true;
}
void journal(const char* phase, JsonVariantConst command) {
  if (!saved["pending"].isNull()) { mode=FAULT; return; }
  auto packet=saved["pending"].to<JsonObject>();
  packet["eventId"]=uuid(); packet["sequence"]=saved["sequence"].as<uint64_t>()+1;
  packet["uptimeMs"]=uptime();
  packet["sessionId"]=command["sessionId"];
  packet["commandId"]=command["id"];
  packet["expectedRevision"]=command["expectedRevision"];
  packet["phase"]=phase;
  if (!strcmp(phase,"started") || !strcmp(phase,"terminal")) {
    packet["roundBootId"]=saved["round"]["roundBootId"];
    packet["startUptimeMs"]=saved["round"]["startUptimeMs"];
    if (!strcmp(phase,"terminal")) packet["terminal"]=saved["round"]["terminal"];
  }
  persist(); // Exact packet committed before request; retry without rebuilding.
}
void terminal() {
  if (!saved["round"]["terminal"].isNull() || mode==FAULT) return;
  auto result=saved["round"]["terminal"].to<JsonObject>();
  result["terminalId"]=uuid(); result["rulesHash"]=RULES_HASH;
  result["outcome"]=game.won?"win":"loss"; result["durationMs"]=game.duration;
  auto trace=result["placements"].to<JsonArray>();
  for (int i=0;i<game.count;i++) {
    auto p=trace.add<JsonObject>();
    p["candidate_x"]=game.trace[i].x; p["candidate_width"]=game.trace[i].width;
    p["overlap_width"]=game.trace[i].overlap; p["locked_at_ms"]=game.trace[i].locked;
  }
  mode=RESULT; finishedAt=uptime(); digitalWrite(STRIP_PIN,LOW);
  persist(); // Retain full trace before upload, even when WiFi is unavailable.
  audioTrack(game.won?3:2);
#if STACK_USE_PIEZO
  tone(PIEZO_PIN,game.won?1400:220,300);
#endif
}
void audioCommand(uint8_t command, uint16_t argument) {
#if STACK_USE_DFPLAYER
  uint8_t bytes[10]={0x7e,0xff,0x06,command,0x00,uint8_t(argument>>8),uint8_t(argument),0,0,0xef};
  uint16_t sum=0; for (int i=1;i<=6;i++) sum+=bytes[i];
  uint16_t check=0-sum; bytes[7]=check>>8; bytes[8]=check&255;
  Serial2.write(bytes,10);
#endif
}
void audioTrack(uint16_t track) { pendingTrack=track; }
void updateAudio() {
#if STACK_USE_DFPLAYER
  if (!volumeSet && uptime()>=2000) {
    audioCommand(0x06,min(30,STACK_DFPLAYER_VOLUME)); volumeSet=true; volumeAt=uptime();
  } else if (volumeSet && pendingTrack && uptime()-volumeAt>=150) {
    audioCommand(0x12,pendingTrack); pendingTrack=0;
  }
#endif
}
void command(JsonVariantConst cmd) {
  String type=cmd["type"]|"";
  String session=cmd["sessionId"]|"";
  String current=saved["round"]["command"]["sessionId"]|"";
  if (type=="reserve") {
    if (current==session) return; // Never restart completed, interrupted or fenced sessions.
    if (!current.isEmpty() && !saved["round"]["completed"].as<bool>() && !saved["round"]["fenced"].as<bool>()) return;
    if (String(cmd["rulesHash"]|"")!=RULES_HASH || String(cmd["rules"]["code"]|"")!="matrix-v1") {
      mode=HELD; Serial.println("Rules mismatch; ask operator to review."); return;
    }
    // Durable high-water mark permanently blocks all earlier reserve commands,
    // including after a stop or after the latest round's details are replaced.
    uint64_t delivery=cmd["deliverySequence"]|uint64_t(0);
    if (!delivery || delivery<=saved["lastDelivery"].as<uint64_t>()) return;
    saved["lastDelivery"]=delivery;
    saved["round"].clear(); saved["round"]["command"]=cmd;
    saved["round"]["accepted"]=false;
    if (persist()) journal("reserved",cmd);
  } else if (type=="fence") {
    if (String(cmd["bootId"]|"")!=saved["registration"]["bootId"].as<String>()) return;
    if (current==session && !saved["round"]["terminal"].isNull()) return;
    bool unstarted=current==session && saved["round"]["accepted"].as<bool>() && saved["round"]["startUptimeMs"].isNull();
    mode=HELD; digitalWrite(STRIP_PIN,LOW);
    uint64_t delivery=cmd["deliverySequence"]|uint64_t(0);
    if (!delivery) { mode=FAULT; return; }
    saved["lastDelivery"]=max(saved["lastDelivery"].as<uint64_t>(),delivery);
    saved["round"]["fenced"]=true;
    if (persist()) journal(unstarted?"fenced_unstarted":"fenced_interrupted",cmd);
  }
}
void handleReply(RequestJob* job) {
  inFlight=false;
  JsonDocument data;
  bool ok=job->status==200 && !deserializeJson(data,job->response) && data["ok"].as<bool>();
  if (job->status==200 && (job->kind=="heartbeat" || job->kind=="commands" || job->kind=="enrollment")) ok=!deserializeJson(data,job->response);
  if (!ok) {
    String code=data["code"]|"";
    if (job->kind=="journal" && (code=="start_held" || code=="reservation_expired")) {
      saved["rejected"]=saved["pending"]; saved.remove("pending");
      mode=HELD; persist();
    } else if (job->status>=400 && job->status<500) {
      mode=HELD; Serial.printf("Device request held (%d). Check operator recovery.\n",job->status);
    } else if (job->status<=0) {
      Serial.println("Connection unavailable; check Wi-Fi, API origin, time sync and trusted CA.");
    }
    nextRequest=uptime()+backoff; backoff=min(backoff*2,uint32_t(10000));
    delete job; return;
  }
  lastContact=uptime(); backoff=1000; nextRequest=0;
  if (job->kind=="enrollment") {
    saved["registration"]["previousBootId"]=data["currentBootId"];
    saved["enrollmentChecked"]=true;
    persist();
  }
  if (job->kind=="boot") {
    registered=true;
    Serial.println("Cabinet boot registered with the backend.");
  }
  if (job->kind=="journal") {
    String phase=saved["pending"]["phase"]|"";
    saved["sequence"]=saved["pending"]["sequence"];
    if (phase=="reserved") { saved["round"]["accepted"]=true; if (!startup) mode=ARMED; }
    if (phase=="terminal") {
      saved["round"]["delivered"]=true;
      saved["round"]["completed"]=!data["reviewRequired"].as<bool>();
      mode=data["reviewRequired"].as<bool>()?HELD:RESULT;
    }
    saved.remove("pending"); persist();
  }
  if (job->kind=="commands") {
    if (data["reviewRequired"].as<bool>()) mode=HELD;
    for (JsonVariantConst cmd:data["commands"].as<JsonArrayConst>()) {
      if (saved["pending"].isNull()) command(cmd);
    }
    if (data["activeSessionId"].isNull() && mode!=PLAYING && mode!=COUNTDOWN &&
        (saved["round"].isNull() || saved["round"]["completed"].as<bool>() || saved["round"]["fenced"].as<bool>())) {
      if (mode!=WAITING) Serial.println("Cabinet ready; waiting for an assigned player.");
      mode=WAITING;
    }
  }
  delete job;
}
void synchronize() {
  RequestJob* reply=nullptr;
  if (xQueueReceive(replies,&reply,0)==pdTRUE) handleReply(reply);
  if (mode==FAULT || inFlight || uptime()<nextRequest || WiFi.status()!=WL_CONNECTED) return;
  if (!hadJournal && !saved["enrollmentChecked"].as<bool>()) { request("enrollment","/api/device/enrollment"); return; }
  if (!registered) { request("boot","/api/device/boot",saved["registration"]); return; }
  if (!saved["pending"].isNull()) { request("journal","/api/device/journal",saved["pending"]); return; }
  if (startup) {
    startup=false;
    if (hadJournal && !rotateBoot) {
      rotateBoot=true; newBoot();
      mode=saved["round"].isNull()?OFFLINE:HELD;
      return;
    }
  }
  if (!saved["round"]["terminal"].isNull() && !saved["round"]["delivered"].as<bool>() && !saved["round"]["fenced"].as<bool>()) {
    journal("terminal",saved["round"]["command"]); return;
  }
  bool heartbeatDue=uptime()-lastHeartbeat>=1000 || lastHeartbeat==0;
  bool pollDue=uptime()-lastPoll>=1000;
  // A slow simulator must not starve command polling with overdue heartbeats.
  // One simulated second also keeps real-wall-time freshness usable at low FPS.
  if (pollDue && (pollAfterHeartbeat || !heartbeatDue)) {
    request("commands","/api/device/commands"); lastPoll=uptime(); pollAfterHeartbeat=false; return;
  }
  if (heartbeatDue) {
    JsonDocument body;
    body["state"]=(mode==PLAYING||mode==COUNTDOWN)?"playing":(mode==WAITING||mode==ARMED||mode==RESULT)?"ready":"offline";
    body["firmware"]="matrix-v1-journal-0.1"; body["rssi"]=WiFi.RSSI();
    request("heartbeat","/api/device/heartbeat",body.as<JsonVariantConst>()); lastHeartbeat=uptime(); pollAfterHeartbeat=true; return;
  }
}

// Panel chain is bottom -> middle -> top. Each 16x16 panel is row-serpentine.
int pixel(int x,int y) {
  int panel=2-y/16, row=y%16;
  return panel*256+row*16+(row%2?15-x:x);
}
void block(int x,int y,int width,uint32_t color) {
  for (int dy=0;dy<2;dy++) for (int i=0;i<width;i++) leds.setPixelColor(pixel(x+i,y+dy),color);
}
const uint16_t digits[10]={0x7b6f,0x2492,0x73e7,0x73cf,0x5bc9,0x79cf,0x79ef,0x7249,0x7bef,0x7bcf};
void digit(int n,int left,int top,int scale,uint32_t color) {
  for (int row=0;row<5;row++) for (int col=0;col<3;col++)
    if (digits[n]&(1<<(14-row*3-col)))
      for (int dy=0;dy<scale;dy++) for (int dx=0;dx<scale;dx++)
        leds.setPixelColor(pixel(left+col*scale+dx,top+row*scale+dy),color);
}
void word(const char* text,int top,uint32_t color) {
  const char* alphabet="GAMEOVRT";
  const uint8_t glyphs[8][5]={{7,4,5,5,7},{2,5,7,5,5},{5,7,7,5,5},{7,4,6,4,7},
                             {7,5,5,5,7},{5,5,5,5,2},{6,5,6,5,5},{7,2,2,2,2}};
  for (int i=0;text[i];i++) {
    const char* found=strchr(alphabet,text[i]);
    if (!found) continue;
    for (int row=0;row<5;row++) for (int col=0;col<3;col++)
      if (glyphs[found-alphabet][row]&(1<<(2-col))) leds.setPixelColor(pixel(i*4+col,top+row),color);
  }
}
void draw() {
  leds.clear();
  uint32_t base=leds.Color(35,90,25), active=leds.Color(120,35,5);
  if (mode==PLAYING || mode==RESULT || mode==COUNTDOWN) {
    block(5,46,6,base);
    int sx=5;
    for (int i=0;i<game.count;i++) {
      int left=max(sx,game.trace[i].x); sx=left;
      if (game.trace[i].overlap) block(left,44-i*2,game.trace[i].overlap,base);
    }
    if (mode==PLAYING && !game.ended) block(game.x(uint32_t(uptime()-startAt)),44-game.score*2,game.width,active);
    if (mode==COUNTDOWN) {
      digit(3-min(2,int((uptime()-countdownAt)/STACK_COUNTDOWN_STEP_MS)),3,0,3,leds.Color(100,45,0));
    } else if (mode==RESULT && !game.won && ((uptime()-finishedAt)/1800)%2==0) {
      word("GAME",2,leds.Color(100,5,5)); word("OVER",9,leds.Color(100,5,5));
    } else {
      digit(game.score/10,1,0,2,base); digit(game.score%10,9,0,2,base);
      uint32_t elapsed=mode==PLAYING?uint32_t(uptime()-startAt):game.duration;
      int remaining=elapsed>=60000?0:(60000-elapsed+999)/1000;
      word("T",11,active); digit(remaining/10,5,11,1,active); digit(remaining%10,9,11,1,active);
    }
  } else {
    uint32_t c=mode==ARMED?leds.Color(20,90,20):mode==WAITING?leds.Color(10,15,45):leds.Color(90,8,5);
    for (int x=3;x<13;x++) leds.setPixelColor(pixel(x,24),c);
  }
  leds.show();
}

#if STACK_HARDWARE_TEST
// Wiring self-test. Short press: counted on every stage. Hold 1 s: next stage.
// Uses the game's brightness cap; no journal, Wi-Fi, token or backend traffic.
const char* const testNames[]={"panel chain","orientation","button","12 V strip","audio"};
constexpr int TEST_STAGES=5;
int testStage=0;
uint32_t testPresses=0;
uint64_t testStageAt=0, testFlashAt=0, testToggleAt=0;
bool testStrip=false;
uint16_t testTrack=0;
void testEnter(int stage) {
  testStage=stage%TEST_STAGES; testStageAt=uptime(); testToggleAt=0;
  testStrip=false; testTrack=0; digitalWrite(STRIP_PIN,LOW);
  Serial.printf("\n== Self-test %d/%d: %s ==\n",testStage+1,TEST_STAGES,testNames[testStage]);
  switch (testStage) {
    case 0: Serial.println("Expect: panel wired to GPIO18 red (bottom), next green (middle), last blue (top).\n"
                           "Wrong colour order = check the DOUT->DIN chain. Dark panel = check its 5 V, GND and data."); break;
    case 1: Serial.println("Expect: white border; red top-left, green top-right, blue bottom-left, yellow bottom-right.\n"
                           "An orange dot scans every row left->right, top->bottom. Jumps/zigzags = adjust pixel()."); break;
    case 2: Serial.println("Press the cabinet button. Count shows on the top panel; bottom row lights while held.\n"
                           "Many edges per press = bounce (the game debounces); always lit = GPIO27 stuck to GND."); break;
    case 3: Serial.println("GPIO25 toggles every second. The 12 V strip should follow the yellow block."); break;
    case 4:
#if STACK_USE_DFPLAYER
      Serial.println("DFPlayer plays /mp3/0001 (countdown), 0002 (loss), 0003 (win), 4 s apart, volume from config.");
#else
      Serial.println("DFPlayer is disabled in config.h (STACK_USE_DFPLAYER=0).");
#endif
      break;
  }
}
void testDraw() {
  leds.clear();
  uint64_t t=uptime(), since=t-testStageAt;
  if (testStage==0) {
    // Raw chain index, not pixel(): proves physical data-chain order.
    for (int i=0;i<768;i++) leds.setPixelColor(i,i<256?leds.Color(60,0,0):i<512?leds.Color(0,60,0):leds.Color(0,0,60));
  } else if (testStage==1) {
    uint32_t edge=leds.Color(30,30,30);
    for (int x=0;x<16;x++) { leds.setPixelColor(pixel(x,0),edge); leds.setPixelColor(pixel(x,47),edge); }
    for (int y=0;y<48;y++) { leds.setPixelColor(pixel(0,y),edge); leds.setPixelColor(pixel(15,y),edge); }
    leds.setPixelColor(pixel(0,0),leds.Color(90,0,0)); leds.setPixelColor(pixel(15,0),leds.Color(0,90,0));
    leds.setPixelColor(pixel(0,47),leds.Color(0,0,90)); leds.setPixelColor(pixel(15,47),leds.Color(90,90,0));
    int dot=int((since/8)%768);
    leds.setPixelColor(pixel(dot%16,dot/16),leds.Color(120,40,0));
  } else if (testStage==2) {
    uint32_t c=t-testFlashAt<120?leds.Color(120,120,120):leds.Color(35,90,25);
    digit((testPresses/10)%10,1,0,2,c); digit(testPresses%10,9,0,2,c);
    if (digitalRead(BUTTON_PIN)==LOW) for (int x=0;x<16;x++) leds.setPixelColor(pixel(x,47),leds.Color(0,60,90));
  } else if (testStage==3) {
    if (testStrip) block(3,22,10,leds.Color(110,90,0));
    else for (int x=3;x<13;x++) leds.setPixelColor(pixel(x,23),leds.Color(20,20,20));
  } else {
    digit(testTrack,5,16,2,leds.Color(100,45,0));
  }
  leds.show();
}
void selfTestSetup() {
  testEnter(0);
  Serial.println("Hardware self-test build: not connected, no journal or score. Reflash the game firmware afterwards.");
}
void selfTestLoop() {
  static bool down=false, advanced=false;
  static uint64_t downAt=0, highSince=0, lastPress=0, frame=0;
  uint64_t t=uptime();
  if (digitalRead(BUTTON_PIN)==LOW) {
    highSince=0;
    if (!down) {
      down=true; advanced=false; downAt=t; testFlashAt=t; testPresses++;
      portENTER_CRITICAL(&inputLock);
      uint32_t edges=buttonEdges; buttonEdges=0; buttonEdge=0;
      portEXIT_CRITICAL(&inputLock);
      Serial.printf("Button press #%lu (gap %lu ms, interrupt edges since last: %lu)\n",
                    (unsigned long)testPresses,lastPress?(unsigned long)(t-lastPress):0UL,(unsigned long)edges);
      lastPress=t;
    }
  } else {
    if (!highSince) highSince=t;
    if (down && t-highSince>=20) down=false; // 20 ms stable release, as in the game.
  }
  if (down && !advanced && t-downAt>=1000) { advanced=true; testEnter(testStage+1); }
  if (testStage==3 && t-testToggleAt>=1000) {
    testToggleAt=t; testStrip=!testStrip; digitalWrite(STRIP_PIN,testStrip?HIGH:LOW);
    Serial.printf("Strip %s\n",testStrip?"ON":"OFF");
  }
  if (testStage==4 && t>=2500 && (!testTrack || t-testToggleAt>=4000)) {
    testToggleAt=t; testTrack=testTrack%3+1;
#if STACK_USE_DFPLAYER
    audioTrack(testTrack);
    Serial.printf("Playing /mp3/000%u.mp3\n",testTrack);
#endif
#if STACK_USE_PIEZO
    tone(PIEZO_PIN,testTrack==3?1400:testTrack==2?220:880,300);
#endif
  }
  updateAudio();
  if (t-frame>=33) { frame=t; testDraw(); }
  delay(1);
}
#endif

void setup() {
  Serial.begin(115200); pinMode(BUTTON_PIN,INPUT_PULLUP); pinMode(STRIP_PIN,OUTPUT);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN),buttonISR,FALLING);
  leds.begin(); leds.setBrightness(25); leds.clear(); leds.show();
#if STACK_USE_DFPLAYER
  Serial2.begin(9600,SERIAL_8N1,-1,17); // TX only, via 1k resistor. Optional DFPlayer support.
#endif
#if STACK_HARDWARE_TEST
  selfTestSetup(); return;
#endif
  if (!nvs.begin("stack-v2",false)) { mode=FAULT; return; }
  String value=nvs.getString("journal",""); hadJournal=value.length()>0;
  if (hadJournal) {
    if (deserializeJson(saved,value) || saved["version"].as<int>()!=2 || !saved["registration"]["bootId"].is<String>() || !saved["storageId"].is<String>()) {
      mode=FAULT; Serial.println("Journal corrupt. Preserve flash; do not erase to release a round."); return;
    }
  } else {
    saved["version"]=2; saved["storageId"]=uuid(); saved["lastDelivery"]=0; newBoot();
  }
  if (mode==FAULT) return;
  if (strlen(STACK_DEVICE_TOKEN)<32 || strstr(STACK_DEVICE_TOKEN,"REPLACE_") || strstr(STACK_API_BASE,"YOUR-")) {
    mode=FAULT; Serial.println("Configure private config.h before connecting; no token was sent."); return;
  }
  requests=xQueueCreate(1,sizeof(RequestJob*)); replies=xQueueCreate(1,sizeof(RequestJob*));
  // TLS verification can be CPU-heavy in simulation. Priority zero shares
  // core 0 with its idle task so the watchdog remains fed and enabled.
  if (!requests||!replies||xTaskCreatePinnedToCore(networkTask,"stack-network",12288,nullptr,0,nullptr,0)!=pdPASS) { mode=FAULT; return; }
  WiFi.onEvent(wifiEvent);
  WiFi.mode(WIFI_STA); WiFi.begin(STACK_WIFI_SSID,STACK_WIFI_PASSWORD);
  configTime(0,0,"pool.ntp.org","time.google.com");
  Serial.println("Connecting. Blue = waiting, green = assigned; physical button starts only an assigned round.");
}
void loop() {
#if STACK_HARDWARE_TEST
  selfTestLoop(); return;
#endif
  if (mode==FAULT) { delay(100); return; }
  static bool clockReported=false;
  if (!clockReported && time(nullptr)>1735689600) {
    clockReported=true; Serial.println("Network time synchronized; verified HTTPS can start.");
  }
  synchronize();
  updateAudio();
  static bool wasDown=false, released=true;
  static uint64_t releaseAt=0, lastPress=0, frame=0, reconnectAt=0;
  uint64_t t=uptime();
  bool down=digitalRead(BUTTON_PIN)==LOW;
  portENTER_CRITICAL(&inputLock);
  uint64_t edge=buttonEdge; buttonEdge=0;
  portEXIT_CRITICAL(&inputLock);
  bool press=edge && released && edge-lastPress>=65;
  if (!down) {
    if (wasDown) releaseAt=t;
    if (t-releaseAt>=20) released=true;
  }
  if (mode==COUNTDOWN && t-countdownAt>=3*STACK_COUNTDOWN_STEP_MS) {
    saved["round"]["roundBootId"]=saved["registration"]["bootId"];
    saved["round"]["startUptimeMs"]=t;
    startAt=t;
    journal("started",saved["round"]["command"]);
    if (mode!=FAULT) { mode=PLAYING; digitalWrite(STRIP_PIN,HIGH); }
  }
  // Local timing starts after countdown and never waits for an HTTP receipt.
  if (mode==PLAYING && t>=startAt) {
    uint32_t elapsed=uint32_t(t-startAt);
    if (press && edge>=startAt) game.press(uint32_t(edge-startAt));
    if (!game.ended && elapsed>=60000) game.timeout();
    if (game.ended) terminal();
  }
  if (press) {
    released=false; lastPress=edge;
    if (mode==ARMED && saved["pending"].isNull() && t-lastContact<10000) {
      game=StackGame{};
      countdownAt=t;
      mode=COUNTDOWN;
      audioTrack(1);
    }
  }
  wasDown=down;
  if (t-frame>=50) { frame=t; draw(); }
  if (WiFi.status()!=WL_CONNECTED && t-reconnectAt>=15000) { reconnectAt=t; WiFi.reconnect(); }
  delay(1);
}
