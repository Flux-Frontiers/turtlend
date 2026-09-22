# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The `zenodo.XXXXXXX` placeholder in the README badge, the README BibTeX and
  `CITATION.cff` is replaced by the Zenodo concept DOI,
  `10.5281/zenodo.22886555`, minted when Zenodo archived the v0.1.1 release.

## [0.1.1] - 2026-09-21

### Added

- `articles/turtlend.tex`, an article describing the approach and the
  algorithms: the frame and its Givens rotations, the operations and their
  invariants, the conventions that make `TurtleND(3)` agree with `Turtle3D`,
  the `orient`, `orient_toward`, `orthonormalize` and `expand_dim` algorithms,
  cost and drift, and the two applications. With its bibliography and a
  compiled PDF.
- README badges for PyPI, Python versions, license, the tests and docs
  workflows, Poetry, ORCID and a DOI placeholder, and a Cite section that
  points to `CITATION.cff` and gives the BibTeX entry.

### Changed

- The Zenodo DOI is a `zenodo.XXXXXXX` placeholder in the README badge, the
  README BibTeX and a commented line in `CITATION.cff`, to be replaced by the
  concept DOI once Zenodo archives a release.

## [0.1.0] - 2026-09-21

### Added

- `TurtleND`, `Turtle3D` and `Vector3D`, moved here from WaveRider 0.15.0 and
  proteusPy 0.100.3, which carried identical copies. The `vector3D` helper
  functions `calc_angle`, `calc_dihedral`, `distance3d`, `rms_difference` and
  `calculate_bond_angle` move with them.
- Tests for `TurtleND.orient`, `expand_dim`, `orient_toward`, `orient_in_time`
  and the tape, and for the `Turtle3D` accessors, orientation methods and
  coordinate transforms. A 200-step random sequence checks that `Turtle3D` and
  `TurtleND(3)` agree.
- A documentation site built with mkdocs and mkdocstrings: a frame-conventions
  page and an API reference for all three modules.
- `CITATION.cff`, and a release workflow that publishes to PyPI by trusted
  publishing on a `v*` tag.

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
- Docstrings drop `:type:` lines that repeated a signature annotation, and
  `Turtle3D.new` no longer documents a `pen` parameter it does not have.
- All three modules declare the BSD-3-Clause license. The WaveRider copies
  declared CC 4.0 and BSD in their headers.
