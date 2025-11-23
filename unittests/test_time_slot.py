import os

import pytest
from scheduler.config import TimeBlock, Meeting, ClassPattern

from scheduler_config_editor.model import JsonConfig, TimeSlot

@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))

class TestTimeSlot:
    def test_add_time_block(self, json_config: JsonConfig):
        old_length = len(json_config.time_slot_config.times.get("MON"))
        test = TimeBlock(start= "09:00", spacing= 5, end= "10:00")
        result = TimeSlot.add_time_block(
            day_index= 1,
            json_config= json_config,
            start= "09:00",
            spacing= 5,
            end= "10:00"
        )

        assert result == "Time block added successfully."
        assert len(json_config.time_slot_config.times.get("MON")) == old_length + 1
        new_time_block= json_config.time_slot_config.times.get("MON")[old_length]
        assert new_time_block.start == test.start
        assert new_time_block.end == test.end
        assert new_time_block.spacing == test.spacing

    def test_add_class_pattern(self, json_config: JsonConfig):
        old_length = len(json_config.time_slot_config.classes)
        test = ClassPattern(credits= 3, meetings= [Meeting(day="MON", start_time="09:00", duration=60, lab=False)], disabled= False, start_time= "09:00")
        result = TimeSlot.add_class_pattern(
            json_config=json_config,
            creds=3,
            meetings= [Meeting(day="MON", start_time="09:00", duration=60, lab=False)],
            disabled= False,
            start_time= "09:00"
        )

        assert result == "Class pattern added successfully."
        assert len(json_config.time_slot_config.classes) == old_length + 1
        new_class_pattern = json_config.time_slot_config.classes[old_length]
        assert new_class_pattern.credits == test.credits
        assert new_class_pattern.meetings == test.meetings
        assert new_class_pattern.disabled == test.disabled
        assert new_class_pattern.start_time == test.start_time

    def test_mod_time_block(self, json_config: JsonConfig):
        index = len(json_config.time_slot_config.times.get("MON")) - 1
        test = TimeBlock(start= "10:00", spacing= 10, end= "15:00")
        result = TimeSlot.mod_time_block(
            index= index,
            day_index=1,
            json_config=json_config,
            start="10:00",
            spacing=10,
            end="15:00"
        )
        assert result == "Time block updated successfully."
        modified_time_block = json_config.time_slot_config.times.get("MON")[index]
        assert modified_time_block.start == test.start
        assert modified_time_block.end == test.end
        assert modified_time_block.spacing == test.spacing

    def test_mod_class_pattern(self, json_config: JsonConfig):
        index = len(json_config.time_slot_config.classes) - 1
        test = ClassPattern(credits= 4, meetings= [Meeting(day="TUE", start_time="11:00", duration=75, lab=True)], disabled= True, start_time= "12:00")
        result = TimeSlot.mod_class_pattern(
            index= index,
            json_config=json_config,
            creds=4,
            meetings= [Meeting(day="TUE", start_time="11:00", duration=75, lab=True)],
            disabled= True,
            start_time= "12:00"
        )

        assert result == "Class pattern updated successfully."
        modified_class_pattern = json_config.time_slot_config.classes[index]
        assert modified_class_pattern.credits == test.credits
        assert modified_class_pattern.meetings == test.meetings
        assert modified_class_pattern.disabled == test.disabled
        assert modified_class_pattern.start_time == test.start_time

    def test_del_time_block(self, json_config: JsonConfig):
        old_length = len(json_config.time_slot_config.times.get("MON"))
        result = TimeSlot.del_time_block(json_config,1, old_length - 1)
        assert result == "Time block deleted successfully."
        assert len(json_config.time_slot_config.times.get("MON")) == old_length - 1

    def test_del_class_pattern(self, json_config: JsonConfig):
        old_length = len(json_config.time_slot_config.classes)
        result = TimeSlot.del_class_pattern(json_config, old_length - 1)
        assert result == "Class pattern deleted successfully."
        assert len(json_config.time_slot_config.classes) == old_length - 1