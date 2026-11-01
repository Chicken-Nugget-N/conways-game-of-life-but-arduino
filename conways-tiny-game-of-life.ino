
#include "LedControl.h"
#include "binary.h"

LedControl lc = LedControl(12, 11, 10, 12);

const int gwidth = 8;
const int glngth = 8;
const int delaytime = 100;
bool grid[glngth][gwidth];
bool nextgrid[glngth][gwidth];

void setup() {
  lc.shutdown(0, false);
  lc.setIntensity(0, 8);
  lc.clearDisplay(0);

  randomSeed(analogRead(A0));

  for (int a = 0; a<glngth; a++){
    for (int b = 0; b<gwidth; b++){
      grid[a][b] = random(2);
    }
  }
}

void gridDisplay() {
  for (int y = 0; y<glngth; y++){
    byte row = 0;
    for (int b = 0; b<gwidth; b++){
      if (grid[y][b]) {
        row |= (1 << (7 - b));
      }
    }

    lc.setRow(0, y, row);
  }
}

int NeyborCnt(int x, int y) {
  int count = 0;

  for (int dy = -1; dy <= 1; dy++) {
    for (int dx = -1; dx<= 1; dx++){
      if (dy == 0 && dx ==0) {
        continue;
      }

      int newx = x + dx;
      int newy = y + dy;

      if (newx >= 0 && newx < gwidth && newy >= 0 && newy < glngth) {
        if (grid[newy][newx] == 1){
          count += 1;
        }
      }

    }
  }

  return count;
}

void nextGen() {
  for (int a = 0; a<glngth; a++){
    for (int b = 0; b<gwidth; b++){
      int nebcnt = NeyborCnt(b, a);
      if (grid[a][b]) {

        nextgrid[a][b] = (nebcnt == 2 || nebcnt == 3);

      } else {

        // Rule 4: Reproduction
        nextgrid[a][b] = (nebcnt == 3);
      }
    }
  }
}

void loop() {
  nextGen();

  // Update board
  for (int y = 0; y < glngth; y++) {
    for (int x = 0; x < gwidth; x++) {
      grid[y][x] = nextgrid[y][x];
    }
  }

  gridDisplay();

  delay(delaytime);
}
