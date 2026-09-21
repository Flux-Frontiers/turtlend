# Frame conventions

Both turtles use the same conventions, so a `TurtleND(3)` and a `Turtle3D`
given the same commands end at the same position with the same frame. The test
suite checks this over a 200-step random sequence.

## The frame

`TurtleND` stores its frame as the rows of an $n \times n$ matrix:

| Row | Name | Property |
|---|---|---|
| `frame[0]` | heading | `heading` |
| `frame[1]` | left | `left` |
| `frame[2]` | up, when $n \ge 3$ | `up` |
| `frame[3]` and higher | unnamed | `basis(i)` |

A new turtle sits at the origin with the identity frame. `move(d)` adds
$d \cdot \text{heading}$ to the position. Rotations never change the position.

The `position`, `frame`, `heading`, `left`, `up` and `basis(i)` accessors return
copies. To change the turtle, call its methods.

## Rotations

All angles are in degrees.

`rotate(angle, i, j)` applies a Givens rotation in the plane of basis vectors
$i$ and $j$. It rotates $b_i$ toward $b_j$:

$$
b_i' = \cos\theta \, b_i + \sin\theta \, b_j
\qquad
b_j' = \cos\theta \, b_j - \sin\theta \, b_i
$$

Only those two basis vectors change. The named rotations are cases of `rotate`:

| Method | Equivalent | In 3-D, rotates about |
|---|---|---|
| `turn(a)` | `rotate(a, 0, 1)` | up |
| `roll(a)` | `rotate(a, 1, 2)` | heading |
| `pitch(a)` | `rotate(-a, 0, 2)` | left |
| `yaw(a)` | `rotate(180 - a, 0, 1)` | up |

`roll` and `pitch` require at least three dimensions.

!!! warning "`yaw` is not `turn`"
    `yaw(a)` rotates by $180 - a$ degrees, not by $a$. This is the
    molecular-building convention from `Turtle3D`: after a bond of a given
    length, `yaw(bond_angle)` points the heading along the next bond. To rotate
    the heading by a plain angle, call `turn`.

## Coordinate transforms

`to_local(p)` returns the coordinates of the global point `p` in the turtle's
frame: the projection of `p - position` onto each basis vector. `to_global`
is its inverse.

## Numerical drift

Each rotation renormalizes the two basis vectors it changes. It does not
restore their orthogonality to each other or to the rest of the frame. After
many thousands of rotations, call `orthonormalize()` to rebuild the frame with
a QR decomposition. Each rebuilt vector keeps the direction of the vector it
replaces.

## Differences in Turtle3D

`Turtle3D` predates `TurtleND` and keeps its original interface:

- Properties are capitalized: `Position`, `Heading`, `Left`, `Up`, `Name`,
  `Pen`, `Recording`, `Orientation`. They return `Vector3D` objects, not arrays.
- `move` does not record to a tape. `TurtleND.move` records when `recording`
  is `True`.
- `Orientation` records which of two protein-building poses the turtle is in.
  `ORIENT_BACKBONE` is at the alpha carbon heading toward the carbonyl carbon.
  `ORIENT_SIDECHAIN` is at the alpha carbon heading toward the beta carbon.
  In both, the nitrogen is on the left. `bbone_to_schain` and
  `schain_to_bbone` convert between them.
