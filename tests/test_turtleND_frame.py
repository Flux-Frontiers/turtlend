"""Tests for the TurtleND frame operations that the original suite does not reach:
orient, expand_dim, orient_toward, orient_in_time, the tape and the accessors."""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from turtlend import TurtleND

_tolerance = 1e-10


def assert_orthonormal(turtle: TurtleND) -> None:
    frame = turtle.frame
    assert_allclose(frame @ frame.T, np.eye(turtle.ndim), atol=_tolerance)


class TestOrient:
    def test_orient_sets_position_and_heading(self):
        t = TurtleND(5)
        position = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        heading = position + np.array([0.0, 2.0, 0.0, 0.0, 0.0])
        left = position + np.array([3.0, 1.0, 0.0, 0.0, 0.0])
        t.orient(position, heading, left)

        assert_allclose(t.position, position)
        assert_allclose(t.heading, [0, 1, 0, 0, 0], atol=_tolerance)
        # left is the input with its heading component removed
        assert_allclose(t.left, [1, 0, 0, 0, 0], atol=_tolerance)
        assert_orthonormal(t)

    def test_orient_when_heading_is_a_later_standard_axis(self):
        # heading = e2 makes the k=2 Gram-Schmidt seed vanish, which takes the
        # fallback search over the other standard basis vectors.
        t = TurtleND(3)
        t.orient([0, 0, 0], [0, 0, 1], [0, 1, 0])
        assert_allclose(t.heading, [0, 0, 1], atol=_tolerance)
        assert_allclose(t.left, [0, 1, 0], atol=_tolerance)
        assert_orthonormal(t)


class TestExpandDim:
    def test_expand_dim_returns_new_axis_and_pads(self):
        t = TurtleND(3)
        t.turn(30.0)
        t.move(2.0)
        old_position = t.position
        old_frame = t.frame

        axis = t.expand_dim(label="time")

        assert axis == 3
        assert t.ndim == 4
        assert_allclose(t.position, [*old_position, 0.0])
        assert_allclose(t.frame[:3, :3], old_frame)
        assert_allclose(t.basis(3), [0, 0, 0, 1])
        assert_orthonormal(t)

    def test_expanded_turtle_can_move_along_new_axis(self):
        t = TurtleND(2)
        axis = t.expand_dim()
        t.rotate(90.0, 0, axis)
        t.move(1.0)
        assert_allclose(np.abs(t.position), [0, 0, 1], atol=_tolerance)


class TestOrientToward:
    def test_orient_toward_standard_axis(self):
        t = TurtleND(4)
        angle = t.orient_toward([0, 0, 1, 0])
        assert angle == pytest.approx(90.0)
        assert_allclose(t.heading, [0, 0, 1, 0], atol=_tolerance)
        assert_orthonormal(t)

    def test_orient_toward_arbitrary_direction(self):
        t = TurtleND(6)
        direction = np.array([1.0, -2.0, 0.5, 3.0, -1.0, 0.25])
        t.orient_toward(direction)
        assert_allclose(t.heading, direction / np.linalg.norm(direction), atol=1e-8)
        assert_orthonormal(t)

    def test_orient_toward_ignores_magnitude(self):
        a, b = TurtleND(3), TurtleND(3)
        a.orient_toward([0, 5, 0])
        b.orient_toward([0, 0.01, 0])
        assert_allclose(a.heading, b.heading, atol=_tolerance)

    def test_zero_direction_is_a_no_op(self):
        t = TurtleND(3)
        assert t.orient_toward([0, 0, 0]) == 0.0
        assert_allclose(t.frame, np.eye(3))

    @pytest.mark.parametrize("direction", [[2, 0, 0], [-2, 0, 0]])
    def test_parallel_and_antiparallel_are_no_ops(self, direction):
        t = TurtleND(3)
        assert t.orient_toward(direction) == 0.0
        assert_allclose(t.frame, np.eye(3))


class TestOrientInTime:
    def test_defaults_to_negative_last_axis(self):
        t = TurtleND(3)
        t.expand_dim(label="time")
        angle = t.orient_in_time()
        assert angle == pytest.approx(90.0)
        assert_allclose(t.heading, [0, 0, 0, -1], atol=_tolerance)

    def test_explicit_time_axis(self):
        t = TurtleND(4)
        t.orient_in_time(time_axis=1)
        assert_allclose(t.heading, [0, -1, 0, 0], atol=_tolerance)


class TestTape:
    def test_tape_records_only_while_recording(self):
        t = TurtleND(3)
        t.move(1.0)
        assert t.tape == []

        t.recording = True
        assert t.recording is True
        t.move(1.0)
        t.move(1.0)
        assert_allclose(t.tape, [[2, 0, 0], [3, 0, 0]])

    def test_tape_is_a_copy(self):
        t = TurtleND(3)
        t.recording = True
        t.move(1.0)
        t.tape.clear()
        assert len(t.tape) == 1

    def test_reset_tape_clears_and_stops_recording(self):
        t = TurtleND(3)
        t.recording = True
        t.move(1.0)
        t.reset_tape()
        assert t.tape == []
        assert t.recording is False


class TestAccessors:
    def test_name(self):
        t = TurtleND(3, name="walker")
        assert t.name == "walker"
        t.name = "flyer"
        assert t.name == "flyer"

    def test_pen(self):
        t = TurtleND(3)
        assert t.pen == "up"
        t.pen = "down"
        assert t.pen == "down"
        t.pen = "up"
        assert t.pen == "up"

    def test_position_setter(self):
        t = TurtleND(4)
        t.position = [1, 2, 3, 4]
        assert_allclose(t.position, [1, 2, 3, 4])

    def test_position_setter_rejects_wrong_shape(self):
        t = TurtleND(4)
        with pytest.raises(ValueError):
            t.position = [1, 2, 3]

    def test_basis_rejects_out_of_range_index(self):
        t = TurtleND(3)
        with pytest.raises(IndexError):
            t.basis(3)

    def test_accessors_return_copies(self):
        t = TurtleND(3)
        t.position[0] = 99.0
        t.heading[0] = 99.0
        t.frame[0, 0] = 99.0
        assert_allclose(t.position, [0, 0, 0])
        assert_allclose(t.frame, np.eye(3))

    def test_pitch_requires_three_dimensions(self):
        with pytest.raises(ValueError):
            TurtleND(2).pitch(10.0)

    def test_repr_names_the_turtle_and_dimension(self):
        text = repr(TurtleND(4, name="walker"))
        assert "walker" in text
        assert "4D" in text
