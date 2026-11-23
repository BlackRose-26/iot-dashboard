#pragma once
#include <stdint.h>

// Integer elapsed-time motion is shared with backend replay; network speed
// cannot slow a row or alter the recorded x position.
struct StackPlacement { int x, width, overlap; uint32_t locked; };
struct StackGame {
  static constexpr int columns=16, levels=15, initialWidth=6;
  StackPlacement trace[levels]{};
  int support=5, width=6, count=0, score=0;
  uint32_t lastLock=0, duration=0;
  bool ended=false, won=false;
  int interval() const { return count==0 ? 60 : 50; }
  int x(uint32_t elapsed) const {
    int span=columns-width;
    int phase=((elapsed-lastLock)/interval())%(2*span);
    return phase<=span ? phase : 2*span-phase;
  }
  void timeout() { ended=true; duration=60000; }
  bool press(uint32_t elapsed) {
    if (ended) return false;
    if (elapsed>=60000) { timeout(); return false; }
    if (elapsed-lastLock<30) return false;
    int pos=x(elapsed);
    int left=pos>support?pos:support;
    int right=pos+width<support+width?pos+width:support+width;
    int overlap=right>left?right-left:0;
    trace[count++]={pos,width,overlap,elapsed};
    lastLock=elapsed;
    if (!overlap) { ended=true; duration=elapsed; }
    else {
      score++; support=left; width=overlap;
      if (score==levels) { won=true; ended=true; duration=elapsed; }
    }
    return true;
  }
};
