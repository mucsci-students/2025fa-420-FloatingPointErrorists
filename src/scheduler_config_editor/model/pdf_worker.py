import pickle
import sys
from PyQt6.QtWidgets import QApplication
from scheduler_config_editor.model.pdf_writer import PdfWriter


def main():
    """Worker process to generate a PDF from a schedule."""
    data = pickle.loads(sys.stdin.buffer.read())
    schedule = data["schedule"]
    output_path = data["output_path"]
    mode = data["mode"]
    # Must create a QApplication instance for Qt to work properly
    _app = QApplication([])
    PdfWriter._export_graph_pdf_direct(schedule, output_path, mode)
    # explicit exit so Qt cleans up
    sys.exit(0)


if __name__ == "__main__":
    main()
