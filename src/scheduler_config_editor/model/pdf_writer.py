import os
from enum import Enum
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from scheduler_config_editor.model import INDEX_TO_DAY
from scheduler_config_editor.model.schedule_handler import CourseMeeting


MINUTES_PER_HOUR = 60


class PdfMode(Enum):
    """Modes for exporting schedules to PDF."""

    FACULTY = "faculty"
    ROOM = "room"


class PdfWriter:
    """Class for exporting schedules to PDF files."""

    @staticmethod
    def _convert_to_timestr(minutes: int) -> str:
        """Convert total minutes to 'H:MM AM/PM'."""
        hour = minutes // MINUTES_PER_HOUR
        minute = minutes % MINUTES_PER_HOUR

        ampm = "AM" if hour < 12 else "PM"
        hour = hour % 12 or 12

        return f"{hour}:{minute:02d} {ampm}"

    @staticmethod
    def _hex_to_color(hex_code: str) -> colors.Color:
        """Convert '#RRGGBB' → ReportLab color."""
        hex_code = hex_code.lstrip("#")
        r = int(hex_code[0:2], 16) / 255
        g = int(hex_code[2:4], 16) / 255
        b = int(hex_code[4:6], 16) / 255
        return colors.Color(r, g, b)

    @staticmethod
    def export_pdf(
        schedule: list[tuple[str, list[list[CourseMeeting]]]], name: str, mode: PdfMode
    ) -> None:
        """Export the given schedule to a PDF file."""
        output_path = os.path.join("pdf", f"{name}.pdf")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        start_minutes = min(
            course.time[0] for _, week in schedule for day in week for course in day
        )
        end_minutes = max(
            course.time[1] for _, week in schedule for day in week for course in day
        )

        start_hour = start_minutes // MINUTES_PER_HOUR
        end_hour = (end_minutes + 59) // MINUTES_PER_HOUR
        total_hours = (end_minutes - start_minutes) / MINUTES_PER_HOUR

        margin = 0.5 * inch
        title_spacing = 0.3 * inch

        column_width = (width - 2 * margin) / 6  # time + 5 days
        row_height = (height - 2 * margin) / (total_hours + 3)

        title_y = height - margin
        header_y = title_y - title_spacing - row_height

        color_pairs = [
            ("#0066ff", "#ffffff"),
            ("#0052cc", "#ffffff"),
            ("#33adff", "#000000"),
            ("#005c99", "#ffffff"),
            ("#66a3ff", "#000000"),
            ("#002966", "#ffffff"),
            ("#99c2ff", "#000000"),
            ("#001433", "#ffffff"),
            ("#b3d1ff", "#000000"),
            ("#000000", "#ffffff"),
        ]

        for page_name, week in schedule:
            c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, title_y, page_name)

            c.setFont("Helvetica-Bold", 14)
            for i in range(1, 6):
                x = margin + column_width * i

                c.rect(x, header_y, column_width, row_height)
                c.drawCentredString(
                    x + column_width / 2, header_y + row_height / 2 - 6, INDEX_TO_DAY[i]
                )

            for hour in range(start_hour, end_hour + 1):
                y = header_y - row_height * (hour - start_hour + 1)
                c.rect(margin, y, column_width, row_height)
                c.drawString(
                    margin + 5,
                    y + row_height / 2 - 6,
                    PdfWriter._convert_to_timestr(hour * 60),
                )

            used_classes: list[str] = []
            text_font_size = 8 if total_hours <= 12 else 6
            text_line_step = 12 if total_hours <= 12 else 8

            for day_index, day in enumerate(week, start=1):
                x = margin + column_width * day_index

                for course in day:
                    if course.name not in used_classes:
                        used_classes.append(course.name)

                    bg_hex, fg_hex = color_pairs[used_classes.index(course.name)]
                    bg = PdfWriter._hex_to_color(bg_hex)
                    fg = PdfWriter._hex_to_color(fg_hex)

                    start, end = course.time
                    duration = end - start
                    start_offset = start - start_minutes

                    y = header_y - (start_offset / 60) * row_height
                    h = (duration / 60) * row_height

                    c.setFillColor(bg)
                    c.rect(x, y - h, column_width, h, fill=1, stroke=1)

                    c.setFillColor(fg)
                    c.setFont("Helvetica-Bold", text_font_size)

                    if mode == PdfMode.FACULTY:
                        lines = [
                            course.name,
                            course.room,
                        ]
                    else:
                        lines = [
                            course.name,
                            course.faculty,
                        ]

                    lines.append(
                        f"{PdfWriter._convert_to_timestr(start)} - "
                        f"{PdfWriter._convert_to_timestr(end)}"
                    )

                    text_y = y - text_line_step
                    for line in lines:
                        c.drawString(x + 5, text_y, line)
                        text_y -= text_line_step

            c.showPage()

        c.save()
