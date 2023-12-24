import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPixmap, QImage
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
        self.label_coordinates.setAlignment(Qt.AlignCenter)  # Use the Qt.AlignCenter enumeration

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.view)
        layout.addWidget(self.label_coordinates)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.view)
        self.origin = None

        self.view.mousePressEvent = self.mouse_press_event
        self.view.mouseMoveEvent = self.mouse_move_event
        self.view.mouseReleaseEvent = self.mouse_release_event

        self.load_pdf()

    def load_pdf(self):
        for page in self.pdf.pages:
            image = page.to_image()
            pil_image = image.original
            q_image = QImage(pil_image.tobytes("raw", "RGB"), pil_image.width, pil_image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            item = self.scene.addPixmap(pixmap)
            item.setPos(0, 0)

    def mouse_press_event(self, event):
        self.origin = event.pos()
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

    def mouse_move_event(self, event):
        if self.origin:
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouse_release_event(self, event):
        if self.origin:
            x0, y0 = self.origin.x(), self.origin.y()
            x1, y1 = event.pos().x(), event.pos().y()

            # Adjust the coordinates based on the position of the QGraphicsView
            x0, y0 = self.view.mapToScene(QPoint(x0, y0)).toPoint().x(), self.view.mapToScene(QPoint(x0, y0)).toPoint().y()
            x1, y1 = self.view.mapToScene(QPoint(x1, y1)).toPoint().x(), self.view.mapToScene(QPoint(x1, y1)).toPoint().y()

            # Adjust the coordinates as needed
            self.label_coordinates.setText(f"Coordinates: ({min(x0, x1)}, {min(y0, y1)}, {max(x0, x1)}, {max(y0, y1)})")

            self.origin = None
            self.rubber_band.setGeometry(QRect().normalized())  # Hide the rubber band

    def closeEvent(self, event):
        if self.pdf:
            self.pdf.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pdf_path = "input/12-18.pdf"  # Replace with the actual path to your PDF file
    window = PDFSelector(pdf_path)
    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec_())
