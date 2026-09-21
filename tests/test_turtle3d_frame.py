"""Tests for the Turtle3D accessors, orientation and coordinate transforms that
the original suite does not reach, plus a long-sequence parity check against
TurtleND(3)."""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from turtlend import ORIENT_BACKBONE, ORIENT_SIDECHAIN, Turtle3D, TurtleND, Vector3D

_tolerance = 1e-10


def frame_of(turtle: Turtle3D) -> np.ndarray:
    return np.array([turtle.Heading.get_array(), turtle.Left.get_array(), turtle.Up.get_array()])


def assert_orthonormal(turtle: Turtle3D) -> None:
    frame = frame_of(turtle)
    assert_allclose(frame @ frame.T, np.eye(3), atol=_tolerance)


class TestAccessors:
    @pytest.mark.parametrize("attr", ["Position", "Heading", "Left", "Up"])
    def test_setter_accepts_vector_and_sequence(self, attr):
        t = Turtle3D()
        setattr(t, attr, Vector3D(0.0, 0.0, 2.0))
        assert_allclose(getattr(t, attr).get_array(), [0, 0, 2])
        setattr(t, attr, [0.0, 3.0, 0.0])
        assert_allclose(getattr(t, attr).get_array(), [0, 3, 0])

    @pytest.mark.parametrize("attr", ["Position", "Heading", "Left", "Up"])
    def test_setter_rejects_wrong_length(self, attr):
        with pytest.raises(ValueError):
            setattr(Turtle3D(), attr, [1.0, 2.0])

    def test_name(self):
        t = Turtle3D("builder")
        assert t.Name == "builder"
        t.Name = "walker"
        assert t.Name == "walker"

    def test_pen(self):
        t = Turtle3D()
        assert t.Pen == "up"
        t.Pen = "down"
        assert t.Pen == "down"
        t.Pen = "up"
        assert t.Pen == "up"

    def test_recording(self):
        t = Turtle3D()
        assert t.Recording is False
        t.Recording = True
        assert t.Recording is True

    def test_reset_tape_stops_recording(self):
        t = Turtle3D()
        t.Recording = True
        t.ResetTape()
        assert t.Recording is False

    def test_orientation_accepts_only_the_two_constants(self):
        t = Turtle3D()
        t.Orientation = ORIENT_BACKBONE
        assert t.Orientation == ORIENT_BACKBONE
        t.Orientation = ORIENT_SIDECHAIN
        assert t.Orientation == ORIENT_SIDECHAIN
        with pytest.raises(AssertionError):
            t.Orientation = 3

    def test_repr_names_the_turtle(self):
        assert "builder" in repr(Turtle3D("builder"))


class TestCopyAndReset:
    def test_copy_coords_copies_frame_and_orientation(self):
        source = Turtle3D()
        source.turn(40.0)
        source.pitch(15.0)
        source.move(2.5)
        source.Orientation = ORIENT_BACKBONE

        target = Turtle3D()
        target.copy_coords(source)
        assert_allclose(target.Position.get_array(), source.Position.get_array())
        assert_allclose(frame_of(target), frame_of(source))
        assert target.Orientation == ORIENT_BACKBONE

        # a copy, not a shared reference
        source.move(1.0)
        assert not np.allclose(target.Position.get_array(), source.Position.get_array())

    def test_reset_returns_to_origin_and_identity(self):
        t = Turtle3D()
        t.turn(40.0)
        t.move(2.5)
        t.reset()
        assert_allclose(t.Position.get_array(), [0, 0, 0])
        assert_allclose(frame_of(t), np.eye(3))


class TestOrient:
    def test_orient_builds_right_handed_orthonormal_frame(self):
        t = Turtle3D()
        position = np.array([1.0, 1.0, 1.0])
        t.orient(position, position + [0.0, 2.0, 0.0], position + [-3.0, 1.0, 0.0])

        assert_allclose(t.Position.get_array(), position)
        assert_allclose(t.Heading.get_array(), [0, 1, 0], atol=_tolerance)
        assert_allclose(t.Left.get_array(), [-1, 0, 0], atol=_tolerance)
        assert_allclose(t.Up.get_array(), [0, 0, 1], atol=_tolerance)
        assert_orthonormal(t)

    def test_orient_from_backbone(self):
        n = np.array([-1.0, 1.0, 0.0])
        ca = np.array([0.0, 0.0, 0.0])
        cb = np.array([0.0, 0.0, 1.5])
        c = np.array([1.5, 0.0, 0.0])

        t = Turtle3D()
        t.orient_from_backbone(n, ca, cb, c, ORIENT_BACKBONE)
        assert t.Orientation == ORIENT_BACKBONE
        assert_allclose(t.Position.get_array(), ca)
        assert_allclose(t.Heading.get_array(), [1, 0, 0], atol=_tolerance)
        assert_orthonormal(t)

        t.orient_from_backbone(n, ca, cb, c, ORIENT_SIDECHAIN)
        assert t.Orientation == ORIENT_SIDECHAIN
        assert_allclose(t.Heading.get_array(), [0, 0, 1], atol=_tolerance)
        assert_orthonormal(t)

    def test_orient_at_residue_reads_a_biopython_style_chain(self):
        class Atom:
            def __init__(self, xyz):
                self._xyz = np.array(xyz, "d")

            def get_vector(self):
                return self

            def get_array(self):
                return self._xyz

        residue = {
            "N": Atom([-1, 1, 0]),
            "CA": Atom([2, 2, 2]),
            "CB": Atom([2, 2, 3.5]),
            "C": Atom([3.5, 2, 2]),
        }
        chain = {7: residue}

        t = Turtle3D()
        t.orient_at_residue(chain, 7, ORIENT_BACKBONE)
        assert t.Orientation == ORIENT_BACKBONE
        assert_allclose(t.Position.get_array(), [2, 2, 2])
        assert_allclose(t.Heading.get_array(), [1, 0, 0], atol=_tolerance)

        t.orient_at_residue(chain, 7, ORIENT_SIDECHAIN)
        assert t.Orientation == ORIENT_SIDECHAIN
        assert_allclose(t.Heading.get_array(), [0, 0, 1], atol=_tolerance)

        with pytest.raises(AssertionError):
            t.orient_at_residue(chain, 7, 3)

    def test_orient_from_backbone_does_not_modify_inputs(self):
        atoms = [np.array(v, "d") for v in ([-1, 1, 0], [0, 0, 0], [0, 0, 1.5], [1.5, 0, 0])]
        before = [a.copy() for a in atoms]
        t = Turtle3D()
        t.orient_from_backbone(*atoms, ORIENT_BACKBONE)
        t.move(3.0)
        for a, b in zip(atoms, before, strict=True):
            assert_allclose(a, b)

    def test_backbone_sidechain_conversions_set_the_flag_and_keep_the_frame_rigid(self):
        t = Turtle3D()
        t.bbone_to_schain()
        assert t.Orientation == ORIENT_SIDECHAIN
        assert_orthonormal(t)
        t.schain_to_bbone()
        assert t.Orientation == ORIENT_BACKBONE
        assert_orthonormal(t)


class TestTransforms:
    def test_local_global_round_trip(self):
        t = Turtle3D()
        t.turn(33.0)
        t.pitch(-20.0)
        t.roll(71.0)
        t.move(4.0)

        point = np.array([2.0, -1.0, 0.5])
        assert_allclose(t.to_global(t.to_local(point)), point, atol=_tolerance)

    def test_local_coordinates_of_a_point_ahead(self):
        t = Turtle3D()
        t.turn(33.0)
        t.move(4.0)
        ahead = t.Position.get_array() + 2.0 * t.Heading.get_array()
        assert_allclose(t.to_local(ahead), [2, 0, 0], atol=_tolerance)

    def test_vector_variants_match_array_variants(self):
        t = Turtle3D()
        t.yaw(25.0)
        t.move(1.0)
        point = np.array([1.0, 2.0, 3.0])
        assert_allclose(t.to_localVec(point).get_array(), t.to_local(point))
        assert_allclose(t.to_globalVec(point).get_array(), t.to_global(point))


class TestParityWithTurtleND:
    def test_long_random_sequence_matches_turtlend(self):
        rng = np.random.default_rng(1990)
        t3, tn = Turtle3D(), TurtleND(3)
        for _ in range(200):
            op = rng.choice(["roll", "pitch", "yaw", "turn", "move"])
            value = float(rng.uniform(-180.0, 180.0))
            getattr(t3, op)(value)
            getattr(tn, op)(value)

        assert_allclose(t3.Position.get_array(), tn.position, atol=1e-7)
        assert_allclose(frame_of(t3), tn.frame, atol=1e-7)

        point = np.array([1.0, -2.0, 3.0])
        assert_allclose(t3.to_local(point), tn.to_local(point), atol=1e-7)
        assert_allclose(t3.to_global(point), tn.to_global(point), atol=1e-7)
