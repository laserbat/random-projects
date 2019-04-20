include "alldifferent.mzn";

set of int: notes = 0..11;

array[notes] of var notes: row_prime;
array[notes] of var notes: row_retrograde;
array[notes] of var notes: row_inverse;
array[notes] of var notes: row_retinv;

array[0..1, notes] of var notes: rows;

array [0..1] of var notes: shift;
array [0..1] of var notes: pitch;
array [0..1] of var bool:  inv;
array [0..1] of var bool:  ret;

array[notes] of var bool: chords;

predicate chord(var int: a, var int: b, var int: c) = (
    let {
        var notes: A = abs(a - b);
        var notes: B = abs(b - c);
        var notes: C = abs(a - c);
    } in (
        A in {3, 4, 7} /\
        B in {3, 4, 7} /\
        C in {3, 4, 7} /\
        A != B /\
        A != C /\ 
        B != C
    )
);

predicate equiv(array[notes] of var notes: row1, array[notes] of var notes: row2, var notes: pitch, var notes: shift) = (
    forall (i in notes) (
        (row1[(i + 12 - shift) mod 12] + 12 - pitch) mod 12 == row2[i]
    )
);

constraint alldifferent(row_prime);

% redundant but speed up computing
constraint alldifferent(row_retrograde);
constraint alldifferent(row_inverse);
constraint alldifferent(row_retinv);

% symmetry breaking
constraint row_prime[0] = 0;

constraint forall (i in notes) (row_retrograde[11 - i] == row_prime[i]);
constraint forall (i in notes) (row_retinv[11 - i] == row_inverse[i]);

constraint row_inverse[0] == row_prime[0];
constraint forall (i in 1..11) (
    row_inverse[i] == (
        row_inverse[i - 1] + row_prime[i - 1] - row_prime[i] + 12
    ) mod 12
);

constraint (
    forall (i in 0..1) (
        let {
            array[notes] of var notes: row = rows[i,notes];
        } in (
            ((not inv[i] /\ not ret[i]) -> equiv(row, row_prime,      pitch[i], shift[i])) /\
            ((    inv[i] /\ not ret[i]) -> equiv(row, row_inverse,    pitch[i], shift[i])) /\
            ((not inv[i] /\     ret[i]) -> equiv(row, row_retrograde, pitch[i], shift[i])) /\
            ((    inv[i] /\     ret[i]) -> equiv(row, row_retinv,     pitch[i], shift[i]))
        )
    )
);

constraint forall (i in notes) (
    chords[i] -> chord(row_prime[i], rows[0,i], rows[1,i])
);

constraint shift[0] > 0;
constraint shift[1] > 0;
constraint shift[0] != shift[1];
constraint sum(chords) > 0;

solve satisfy;
output ["\(row_prime) -- prime\n",
        "\(rows[0,notes]) -- inverse: \(inv[0]), retrograte: \(ret[0]), +\(pitch[0]) semitones, shift: \(shift[0])\n",
        "\(rows[1,notes]) -- inverse: \(inv[1]), retrograde: \(ret[1]), +\(pitch[1]) semitones, shift: \(shift[1])\n",
        "\(chords)\n"
];
