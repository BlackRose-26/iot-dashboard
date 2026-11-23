# Physical cabinet bring-up over a phone hotspot

Updated 23 November 2026. This guide follows the user's network choice: **phone hotspot → ESP32 → mobile data → Cloudflare HTTPS tunnel → this PC**. Players open registration on their own mobile data through the same public HTTPS address; only the ESP32 needs the hotspot. The PC needs Internet access but does not have to be on the hotspot. The hotspot phone can be Android or iPhone. The hardware follows the [ESP32 wiring guide](esp32-online.md#firmware-files-and-wiring): ESP32 DevKit, three 16×16 WS2812 panels on GPIO18 via a 74AHCT125, button GPIO27 to GND, 12 V strip MOSFET GPIO25, DFPlayer TX GPIO17.

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

## 2. Wiring self-test (do this as soon as the wiring is finished)

Use a separate, adequately rated 5 V supply for the panels with a common ground to the ESP32. Do not power the panels from the ESP32 VIN/USB. The self-test uses the game's brightness cap (25/255); stage 1 lights all 768 pixels dimly. Check actual supply ratings before powering up.

1. Connect the ESP32 by a **data-capable** USB cable. Install the USB-serial driver (CP210x or CH340) if Windows shows no COM port. If upload reports a boot-mode error, hold the board's BOOT button while it starts connecting.
2. Run `npm run device:selftest`, then open the serial monitor command it prints (115200 baud).
3. **Short press** counts a press on every stage. **Hold 1 s** moves to the next stage. The serial monitor explains each stage.

| Stage | Expected | If wrong |
| --- | --- | --- |
| 1 Panel chain | First panel from GPIO18 red (bottom), next green (middle), last blue (top). Uses raw chain order. | Colours out of order: check DOUT→DIN. Dark panel: check its 5 V, GND and data. |
| 2 Orientation | White border; red top-left, green top-right, blue bottom-left, yellow bottom-right; an orange dot scans each row left→right, top→bottom. | Mirrored corners, zigzag or jumps: adjust `pixel()` in `stack_moko_baby.ino` (panel order, row direction, serpentine). |
| 3 Button | Count on the top panel; bottom row lights while held; serial prints gap and raw interrupt edges. | Bottom row always lit: GPIO27 stuck to GND. Many edges per press: mechanical bounce (the game debounces 20 ms / 65 ms). |
| 4 12 V strip | GPIO25 toggles every second; the strip follows the yellow block. | Check MOSFET gate, 12 V supply and common ground. |
| 5 Audio | DFPlayer plays `/mp3/0001.mp3`, `0002`, `0003`, 4 s apart. | Check SD card folder/names, TX→RX via 1 kΩ, speaker and `STACK_DFPLAYER_VOLUME`. |

If `pixel()` changes, re-run the self-test until stage 2 is correct. The game and the backend replay use logical x positions only, so a mapping fix does not change scoring.

## 3. Flash the game firmware for the hotspot

Start MySQL in XAMPP. In a PowerShell terminal (the values stay in that terminal session only):

```powershell
$env:STACK_FIRMWARE_WIFI_SSID = "YOUR-HOTSPOT-NAME"
$env:STACK_FIRMWARE_WIFI_PASSWORD = "YOUR-HOTSPOT-PASSWORD"
npm run online:device
```

The launcher prints the administrator and player links, saves the tunnel's verified root certificate, writes private `config.h` and uploads the game firmware. Keep the terminal running. **Each new run gets a new tunnel hostname**, so the cabinet must be re-flashed by USB every time the launcher restarts (a stable named tunnel would remove this; it needs a domain). If firmware upload fails, the dashboard stays online; fix the cause and run the retry command it prints.

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
| Mobile-data use over a 30-minute rehearsal recorded | Not run |

Passing these gates is physical acceptance evidence; Wokwi runs and backend tests are not.
