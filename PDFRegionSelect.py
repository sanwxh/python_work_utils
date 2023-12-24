import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QVBoxLayout, QWidget
import pdfplumber

class PDFSelector(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()

        self.pdf_path = pdf_path
        self.pdf = pdfplumber.open(pdf_path)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 800, 600)  # Adjust the scene rectangle as needed

        self.label_coordinates = QLabel("Coordinates: (0, 0, 0, 0)")
        self.label_coordinates.setAlignment(0x84)  # Align to center

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.view)
        layout.addWidget(self.label_coordinates)

        self.rect_item = None

        self.view.mousePressEvent = self.mouse_press_event

    def mouse_press_event(self, event):
        if self.rect_item:
            self.scene.removeItem(self.rect_item)

        x0 = int(event.scenePos().x())
        y0 = int(event.scenePos().y())
        x1 = x0 + 100  # Adjust the width of the rectangle as needed
        y1 = y0 + 100  # Adjust the height of the rectangle as needed

        self.rect_item = QGraphicsRectItem(x0, y0, x1 - x0, y1 - y0)
        self.scene.addItem(self.rect_item)

        self.label_coordinates.setText(f"Coordinates: ({x0}, {y0}, {x1}, {y1})")

    def closeEvent(self, event):
        if self.pdf:
            self.pdf.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pdf_path = "path/to/your/pdf_file.pdf"  # Replace with the actual path to your PDF file
    window = PDFSelector(pdf_path)
    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec_())
