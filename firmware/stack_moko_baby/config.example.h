#pragma once
// Copy to config.h; keep that file private. Never paste an event token into
// a public Wokwi project. Use a separate synthetic event for public simulations.
#define STACK_WIFI_SSID "Wokwi-GUEST"
#define STACK_WIFI_PASSWORD ""
#define STACK_API_BASE "https://YOUR-SERVICE.onrender.com"
#define STACK_DEVICE_TOKEN "REPLACE_WITH_PRIVATE_DEVICE_TOKEN"
// PEM trust anchor for the HTTPS server. See docs/esp32-online.md.
#define STACK_ROOT_CA ""
#define STACK_ALLOW_LOCAL_HTTP 0
#define STACK_USE_PIEZO 0
#define STACK_USE_DFPLAYER 1
#define STACK_DFPLAYER_VOLUME 8
#define STACK_COUNTDOWN_STEP_MS 500
