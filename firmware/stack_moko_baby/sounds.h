#pragma once
#include <stdint.h>
// Simple speaker sounds (STACK_USE_PIEZO): no sound files or sound module.
// Kept in a header so Arduino's generated prototypes can see the Note type.
struct Note { uint16_t hz, ms; };  // hz 0 = rest
// 3, 2, 1, GO: each beat is 120 ms tone + 10 ms gap + 360 ms rest + 10 ms gap = 500 ms,
// matching the firmware's 500 ms countdown steps.
const Note SOUND_COUNTDOWN[]={{880,120},{0,360},{880,120},{0,360},{880,120},{0,360},{1760,250}};
const Note SOUND_LOSS[]={{392,160},{330,160},{262,420}};
const Note SOUND_WIN[]={{523,120},{659,120},{784,120},{1047,380}};
const Note SOUND_PLACE[]={{1200,30}};
#define PLAY_SOUND(notes) playSound(notes,sizeof(notes)/sizeof(notes[0]))
