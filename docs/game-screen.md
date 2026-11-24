# The web game screen (default game display)

Updated 25 November 2026. **The game migrated from the LED-matrix cabinet to a web game screen.** The stacking game runs as a full-screen web page on a second laptop (the *game screen*), and players still use the 60 mm arcade button. The player flow does not change: scan the QR, register, wait in line, get called, play, and see the result on the phone and the leaderboard.

**The LED cabinet is still supported.** Both use the same device protocol, the same Matrix v1 rules and the same leaderboard, and only one plays as Cabinet 01 at a time. An administrator switches between them in Settings → **Game screen** (see [switching back to the LED cabinet](#switching-back-to-the-led-cabinet)). The migration happened because the LED panels failed before the event; the plan (internally called *Plan B*) was assessed first, as below.

## Why the web screen is the default (assessment, 25 November)

It was judged a good idea, with the conditions below.

- **It removes the riskiest hardware.** LED power from a laptop USB port, 3.3 V data into 5 V LEDs, panel chain order and 768 LEDs are gone. Only the button and the ESP32 remain, with no power load.
- **Network delay cannot affect play.** The game runs in the screen's browser, and the ESP32 stamps each press with its own clock. The tunnel and hotspot only carry "this player is next" and the finished round.
- **Scores keep the same protection.** The screen plays as Cabinet 01 through the existing device journal (protocol v2). The server replays every placement against Matrix v1, checks the timing against the reservation, and keeps the review and recovery rules. Screen rounds share the leaderboard with earlier cabinet rounds (same rules, same `device` cohort).
- **Conditions:**
  - The screen must use **Chrome or Edge** (Web Serial).
  - The screen must open the **HTTPS tunnel address**: the same origin as the API, and a secure page for Web Serial.
  - The screen laptop stays plugged in and awake.
  - The device token sits in that browser's storage. The laptop is staff-held, and pairing again replaces the token.

## Roles

| Device | Job | Runs |
|---|---|---|
| Laptop 1 (operator) | Backend, MariaDB, tunnel, admin dashboard (queue, Call next, no-shows, recovery) | `npm run online` |
| Laptop 2 (game screen) | Runs and shows the game; uploads each finished round | Chrome or Edge at `https://<tunnel>/screen` |
| ESP32 (button bridge) | Reports each press over USB with its own timestamp; no Wi-Fi | `firmware/button_bridge/` |

## Button wiring

The only wiring now:

| From | To |
|---|---|
| Button switch COM | ESP32 GND |
| Button switch NO | ESP32 GPIO27 (internal pull-up, no resistor; NC unused) |
| Button light + | ESP32 5V/VIN pin (USB 5 V on most DevKits; check with a meter) |
| Button light − | ESP32 GND |
| ESP32 USB | Laptop 2 (data-capable cable) |

With the web screen, no LED panels, display power lead, capacitor, 330 Ω resistor or speaker are needed (keep them for the LED cabinet). Sound comes from laptop 2 as Web Audio square-wave beeps, the same notes as `firmware/stack_moko_baby/sounds.h`.

## Setup

**One time**
1. Flash the bridge with the ESP32 on USB: `npm run device:bridge -- --port COM5`. Like the other flash commands, it never erases the board, so the game firmware can be flashed back later.
2. Check it with `arduino-cli monitor -p COM5 -c baudrate=115200`. You should see `READY` every 5 s and one `PRESS <ms>` line per press. Close the monitor afterwards, because only one program can use the port.
3. Laptop 2 power settings: plugged in, *Screen and sleep: Never* when plugged in, and USB selective suspend off. `npm run event:check -- --fix-power` does this on a laptop that has the project. The page also requests a screen wake lock.

**Each event start, and whenever the tunnel address changes**
1. Laptop 1: run `npm run online`.
2. Laptop 2: open the tunnel address at `/admin/login` and sign in as an administrator.
3. Go to Settings → **Game screen** → **Use this laptop as the game screen**. The game screen opens.
4. Operator → **Connect button (USB)** and choose the ESP32 port. Later visits reconnect by themselves, including after unplugging.
5. Operator → **Full screen**, then click once so the browser allows sound. Signing out of the admin afterwards is fine; the screen does not use the staff session.

A new tunnel address is a different website to the browser. It brings new storage and a new serial permission, so pair again and connect the button again. Pairing is refused while a player is called or playing, and it cuts off any other screen and the LED cabinet until you switch back.

## How a round works

1. **Idle.** The screen sends a heartbeat (`ready`, firmware `web-screen-1`) and polls commands every second. Laptop 1's Machine page shows "Web game screen".
2. **Call next.** The operator calls the next player, and a reserve command arrives. The screen checks the Matrix v1 rules hash, saves the reservation, journals `reserved`, and shows *Your turn! Press the button to start* with the 3-minute limit.
3. **Start.** A press starts the 3-2-1 countdown (500 ms steps). When it ends, the start marker is saved, then journaled as `started`.
4. **Play.** Each press is timed from the ESP32's edge time, mapped to page time with the lowest-delay offset seen. It runs through `frontend/src/screen/engine.js`, an exact port of `game_engine.h`. The round ends on a full miss, at 15 levels, or after 60 s.
5. **Result.** The result is saved in the browser, then journaled as `terminal`. The server replays it and stores the score. The screen shows *Score saved to the leaderboard* for 8 s.

**Saved before sent.** Every journal event is stored in `localStorage` before it is sent, and resent unchanged until the server confirms it. A lost response or a server outage never creates a second, different result.

**Reload during a round.** If the page is reloaded mid-round, that round is lost from the page. The screen then registers a new boot, like an ESP32 reboot, and the server holds the round for review. On laptop 1, request a fence, then release the no-show or, as administrator, void the interrupted round.

**One tab only.** Only one game screen tab can run per browser (Web Locks), because two tabs would race the same journal.

## Fallbacks and fixes

| Screen shows | Do |
|---|---|
| Button not connected / unplugged | Operator → Connect button (USB). Replug the cable. Close any serial monitor. |
| No Web Serial: use Chrome or Edge | Use Chrome or Edge at the https tunnel address, not `http://<ip>`. |
| This laptop is not the game screen yet | Pair again (the tunnel address changed, or another screen was paired). |
| A server connection message | Check the tunnel on laptop 1. A running round finishes, and its score uploads later. |
| Round held | Use the round's recovery on laptop 1 (fence, then release or void). |
| The button breaks mid-event | Operator → Keyboard fallback: on, so the Space bar plays. It is off by default so passers-by cannot play from the laptop keyboard. |
| The active game is not Matrix v1 | Run the project setup on laptop 1 (`backend/setup_local.py`). |

## Switching back to the LED cabinet

Use this when working LED panels are available again (or for a test).

1. Flash the LED game firmware to the ESP32: `npm run online:device` with the hotspot name and password set (see [physical bring-up](hardware-bringup.md)). This replaces the button bridge; the button wiring stays the same, and the panels, power lead and speaker are wired as in the [PDF guide](Stack-Moko-Baby-Wiring-and-Operation-Guide.pdf), sections 1–3.
2. With no player called or playing, an administrator chooses Settings → Game screen → **Use the LED cabinet instead**. This restores the configured cabinet token (`STACK_DEVICE_TOKEN`, the one the launcher builds into the private `config.h`), so the paired game screen stops working. It is audited as `led_cabinet_restored`.
3. Check the Machine page shows the cabinet's firmware and *ready*, then call the next player as usual.

To return to the web screen, flash the bridge (`npm run device:bridge`) and pair the screen again. Scores from both stay on one leaderboard; the Sessions page labels the source *Game screen / cabinet*.

## Code map

- `frontend/src/screen/engine.js`: the Matrix v1 engine. `contracts/matrix-v1.vectors.json` holds 18 press-time vectors from an independent Python port. Both `backend/tests/test_matrix_vectors.py` (server `replay()`) and `engine.test.js` check them.
- `frontend/src/screen/deviceClient.js`: the protocol-v2 client, a port of `backend/recovery_emulator.py`.
- `frontend/src/screen/button.js`: Web Serial reader and the ESP32-to-page clock mapping.
- `frontend/src/screen/sound.js`: sounds.
- `frontend/src/pages/GameScreen.jsx`: the `/screen` page (canvas board in the three player colours, HUD, operator menu, wake lock).
- `frontend/src/components/GameScreenPairing.jsx`, `POST /api/admin/screen/pair` and `POST /api/admin/screen/use-led-cabinet`: administrator-only and audited (`screen_paired`, `led_cabinet_restored`). Pairing issues a new device token once; switching back restores the configured cabinet token. Both refuse while a round is active.
- `firmware/button_bridge/button_bridge.ino`, and `scripts/flash-device.py --bridge` (`npm run device:bridge`).
- Tests: `backend/tests/test_screen_pairing.py`, `frontend/src/screen/*.test.js`, and the browser journey `frontend/e2e/screen-game.spec.js`. Run the journey with `STACK_TEST_RULESET=matrix-v1`.

## Verified so far (25 November)

- **Automated:**
  - the engine matches the server on every vector;
  - the device client keeps and resends an unconfirmed result through a reload, and holds an interrupted round;
  - pairing and switching back are administrator-only, replace the token and are refused during a round;
  - device commands still carry no player identity.
- **Browser journey on a throwaway database, Edge headless with the keyboard fallback:**
  - pair from Settings;
  - call a real registered player and play a full round;
  - the screen's score equals the player's ticket score;
  - a reload during a second round puts it on hold for review.
- **Compiled:** the bridge sketch built with Arduino CLI, and the flash layout check passed (NVS not written).

Not yet run:
- the bridge on the real ESP32 and button;
- Web Serial with the real port;
- two laptops on the phone hotspot;
- real phones;
- a 10-round back-to-back rehearsal.

Those are the first items in [remaining work](remaining-work.md).
