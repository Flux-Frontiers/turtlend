# turtlend

[![PyPI](https://img.shields.io/pypi/v/turtlend.svg)](https://pypi.org/project/turtlend/)
[![Python](https://img.shields.io/pypi/pyversions/turtlend.svg)](https://pypi.org/project/turtlend/)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![Tests](https://github.com/Flux-Frontiers/turtlend/actions/workflows/tests.yml/badge.svg)](https://github.com/Flux-Frontiers/turtlend/actions/workflows/tests.yml)
[![Docs](https://github.com/Flux-Frontiers/turtlend/actions/workflows/docs.yml/badge.svg)](https://flux-frontiers.github.io/turtlend/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.XXXXXXX-blue.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0009--0891--1507-A6CE39.svg)](https://orcid.org/0009-0009-0891-1507)

A turtle that carries its own orthonormal frame through 3- or N-dimensional space.

`turtlend` provides three classes and depends only on NumPy:

- `TurtleND` holds a position and an orthonormal frame in N dimensions. It moves
  along its heading and rotates in the plane of any two basis vectors.
- `Turtle3D` is the three-dimensional turtle that `TurtleND` generalizes. It
  builds molecular geometry from bond lengths, bond angles and dihedral angles.
- `Vector3D` is the vector class that `Turtle3D` uses, with helper functions
  for angles, dihedrals and distances.

`Turtle3D` began as C code written in 1990 and was ported to Python for
[proteusPy](https://github.com/suchanek/proteusPy). `TurtleND` was written for
[WaveRider](https://github.com/Flux-Frontiers/waverider). Both packages carried
their own copies of these modules. This package is the single source for both.

## Install

```bash
pip install turtlend
```

`turtlend` requires Python 3.12 or 3.13.

## Move a turtle in N dimensions

All angles are in degrees.

```python
from turtlend import TurtleND

turtle = TurtleND(ndim=5)
turtle.move(1.0)             # along the heading, frame[0]
turtle.rotate(90.0, 0, 3)    # in the plane of basis vectors 0 and 3
turtle.move(1.0)

print(turtle.position)       # position in global coordinates
print(turtle.heading)        # frame[0]
```

In three or more dimensions, `roll`, `pitch`, `yaw` and `turn` are named cases
of `rotate` and follow the `Turtle3D` conventions.

To convert a vector between the global frame and the turtle's frame, call
`to_local` or `to_global`.

## Record a path

To record each position the turtle visits, set `recording` to `True`:

```python
turtle.recording = True
turtle.move(1.0)
turtle.turn(30.0)
turtle.move(1.0)

path = turtle.tape           # list of position arrays
turtle.reset_tape()
```

## Add a dimension to a live turtle

`expand_dim` grows the position and the frame from N to N+1 dimensions and
returns the index of the new axis. The existing basis vectors are unchanged.

```python
axis = turtle.expand_dim(label="time")
turtle.orient_in_time(axis)  # heading becomes the negative unit vector of that axis
```

`orient_in_time` points the heading along the negative direction of the axis.
To rotate the heading toward an arbitrary direction, call `orient_toward`.

## Use the 3-D turtle

```python
from turtlend import Turtle3D

turtle = Turtle3D()
turtle.move(1.53)
turtle.turn(109.5)
turtle.roll(60.0)
```

To place the turtle on a protein backbone, call `orient_from_backbone` with
the N, CA, CB and C atom positions as NumPy arrays.

## Develop

```bash
poetry install --with dev
poetry run pytest
```

## Cite

The citation metadata is in [CITATION.cff](CITATION.cff); GitHub renders it
under "Cite this repository". The equivalent BibTeX entry is:

```bibtex
@software{suchanek2026turtlend,
  author  = {Suchanek, Eric G.},
  title   = {turtlend: Orthonormal-Frame Turtles in 3 and N Dimensions},
  version = {0.1.1},
  year    = {2026},
  url     = {https://github.com/Flux-Frontiers/turtlend},
  doi     = {10.5281/zenodo.XXXXXXX},
  license = {BSD-3-Clause}
}
```

`zenodo.XXXXXXX` is a placeholder. Zenodo mints the DOI when it archives the
first GitHub Release; replace it with the concept DOI (the one that always
resolves to the newest version, from the `conceptdoi` field of the Zenodo API,
not the version DOI shown on the record page) here, in the badge above, and in
`CITATION.cff`.

An article describing the approach and the algorithms is in
[articles/turtlend.tex](articles/turtlend.tex), with a compiled
[PDF](articles/turtlend.pdf).

## License

BSD-3-Clause. See [LICENSE](LICENSE).
