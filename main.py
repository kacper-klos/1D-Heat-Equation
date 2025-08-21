from cpp.build import simulation
import numpy as np
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent = None):
        self.fig = Figure(figsize = (6, 4), dpi = 100)
        super().__init__(self.fig)
        self.setParent(parent)

        self.ax = self.fig.add_subplot(111)
        self._im = None
        self._cbar = None

    def plot_heatmap(self, results, dx, time):
        # Clears and plots the heat map
        self.ax.clear()
        self._im = self.ax.imshow(
            results, 
            aspect = "auto", 
            origin = "lower",
            extent = [0, results.shape[1] * dx, 0, time],
            cmap = "inferno",
        )
        # Define color bar
        if self._cbar is not None:
            self._cbar.remove()
        self._cbar = self.fig.colorbar(self._im, ax = self.ax, fraction = 0.046, pad = 0.04)
        self._cbar.set_label(label = r"Temperature [$^\circ C$]")
        # Describe labels
        self.ax.set_xlabel("Space [$m$]")
        self.ax.set_ylabel("Time [$s$]")
        self.ax.set_title("1D Temperature Distribution over Time")

        self.draw_idle()

    def update_heatmap(self, results, dx, time):
        # If there is no image got to main ploting function
        if self._im is None:
            return self.plot_heatmap(results, dx, time)
        # Set new data
        self._im.set_data(results)
        self._im.set_extent([0, results.shape[1] * dx, 0, time])
        self._im.autoscale()
        # Update color bar
        if self._cbar is not None:
            self._cbar.update_normal(self._im)

        self.draw_idle()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("1D Heat Simulation")
        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        self.canvas = MplCanvas(self)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)


        # Input data
        time = 25
        dt = 0.001
        dx = 1
        a = 110
        # One dm rod with 100 and 0 temperature at the end
        initial_conditions = [100.0] + [0.0] * 100 + [0.0]

        results = np.array(simulation.simulation_init(initial_conditions, time, dt, dx, a))
        self.canvas.plot_heatmap(results, dx, time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(900, 600)
    w.show()
    sys.exit(app.exec())

