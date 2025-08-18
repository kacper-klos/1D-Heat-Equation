import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from matplotlib.figure import Figure

class SimulationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("1D Heat Simulation")

        # Central widget
        central = QWidget(self)
        self.setCentralWidget(central)

        # Matplot figure
        self.figure = Figure(figsize = (6,4), dpi = 100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Button
        self.button = QPushButton("Simulate")

        # Layout
        layout = QVBoxLayout(central)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SimulationWindow()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())
