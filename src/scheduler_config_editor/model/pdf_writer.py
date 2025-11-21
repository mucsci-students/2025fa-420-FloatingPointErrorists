from typing import List, Tuple
from scheduler_config_editor.model.schedule_handler import CourseMeeting
from xhtml2pdf import pisa


class PdfWriter:
    """
    A class responsible for writing room/faculty schedules to PDF
    using HTML + CSS (Google Calendar-like layout).
    """

    HOURS = list(range(8, 23))  # 8 to 22 inclusive
    DAYS = ["MON", "TUE", "WED", "THU", "FRI"]

    @staticmethod
    def _generate_html_page(name: str, week: List[List[CourseMeeting]]) -> str:
        """
        Generate HTML for one page of a schedule.
        `week` is a list of 5 lists (one per day), each containing CourseMeeting objects.
        """
        html = f"""
        <html>
        <head>
        <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
        h2 {{ text-align: center; margin: 10px; }}
        .calendar {{ display: table; width: 100%; border-collapse: collapse; }}
        .day-column {{ display: table-cell; border: 1px solid #999; vertical-align: top; width: 20%; }}
        .hour {{ height: 50px; border-top: 1px solid #ccc; position: relative; }}
        .class-block {{
            position: absolute;
            left: 0;
            right: 0;
            padding: 2px;
            color: white;
            font-size: 10px;
            border-radius: 3px;
        }}
        </style>
        </head>
        <body>
        <h2>{name}</h2>
        <div class="calendar">
        """
        colors = [
            "#e74c3c", "#3498db", "#f1c40f", "#9b59b6", "#2ecc71",
            "#e67e22", "#fd79a8", "#1abc9c", "#95a5a6", "#34495e",
            "#16a085", "#c0392b"
        ]
        class_color_map = {}

        for day_idx, day in enumerate(week):
            html += f'<div class="day-column"><strong>{PdfWriter.DAYS[day_idx]}</strong>'
            for course in day:
                # Determine color for this course
                if course.name not in class_color_map:
                    class_color_map[course.name] = colors[len(class_color_map) % len(colors)]
                color = class_color_map[course.name]

                # Compute position & height
                start_hour = course.time[0] / 60
                end_hour = course.time[1] / 60
                top_percent = ((start_hour - PdfWriter.HOURS[0]) / (PdfWriter.HOURS[-1] - PdfWriter.HOURS[0])) * 100
                height_percent = ((end_hour - start_hour) / (PdfWriter.HOURS[-1] - PdfWriter.HOURS[0])) * 100

                html += f"""
                <div class="class-block" style="top:{top_percent}%; height:{height_percent}%; background-color:{color};">
                    {course.name}<br>{course.faculty if course.room else course.room}<br>
                </div>
                """
            html += "</div>"  # end day-column

        html += "</div></body></html>"
        return html

    @staticmethod
    def _save_pdf(html: str, output_path: str) -> None:
        """Convert HTML string to PDF and save to output_path."""
        with open(output_path, "wb") as f:
            pisa.CreatePDF(src=html, dest=f)

    @staticmethod
    def export_room_schedule(schedule: List[Tuple[str, List[List[CourseMeeting]]]], output_path: str) -> None:
        """Export room schedule to multi-page PDF (one page per room)."""
        combined_html = ""
        for room, week in schedule:
            combined_html += PdfWriter._generate_html_page(room, week) + "<div style='page-break-after: always;'></div>"
        PdfWriter._save_pdf(combined_html, output_path)

    @staticmethod
    def export_faculty_schedule(schedule: List[Tuple[str, List[List[CourseMeeting]]]], output_path: str) -> None:
        """Export faculty schedule to multi-page PDF (one page per faculty)."""
        combined_html = ""
        for faculty, week in schedule:
            combined_html += PdfWriter._generate_html_page(faculty, week) + "<div style='page-break-after: always;'></div>"
        PdfWriter._save_pdf(combined_html, output_path)
