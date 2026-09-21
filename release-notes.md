# Release Notes -- v0.1.0

First release. `turtlend` provides `TurtleND`, `Turtle3D` and `Vector3D` as one
package with NumPy as its only dependency.

WaveRider 0.15.0 and proteusPy 0.100.3 each carried identical copies of these
three modules. This package replaces both copies.

## Fixed

These defects were present in both source copies. No code in WaveRider or
proteusPy called the affected paths.

- `Turtle3D.orient` did not update the `Position` property.
- `Turtle3D.ResetTape` raised `TypeError`.
- `Turtle3D.orient_at_residue` raised `AttributeError`, and its assertion
  checked the turtle's state in place of the `orientation` argument.

## Changed

- `Turtle3D` type annotations use `numpy.ndarray`, and the package ships a
  `py.typed` marker.
- All three modules declare the BSD-3-Clause license.

See [CHANGELOG.md](CHANGELOG.md) for the full list.
