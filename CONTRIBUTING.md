# Contributing

Thank you for your interest in turtlend.

## Reporting problems and asking for help

Open an issue at
<https://github.com/Flux-Frontiers/turtlend/issues>. For a bug, include the
Python and NumPy versions, the shortest command sequence that reproduces the
problem, and what you expected the turtle to do. Questions about usage and
the frame conventions are welcome as issues too.

## Contributing changes

1. Fork the repository and create a branch from `main`.
2. Install the development tooling:

   ```bash
   poetry install --with dev
   ```

3. Make the change, add or update tests under `tests/`, and run:

   ```bash
   poetry run pytest
   poetry run ruff check src tests
   poetry run ruff format --check src tests
   ```

   The test suite enforces a coverage floor of 80 percent.

4. Open a pull request against `main` describing what changed and why.

`Turtle3D` keeps the conventions it has had since 1990 so that proteusPy
code runs unchanged, and `TurtleND(3)` must keep agreeing with it. A change
to either frame convention needs a matching change to the parity test in
`tests/test_turtle3d_frame.py` and an entry in `CHANGELOG.md`.

## License

By contributing you agree that your contribution is licensed under the
BSD-3-Clause license in `LICENSE`.
