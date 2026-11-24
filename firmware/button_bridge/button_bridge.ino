// Stack Moko Baby button bridge (Plan B, 25 November 2026).
// The LED matrices are not used: the game runs on the web game screen (/screen), and this
// ESP32 only reports the arcade button over USB. Chrome or Edge reads it with Web Serial.
// No Wi-Fi, token or config.h. Flash with: npm run device:bridge -- --port COMx
//
// Wiring is unchanged: button COM -> GND, NO -> GPIO27 (internal pull-up).
// Serial 115200 baud. Lines: "READY" at boot, then "PRESS <millis>" per press, where
// <millis> is the ESP32's time of the falling edge, so USB delay does not shift timing.
#include <Arduino.h>

const int BUTTON_PIN = 27;
const uint32_t MIN_PRESS_GAP_MS = 65;    // same debounce as the game firmware
const uint32_t STABLE_RELEASE_MS = 20;

portMUX_TYPE edgeLock = portMUX_INITIALIZER_UNLOCKED;
volatile uint32_t buttonEdge = 0;

void IRAM_ATTR buttonISR() {
  portENTER_CRITICAL_ISR(&edgeLock);
  if (!buttonEdge) buttonEdge = millis() | 1;  // never 0, so "no edge" stays distinct
  portEXIT_CRITICAL_ISR(&edgeLock);
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
  delay(50);
  Serial.println("READY");
}

void loop() {
  static bool released = true, wasDown = false;
  static uint32_t releaseAt = 0, lastPress = 0, readyAt = 0;
  uint32_t now = millis();
  bool down = digitalRead(BUTTON_PIN) == LOW;
  portENTER_CRITICAL(&edgeLock);
  uint32_t edge = buttonEdge;
  buttonEdge = 0;
  portEXIT_CRITICAL(&edgeLock);
  if (!down) {
    if (wasDown) releaseAt = now;
    if (now - releaseAt >= STABLE_RELEASE_MS) released = true;
  }
  if (edge && released && (lastPress == 0 || edge - lastPress >= MIN_PRESS_GAP_MS)) {
    released = false;
    lastPress = edge;
    Serial.print("PRESS ");
    Serial.println(edge);
  }
  // Repeat READY every 5 s so a page that opened the port late still sees the bridge.
  if (now - readyAt >= 5000) { readyAt = now; Serial.println("READY"); }
  wasDown = down;
  delay(1);
}
