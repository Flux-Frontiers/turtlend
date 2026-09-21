# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `TurtleND`, `Turtle3D` and `Vector3D`, moved here from WaveRider 0.15.0 and
  proteusPy 0.100.3, which carried identical copies. The `vector3D` helper
  functions `calc_angle`, `calc_dihedral`, `distance3d`, `rms_difference` and
  `calculate_bond_angle` move with them.
- Tests for `TurtleND.orient`, `expand_dim`, `orient_toward`, `orient_in_time`
  and the tape, and for the `Turtle3D` accessors, orientation methods and
  coordinate transforms. A 200-step random sequence checks that `Turtle3D` and
  `TurtleND(3)` agree.

### Fixed

These three defects were present in both source copies. No code in WaveRider or
proteusPy called the affected paths.

- `Turtle3D.orient` did not update the `Position` property, which kept its
  previous value.
- `Turtle3D.ResetTape` raised `TypeError` because it called the `Recording`
  property as a function.
- `Turtle3D.orient_at_residue` raised `AttributeError` because it called a
  `set_orientation` method that does not exist. Its assertion also checked the
  turtle's state in place of the `orientation` argument.

### Changed

- `Turtle3D` type annotations use `numpy.ndarray` in place of the `numpy.array`
  function. `Turtle3D.unit` and `Turtle3D.Orientation` declare the types they
  return.
- All three modules declare the BSD-3-Clause license. The WaveRider copies
  declared CC 4.0 and BSD in their headers.
