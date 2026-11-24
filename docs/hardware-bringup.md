# Physical cabinet bring-up over a phone hotspot

Updated 23 November 2026. This guide follows the user's network choice: **phone hotspot → ESP32 → mobile data → Cloudflare HTTPS tunnel → this PC**. Players open registration on their own mobile data through the same public HTTPS address; only the ESP32 needs the hotspot. The PC needs Internet access but does not have to be on the hotspot. The hotspot phone can be Android or iPhone. Hardware (updated 23 November 2026): ESP32 DevKit **powered by the laptop USB**; an 8×32 WS2812 HUD followed by two 16×16 WS2812 block panels on one GPIO18 data line through a **330 Ω resistor (no level shifter)**; a 60 mm LED-lit arcade button (5–12 V, microswitch): switch **COM → GND, NO → GPIO27**, NC unused (internal pull-up, no resistor), and its light **+ → the 5 V display lead, − → GND**, always on (about 10–20 mA, possibly dimmer at 5 V). Keep the light tabs away from GPIO27: 5 V on an ESP32 pin can destroy it; a scrap speaker on GPIO26 through 220 Ω playing simple firmware beeps (no DFPlayer or sound files). The **laptop is the only power source**: USB port 1 powers the ESP32 and USB port 2 feeds the displays through a USB power lead (red 5 V, black GND), never through the ESP32 board. The firmware dims any frame whose estimated LED current exceeds `STACK_LED_BUDGET_MA` (default 400 mA, in `display_layout.h`). Do not use the team's 6 V regulator for the LEDs. The 12 V decoration strip is outside this guide.

**Status:** the tooling below compiles and its flash-layout check passes. **None of these steps has run on the physical cabinet yet.** Record each gate as passed only after it is actually observed.

## Tools added for the physical board

| Command | What it does |
| --- | --- |
| `npm run device:selftest` | Builds the **wiring self-test** and uploads it over USB. No Wi-Fi, token, NVS journal or backend traffic. |
| `npm run online:device` | Starts the dashboard and tunnel (like `online:firmware`), writes the hotspot `config.h`, builds the game firmware and uploads it over USB. |
| `npm run device:flash` | Re-uploads the game firmware with the existing private `config.h` (same tunnel address). |

Pass a port when more than one USB serial board is attached: `npm run device:selftest -- --port COM5`, or set `STACK_ESP32_PORT`.

`scripts/flash-device.py` writes only the bootloader (0x1000), partition table (0x8000), boot selector (0xE000) and application (0x10000). It parses the built partition table and **refuses any write overlapping the NVS partition** (0x9000–0xDFFF in the default layout), never runs `erase_flash`, and refuses a `config.h` that still targets `Wokwi-GUEST`. Never flash the Wokwi `.merged.bin` image onto the real cabinet: its padding overwrites NVS. A board previously flashed with a different partition scheme should be checked before relying on journal preservation.

## 1. Prepare the hotspot phone

- Use **2.4 GHz**. Android: hotspot band 2.4 GHz. iPhone: turn on **Maximize Compatibility**.
- Give the hotspot a **plain ASCII name** (letters, numbers, spaces). iPhone default names use a curly apostrophe; the helper refuses non-ASCII names.
- Use a WPA2 password of 8–63 plain characters.
- Android: turn off "turn off hotspot automatically" / idle timeout. iPhone: keep the Personal Hotspot screen open while the ESP32 first joins.
- Mobile data must be on. The cabinet sends about two small HTTPS requests per second; actual data use is **not measured yet**. Check the phone's data counter during the rehearsal.

### LED panel connectors (added 24 November 2026)

The panels in use (WS2812 "RGBIC" 8×32 and two 16×16) each have three wire groups on the back. "RGBIC" is a marketing name for individually addressable WS2812 LEDs; the firmware drives them unchanged.

| Connector | What it is | Connect it to |
|---|---|---|
| **DIN · 5V · GND** (3 wires) | Data input | 8×32 HUD: DIN ← 330 Ω ← GPIO18, GND → ESP32 GND, 5V **taped off** (never to the ESP32's 5V or VIN). Block panels: the previous panel's DOUT plug. |
| **5V · GND** (2 thicker wires) | Power input | The USB power lead (red → 5 V, black → GND), one pair per panel. |
| **DOUT · 5V · GND** (3 wires) | Data output | The next panel's DIN plug: HUD → bottom block → upper block. The upper block's DOUT stays unconnected and taped. |

Wire colours vary between batches; go by the printed labels or the arrow on the panel (data flows DIN → DOUT). With a multimeter, the GND wires of all three groups beep together, and so do the 5V wires; DIN and DOUT do not. Data fed into DOUT lights nothing but does no harm.

## 2. Wiring self-test (do this as soon as the wiring is finished)

Power the displays from a second laptop USB port through the USB power lead; prefer a USB-C port rated 1.5 A or more, because a USB-A port gives only about 0.5–0.9 A. Join the power lead GND to the ESP32 GND, but never connect the lead's 5 V to the ESP32 VIN/5V pin. The 768 LEDs also draw idle current (estimated 0.25–0.8 A, unmeasured) and the ESP32 about 0.1–0.4 A. If the ESP32 restarts, LEDs flicker or the laptop warns about USB power, lower `STACK_LED_BUDGET_MA`, use a USB-C port, or add a 5 V phone charger for the displays. The self-test uses the game's brightness cap (25/255); stage 1 lights all 768 pixels dimly. Check actual supply ratings before powering up.

1. Connect the ESP32 by a **data-capable** USB cable. Install the USB-serial driver (CP210x or CH340) if Windows shows no COM port. If upload reports a boot-mode error, hold the board's BOOT button while it starts connecting.
2. Run `npm run device:selftest`, then open the serial monitor command it prints (115200 baud).
3. **Short press** counts a press on every stage. **Hold 1 s** moves to the next stage. The serial monitor explains each stage.

| Stage | Expected | If wrong |
| --- | --- | --- |
| 1 Panel chain | 8×32 HUD (first on GPIO18) red, bottom block panel green, upper block panel blue. Uses raw chain order. | Colours out of order: check DOUT→DIN. Dark display: check its 5 V, GND and data. |
| 2 Orientation | On both the HUD and the block area: white border; red top-left, green top-right, blue bottom-left, yellow bottom-right; an orange dot scans each row left→right, top→bottom. | Mirrored corners, zigzag or jumps: change the flags in `display_layout.h` (HUD column/row order, zigzag, flips; block flips), not `stack_moko_baby.ino` (panel order, row direction, serpentine). |
| 3 Button | Count on the top panel; bottom row lights while held; serial prints gap and raw interrupt edges. | Bottom row always lit: GPIO27 stuck to GND (switch wired to NC instead of NO?). Many edges per press: mechanical bounce (the game debounces 20 ms / 65 ms). |
| 4 (skip) | GPIO25 decoration-strip output; HUD shows ON/OFF. Outside this guide. | Hold the button 1 s to continue. |
| 5 Sound | Speaker plays countdown beeps, loss tune, win tune, 4 s apart (HUD shows TRACK 1–3). | Check GPIO26 → 220 Ω → speaker → GND. Never connect the speaker to a power supply. |

If a layout flag changes, re-run the self-test until stage 2 is correct on both displays. The game and the backend replay use logical x positions only, so a mapping fix does not change scoring.

## 3. Flash the game firmware for the hotspot

Start MySQL in XAMPP. In a PowerShell terminal (the values stay in that terminal session only):

```powershell
$env:STACK_FIRMWARE_WIFI_SSID = "YOUR-HOTSPOT-NAME"
$env:STACK_FIRMWARE_WIFI_PASSWORD = "YOUR-HOTSPOT-PASSWORD"
npm run online:device
```

The launcher prints the administrator and player links, saves a root-certificate bundle (the live tunnel root plus the Google Trust Services, Let's Encrypt and SSL.com roots Cloudflare uses), writes private `config.h` and uploads the game firmware. Keep the terminal running. If firmware upload fails, the dashboard stays online; fix the cause and run the retry command it prints.

**Later restarts do not need a reflash (24 November 2026).** Each launcher start gets a new tunnel hostname. Plain `npm run online` sends it to the USB-connected cabinet as `STACK-URL https://<name>.trycloudflare.com`. The firmware stores it in its own NVS namespace (`stack-cfg`, separate from the game journal) and reconnects without rebooting. It accepts only HTTPS `*.trycloudflare.com` origins or the compiled address, refuses during a countdown or round (the helper retries), and a newly flashed build always starts from its compiled address. If the cabinet was unplugged or a serial monitor held the port, run `npm run device:url` later. Reflash with `npm run online:device` only for firmware or Wi-Fi changes, or if a future tunnel certificate chains to a root outside the bundle (the serial log then shows a TLS error). The registration QR still changes with the hostname: show it from the dashboard's Registration QR on a screen rather than printing it.

## 4. Connection gates (watch the serial monitor and the Machines page)

| Gate | Pass when | Status |
| --- | --- | --- |
| Wi-Fi | Serial: `Wi-Fi connected to "…": IP …, signal … dBm`. "Hotspot not found" means 2.4 GHz/name; "rejected the password" means rebuild with the right password. | Not run |
| Time | Serial: `Network time synchronized`. HTTPS cannot start before this. | Not run |
| Registration | Serial: `Cabinet boot registered with the backend.` | Not run |
| Heartbeat | Machines page shows a last heartbeat updating every few seconds, the RSSI and firmware `matrix-v1-journal-0.1`. Simulator controls are off in online mode. | Not run |
| Ready | Serial: `Cabinet ready; waiting for an assigned player.` Matrix centre bar is blue. | Not run |

A `Network request failed: HTTP transport …, TLS …` line means the address, tunnel or certificate needs attention; never disable certificate checks. If an earlier Wokwi simulation left a reserved or interrupted round, resolve it on the Machines page first: the fresh physical journal registers a new storage lineage and cannot claim an old round never started (see [device recovery](device-recovery.md)).

## 5. First real round

1. A test player scans the dashboard QR **on mobile data**, registers and sees the waiting ticket.
2. The administrator calls the next player. The cabinet bar turns **green**.
3. Press the physical button: 1.5 s countdown, then play. Unassigned presses never start a ranked game.
4. After win/loss, the result appears on the ticket, the leaderboard unlocks and the dashboard shows the round.

| Gate | Status |
| --- | --- |
| Assigned round plays, result validated and notified | Not run |
| Button latency and difficulty feel acceptable (numeric settings remain proposals) | Not run |
| Power-off during idle, then power-on: cabinet re-registers without operator action | Not run |
| Power-off mid-round: round held for operator review, no score awarded automatically | Not run |
| Hotspot drop and recovery during idle | Not run |
| Launcher restart: `npm run online` sends the new address over USB and a fresh heartbeat follows, with no reflash | Not run |
| Mobile-data use over a 30-minute rehearsal recorded | Not run |

Passing these gates is physical acceptance evidence; Wokwi runs and backend tests are not.
