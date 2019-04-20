// gcc -Ofast -march=native ./infinite_state.c -o infinite_state; ./infinite_state | mpv - -scale oversample

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define W (1080 / 4)
#define H (1920 / 4)

// Fast swap function. Code from https://stackoverflow.com/questions/2786899/fastest-sort-of-fixed-length-6-int-array
#define min(x, y) (x<y?x:y)
#define max(x, y) (x<y?y:x)
#define SWAP(x,y) { const double a = min(temp[x], temp[y]); const double b = max(temp[x], temp[y]); temp[x] = a; temp[y] = b;}

int main(void){
    static uint32_t world[W][H][2] = {0};
    uint32_t u;
    int16_t i, j;
    int8_t flag = 0;

    srand(1113);

    for(i = 0; i < W; i ++){
        for(j = 0; j < H; j ++){
            world[i][j][0] = world[i][j][1] = rand();
        }
    }

    flag = 0;

    while (1){
        printf("P6\n%d %d\n255\n", H, W);
        for(i = 0; i < W; i ++){
            for(j = 0; j < H; j ++){
                uint32_t temp[9];

                // Put all neighbors into an array.
                temp[0] = world[i][j][flag];
                temp[1] = world[(W + i - 1) % W][j][flag];
                temp[2] = world[(i + 1) % W][j][flag];
                temp[3] = world[i][(H + j - 1) % H][flag];
                temp[4] = world[i][(j + 1) % H][flag];
                temp[5] = world[(i + 1) % W][(H + j - 1) % H][flag];
                temp[6] = world[(W + i - 1) % W][(j + 1) % H][flag];
                temp[7] = world[(i + 1) % W][(j + 1) % H][flag];
                temp[8] = world[(W + i - 1) % W][(H + j - 1) % H][flag];

                // Sort neighbors by using a sorting network.
                // Code from http://pages.ripco.net/~jgamble/nw.html
                SWAP(0, 1);
                SWAP(3, 4);
                SWAP(6, 7);
                SWAP(1, 2);
                SWAP(4, 5);
                SWAP(7, 8);
                SWAP(0, 1);
                SWAP(3, 4);
                SWAP(6, 7);
                SWAP(0, 3);
                SWAP(3, 6);
                SWAP(0, 3);
                SWAP(1, 4);
                SWAP(4, 7);
                SWAP(1, 4);
                SWAP(2, 5);
                SWAP(5, 8);
                SWAP(2, 5);
                SWAP(1, 3);
                SWAP(5, 7);
                SWAP(2, 6);
                SWAP(4, 6);
                SWAP(2, 4);
                SWAP(2, 3);
                SWAP(5, 6);

                u = temp[0] + temp[7] + temp[8];
                //u = temp[0] + temp[1] + temp[2] + temp[3] + temp[4] + temp[5] + temp[6] + temp[7] + temp[8];
                u = temp[u % 9];
                world[i][j][!flag] = u;
            
                putchar(u & 255); u >>= 3;
                putchar(u & 255); u >>= 3;
                putchar(u & 255);
            }
        }
        flag ^= 1;
    }
}
