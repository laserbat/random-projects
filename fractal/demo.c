// gcc -Ofast -march=native demo.c -o demo; ./demo | mpv - -fs -scale=nearest
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

#define W (1920)
#define H (1080)

#define MIN_FRAMES 64
#define BITS 11
#define NUMVAR 4

uint8_t func(uint16_t x, uint16_t y, uint64_t operator){
    uint16_t val[NUMVAR] = {x, y};
    uint16_t assignment;
    uint16_t variation = operator & 1;

    uint16_t i, j;

    operator >>= 1;

    val[2] = x >> (1 + variation);
    val[3] = y >> (1 + variation);

    for(i = 0; i < BITS; i ++){
        assignment = 0;
        for(j = 0; j < NUMVAR; j ++){
            assignment <<= 1;
            assignment |= val[j] & 1;

            val[j] >>= 1;
        }

        if ((operator >> assignment) & 1)
            return 1;
    }

    return 0;
}

int check(uint64_t operator){
    uint16_t x, y;
    uint32_t total = 0;
    for (x = 0; x < H / 2; x ++)
        for (y = 0; y < W / 2; y ++)
            if (!func(x, y, operator))
                total ++;

    return (total > (W * H / 32));
}

int main(int argc, char **argv){
    uint16_t shift = 0;
    uint16_t x, y;

    uint64_t op, new_op;
    uint16_t new_op_good = 0;

    uint8_t out;

    srand(time(0));

    do {
        op = rand();
    } while (!check(op));

    while(1){
        shift += 1;

        if(!new_op_good){
            new_op = rand();
            new_op_good = check(new_op);
        } else if (shift > MIN_FRAMES){
            shift = new_op_good = 0;
            op = new_op;
        }

        printf("P4\n%d %d\n", W, H);
        for (x = 0; x < H; x ++){
            for (y = 0; y < W; y ++){
                out <<= 1;
                out |= func(x + (4 * shift), y, op);

                if (y % 8  == 7)
                    putchar(out);
            }

            if (W % 8 != 0)
                putchar(out);
        }
    }
}
