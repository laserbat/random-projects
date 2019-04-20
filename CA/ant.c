// gcc -Ofast -march=native ./ant.c -o ant; ./ant | mpv - -scale oversample

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define W (1080 / 4)
#define H (1920 / 4)

const int dir[9][2] = {
    {0, 1}, {1, 0}, {0, -1}, {-1, 0}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
};

int main(void){
    static uint32_t world[W][H] = {0};
    uint32_t u;
    int16_t i, j, k;

    uint32_t ax, ay, as;

    srand(12343);

    ax = W/2;
    ay = H/2;
    as = rand();

    world[ax][ay] = as;

    while (1){
        printf("P6\n%d %d\n255\n", H, W);
        for(i = 0; i < W; i ++){
            for(j = 0; j < H; j ++){
                u = world[i][j];
            
                putchar(u & 255); u >>= 3;
                putchar(u & 255); u >>= 3;
                putchar(u & 255);
            }
        }

        for(k = 0; k < 8; k ++){
            world[ax][ay] = as;
            ax = (ax + W + dir[as % 9][0]) % W;
            ay = (ay + H + dir[as % 9][1]) % H;
            as += world[ax][ay];
        }
    }
}
