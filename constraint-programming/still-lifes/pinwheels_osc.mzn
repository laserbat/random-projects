int: W = 16;
int: S = 3;
set of int: states = {-1, 0, 1};
set of int: coords = 0..W-1;
set of int: steps = 0..S-1;

array[-1..1, -8..8] of states: rule = array2d(-1..1, -8..8, [-1,-1,1,-1,-1,-1,0,0,0,0,0,1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,1,-1,-1,1,1,1,-1,0,0,0,0,0,1,1,1,-1,1,1]);

array[steps, coords, coords] of var states: world;

constraint forall (z in steps, i,j in 1..W-2) ( world[(z + 1) mod S,i,j] == rule[world[z,i,j],
    sum([
        world[z,i,j-1],world[z,i,j+1],world[z,i-1,j],world[z,i+1,j],
        world[z,i-1,j-1],world[z,i-1,j+1],world[z,i+1,j-1],world[z,i+1,j+1],
    ])]
);

constraint exists (i, j in coords) (world[0,i,j] != world[1,i,j]);

constraint forall (z in steps, i, j in coords) (
    (i <= 4 \/ j <= 4 \/ i >= W - 5 \/ j >= W - 5) -> (world[z,i,j] == 0)
);

output [ "array2d \(world[0,coords,coords])"];
