"""
turtlend: a turtle that carries its own coordinate frame, in 3 or N dimensions.

``TurtleND`` holds a position and an orthonormal frame in N-dimensional space.
It moves along its heading and rotates in the plane of any two basis vectors.
``Turtle3D`` is the three-dimensional original it generalizes, and ``Vector3D``
is the vector class ``Turtle3D`` is built on.

Author: Eric G. Suchanek, PhD
Affiliation: Flux-Frontiers, https://github.com/Flux-Frontiers
License: BSD-3-Clause
"""

from importlib.metadata import PackageNotFoundError, version

from .turtle3D import ORIENT_BACKBONE, ORIENT_SIDECHAIN, Turtle3D
from .turtleND import TurtleND
from .vector3D import (
    Vector3D,
    calc_angle,
    calc_dihedral,
    calculate_bond_angle,
    distance3d,
    rms_difference,
)

try:
    __version__ = version("turtlend")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "ORIENT_BACKBONE",
    "ORIENT_SIDECHAIN",
    "Turtle3D",
    "TurtleND",
    "Vector3D",
    "calc_angle",
    "calc_dihedral",
    "calculate_bond_angle",
    "distance3d",
    "rms_difference",
]
