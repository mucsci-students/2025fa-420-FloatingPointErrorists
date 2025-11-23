import unittest
from unittest.mock import patch
import copy

from scheduler_config_editor.model.json_config import (
    JsonConfig,
)  # change this to where JsonConfig actually lives


# ----------------------------------------------------------------------
# Dummy minimal stand-in classes because the real scheduler models
# are too complex and unnecessary for undo/redo tests.
# ----------------------------------------------------------------------
class DummySchedulerConfig:
    def __init__(self, val):
        self.val = val


class DummyTimeSlotConfig:
    def __init__(self, val):
        self.val = val


class DummyCombinedConfig:
    """Minimal object with .config and .time_slot_config attributes."""

    def __init__(self, a, b):
        self.config = DummySchedulerConfig(a)
        self.time_slot_config = DummyTimeSlotConfig(b)

    def __eq__(self, other):
        return (
            isinstance(other, DummyCombinedConfig)
            and self.config.val == other.config.val
            and self.time_slot_config.val == other.time_slot_config.val
        )

    def clone(self):
        return DummyCombinedConfig(self.config.val, self.time_slot_config.val)


# ----------------------------------------------------------------------
# Actual test cases for undo/redo.
# ----------------------------------------------------------------------
class TestUndoRedo(unittest.TestCase):
    def setUp(self):
        patcher1 = patch("scheduler_config_editor.model.json_config.os.makedirs")
        patcher2 = patch(
            "scheduler_config_editor.model.json_config.load_config_from_file",
            return_value=DummyCombinedConfig(1, 2),
        )

        self.mock_makedirs = patcher1.start()
        self.mock_load = patcher2.start()

        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)

        self.cfg = JsonConfig("test_config.json")

    # -----------------------------------------------------------
    # add_to_undo_stack behavior
    # -----------------------------------------------------------
    def test_add_to_undo_stack_pushes_deepcopy(self):
        original = copy.deepcopy(self.cfg._combined_config)

        self.cfg.add_to_undo_stack()

        self.assertEqual(self.cfg.get_undo_stack_size(), 1)
        stored = self.cfg._JsonConfig__undo_stack[0]

        self.assertEqual(stored, original)
        self.assertIsNot(
            stored,
            original,
            "Undo stack must store a deep copy, not the same object.",
        )

        # redo stack must be cleared
        self.assertEqual(self.cfg.get_redo_stack_size(), 0)

    # -----------------------------------------------------------
    # undo behavior
    # -----------------------------------------------------------
    def test_undo_raises_when_empty(self):
        with self.assertRaises(IndexError):
            self.cfg.undo()

    def test_undo_restores_previous_state(self):
        self.cfg.add_to_undo_stack()

        # Change current config
        self.cfg._combined_config = DummyCombinedConfig(99, 100)

        self.cfg.undo()

        # Should match the original loaded config
        self.assertEqual(self.cfg._combined_config, DummyCombinedConfig(1, 2))
        self.assertEqual(self.cfg.get_undo_stack_size(), 0)
        self.assertEqual(self.cfg.get_redo_stack_size(), 1)

    # -----------------------------------------------------------
    # redo behavior
    # -----------------------------------------------------------
    def test_redo_raises_when_empty(self):
        with self.assertRaises(IndexError):
            self.cfg.redo()

    def test_redo_restores_next_state(self):
        # Save old state
        self.cfg.add_to_undo_stack()

        # Modify config
        self.cfg._combined_config = DummyCombinedConfig(99, 100)

        # Undo (=> redo contains (99,100))
        self.cfg.undo()

        # Redo (=> restore forward state)
        self.cfg.redo()

        self.assertEqual(self.cfg._combined_config, DummyCombinedConfig(99, 100))
        self.assertEqual(self.cfg.get_redo_stack_size(), 0)
        self.assertEqual(self.cfg.get_undo_stack_size(), 1)

    # -----------------------------------------------------------
    # redo stack should clear after new edits
    # -----------------------------------------------------------
    def test_redo_clears_after_new_change(self):
        self.cfg.add_to_undo_stack()
        self.cfg._combined_config = DummyCombinedConfig(50, 60)

        # Undo → redo now has one entry
        self.cfg.undo()
        self.assertEqual(self.cfg.get_redo_stack_size(), 1)

        # New change → redo wiped
        self.cfg.add_to_undo_stack()
        self.assertEqual(self.cfg.get_redo_stack_size(), 0)

    # -----------------------------------------------------------
    # clear_stacks
    # -----------------------------------------------------------
    def test_clear_stacks(self):
        self.cfg.add_to_undo_stack()
        self.cfg._combined_config = DummyCombinedConfig(3, 4)
        self.cfg.undo()

        self.cfg.clear_stacks()

        self.assertEqual(self.cfg.get_undo_stack_size(), 0)
        self.assertEqual(self.cfg.get_redo_stack_size(), 0)
