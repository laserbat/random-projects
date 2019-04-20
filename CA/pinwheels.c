// gcc -Ofast -march=native ./pinwheels.c -o pinwheels; ./pinwheels | mpv - -scale oversample

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define W (1080 / 4)
#define H (1920 / 4)

#define STATES 3

char rule[] = "--+---00000+---++"
              "------00000++++++"
              "--+++-00000+++-++";

int8_t table[3][17];

int main(int argc, char **argv){
    static int8_t world[W][H][2] = {0};
    static uint32_t color[STATES] = {0x20400FF, 0, 0xFF4020};
    int16_t i, j, k;
    int8_t flag = 0;

    srand(12343);

    for(i = 0; i < 3; i ++){
        for(j = 0; j < 17; j ++){
            k = rule[17 * i + j];
            
            switch(k){
                case '0':
                    table[i][j] = 0;
                    break;
                case '+':
                    table[i][j] = 1;
                    break;
                case '-':
                    table[i][j] = -1;
            }
        }
    }

    for(i = 0; i < W; i ++){
        for(j = 0; j < H; j ++){
            world[i][j][0] = world[i][j][1] = (rand() % 3) - 1; 
        }
    }

    flag = 0;

    while (1){
        printf("P6\n%d %d\n255\n", H, W);
        for(i = 0; i < W; i ++){
            for(j = 0; j < H; j ++){
                int8_t temp[9], sum = 8;
                int64_t u;

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

                for (k = 1; k < 9; k ++){
                    sum += temp[k];
                }

                u = table[temp[0] + 1][sum];

                world[i][j][!flag] = u;
                u = color[u + 1];
        
                putchar(u & 255); u >>= 8;
                putchar(u & 255); u >>= 8;
                putchar(u & 255);
            }
        }
        flag ^= 1;
    }
}
