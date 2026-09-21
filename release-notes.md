# Release Notes -- v0.1.0

> Released: 2026-09-21

This is the first release of `turtlend`. It provides `TurtleND`, `Turtle3D`
and `Vector3D` as one package whose only dependency is NumPy. WaveRider 0.15.0
and proteusPy 0.100.3 each carried an identical copy of these three modules,
and this package replaces both copies.

## What changed

**One source for the turtles.** The modules come from the WaveRider copies with
the import path and the license headers changed. Before this release, both
downstream packages were tested against the built wheel: proteusPy passes the
same 289 tests and WaveRider the same 359 tests as before, and the coordinates
each package computes through the turtles are identical to eight decimal places.

**Three `Turtle3D` defects fixed.** `orient` did not update the `Position`
property. `ResetTape` raised `TypeError`. `orient_at_residue` raised
`AttributeError`, and its assertion checked the turtle's state in place of the
`orientation` argument. All three were present in both source copies, and no
code in either package called the affected paths.

**Types and documentation.** `Turtle3D` annotations use `numpy.ndarray`, and
the package ships a `py.typed` marker. A documentation site describes the frame
conventions, including why `yaw(a)` rotates by `180 - a` degrees while `turn(a)`
rotates by `a`, and carries an API reference for all three modules.

## Upgrading

To install, run `pip install turtlend`. The package requires Python 3.12 or
3.13, and works with NumPy 1.26 and NumPy 2.

Code that imports `proteusPy.turtle3D`, `proteusPy.turtleND`,
`proteusPy.vector3D` or the WaveRider equivalents needs no change. Those modules
re-export this package in the next proteusPy and WaveRider releases.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
