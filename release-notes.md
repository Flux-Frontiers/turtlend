# Release Notes -- v0.1.1

> Released: 2026-09-21

This release adds the article that describes the turtle, and the badges and
citation section the README was missing. The code is unchanged from 0.1.0.

## What changed

**The article.** `articles/turtlend.tex` is a twelve-page description of the
approach and the algorithms. It defines the orthonormal frame and the Givens
rotation, gives the operations and the invariants they preserve with proofs,
explains the `Turtle3D` conventions that `TurtleND` inherits (including why
`yaw` rotates by `180 - a`), and gives pseudocode for `orient`,
`orient_toward`, `orthonormalize` and `expand_dim`. A section on numerical
behavior gives the cost of each operation and the size of the orthogonality
drift after many rotations. The bibliography and a compiled PDF ship with it.
It also records one difference the tests do not cover: `TurtleND.orient` in
three dimensions can produce a left-handed frame, where `Turtle3D.orient`
always produces a right-handed one.

**README badges and citation.** The README carries badges for PyPI, Python
versions, license, the tests and docs workflows, Poetry and ORCID, and a Cite
section that points to `CITATION.cff` and gives the BibTeX entry. The DOI
badge and the BibTeX `doi` field hold a `zenodo.XXXXXXX` placeholder, as does a
commented line in `CITATION.cff`, until Zenodo archives a release and mints the
concept DOI.

## Upgrading

Run `pip install --upgrade turtlend`. No code changed, so nothing needs to be
done.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
