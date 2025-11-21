import os

import pytest
from scheduler.config import TimeBlock, Meeting, ClassPattern

from scheduler_config_editor.model import TimeSlot, JsonConfig

@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))

class TestTimeSlot:
    def test_add_time_slot(self, json_config: JsonConfig):
        old_length = len(json_config.time_slot_config.items)
        test_times = {"MON": [TimeBlock(start= "09:00", spacing= 15, end= "10:00"),
                         TimeBlock(start= "12:00", spacing= 20, end= "15:00")],
                 "TUE": [TimeBlock(start= "13:10", spacing= 10, end= "14:25")]}
        test_classes = [ClassPattern(credits= 3, meetings= [Meeting(day= "MON", duration= 50, lab= False)], disabled= False,
                   start_time= "09:00")]

        result = TimeSlot.add_time_slot(
            json_config=json_config,
            times=test_times,
            classes=test_classes
        )

        assert result == "Time slot added successfully."
        assert len(json_config.time_slot_config.items) == old_length + 1

        new_time_slot = json_config.time_slot_config.items[old_length]
        assert new_time_slot.times == test_times
        assert new_time_slot.classes == test_classes
        assert new_time_slot.max_time_gap == 30
        assert new_time_slot.min_time_overlap == 45