int: W = 20;
set of int: states = {-1, 0, 1};
set of int: coords = 0..W-1;

array[-1..1, -8..8] of states: rule = array2d(-1..1, -8..8, [-1,-1,1,-1,-1,-1,0,0,0,0,0,1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,1,-1,-1,1,1,1,-1,0,0,0,0,0,1,1,1,-1,1,1]);

array[coords, coords] of var states: world;

constraint forall (i,j in 1..W-2) ( world[i,j] == rule[world[i,j],
    sum([
        world[i,j-1],world[i,j+1],world[i-1,j],world[i+1,j],
        world[i-1,j-1],world[i-1,j+1],world[i+1,j-1],world[i+1,j+1],
    ])]
);

constraint forall (i, j in coords) (
    (i <= 4 \/ j <= 4 \/ i >= W - 5 \/ j >= W - 5) -> (world[i,j] == 0)
);

output [ "array2d \(world[coords,coords])"];
