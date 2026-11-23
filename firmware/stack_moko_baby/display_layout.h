#pragma once
// Physical LED layout (not secret; safe to commit and share).
// Data chain on GPIO18: 8x32 HUD first -> bottom 16x16 block panel -> upper 16x16 block panel.
// Run `npm run device:selftest` (stage 2) and change only these flags if the picture is
// mirrored or scrambled. Game rules, timing and scoring do not depend on these values.

// ---- 8x32 HUD on top: logical 32 wide x 8 tall, x left->right, y top->bottom ----
// Common flexible 8x32 WS2812B panels run in zigzag columns of 8 (column-major).
#ifndef STACK_HUD_COLUMN_MAJOR
#define STACK_HUD_COLUMN_MAJOR 1   // 1: LEDs run down/up columns of 8. 0: LEDs run along rows of 32.
#endif
#ifndef STACK_HUD_SERPENTINE
#define STACK_HUD_SERPENTINE 1     // 1: every other column/row runs backwards (zigzag).
#endif
#ifndef STACK_HUD_FLIP_X
#define STACK_HUD_FLIP_X 0         // 1: mirror left/right (DIN on the right-hand end).
#endif
#ifndef STACK_HUD_FLIP_Y
#define STACK_HUD_FLIP_Y 0         // 1: mirror top/bottom.
#endif

// ---- Two 16x16 block panels below: logical 16 wide x 32 tall, y 0 = top ----
#ifndef STACK_BLOCK_FLIP_X
#define STACK_BLOCK_FLIP_X 0       // 1: mirror each block panel left/right.
#endif
#ifndef STACK_BLOCK_FLIP_ROWS
#define STACK_BLOCK_FLIP_ROWS 0    // 1: each block panel's first LED row is at its bottom.
#endif
