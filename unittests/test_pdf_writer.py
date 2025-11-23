import os
import pytest

from scheduler_config_editor.model import PdfWriter, PdfMode
from scheduler_config_editor.model.schedule_handler import CourseMeeting


def test_convert_to_timestr():
    assert PdfWriter._convert_to_timestr(0) == "12:00 AM"
    assert PdfWriter._convert_to_timestr(60) == "1:00 AM"
    assert PdfWriter._convert_to_timestr(12 * 60) == "12:00 PM"
    assert PdfWriter._convert_to_timestr(13 * 60 + 5) == "1:05 PM"
    assert PdfWriter._convert_to_timestr(23 * 60 + 59) == "11:59 PM"


def test_hex_to_color():
    c = PdfWriter._hex_to_color("#3366CC")
    # verify RGB conversion
    assert pytest.approx(c.red, rel=1e-3) == 0x33 / 255
    assert pytest.approx(c.green, rel=1e-3) == 0x66 / 255
    assert pytest.approx(c.blue, rel=1e-3) == 0xCC / 255


def make_fake_schedule():
    """Creates a simple schedule with deterministic CourseMeeting objects."""
    cm1 = CourseMeeting(
        name="Math",
        faculty="Prof A",
        room="R101",
        time=(480, 540),  # 8:00–9:00
    )
    cm2 = CourseMeeting(
        name="CS",
        faculty="Prof B",
        room="Lab1",
        time=(600, 660),  # 10:00–11:00
    )

    # week = list of 5 days, each day is list of CourseMeeting
    week = [
        [cm1],  # Monday
        [cm2],  # Tuesday
        [],
        [],
        [],  # Wed/Thu/Fri empty
    ]

    return [("TestPage", week)]


def test_export_pdf_faculty():
    schedule = make_fake_schedule()

    output_path = "pdf/test_faculty.pdf"
    if os.path.exists(output_path):
        os.remove(output_path)

    PdfWriter.export_pdf(schedule, "test_faculty", PdfMode.FACULTY)

    assert os.path.exists(output_path)
    os.remove(output_path)


def test_export_pdf_room():
    schedule = make_fake_schedule()

    output_path = "pdf/test_room.pdf"
    if os.path.exists(output_path):
        os.remove(output_path)

    PdfWriter.export_pdf(schedule, "test_room", PdfMode.ROOM)

    assert os.path.exists(output_path)
    os.remove(output_path)
