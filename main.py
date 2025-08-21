from cpp.build import simulation
import numpy as np
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFormLayout, QDoubleSpinBox, QLabel
)
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

    def plot_heatmap(self, results: np.ndarray, dx: float, time: float):
        """ Plot heatmap of temparature over time.

        Args:
            results: 2D numpy array with frames of simulation.
            dx: Size of one node.
            time: Time of simulation
        """

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

    def update_heatmap(self, results: np.ndarray, dx: float, time: float):
        """ Update heatmap after it was already ploted.

        Args:
            results: 2D numpy array with frames of simulation.
            dx: Size of one node.
            time: Time of simulation
        """

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
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        control_panel = QWidget()
        control_layout = QFormLayout(control_panel)
        # Time field
        self.time_field = QDoubleSpinBox()
        self.time_field.setRange(1.0, 1000.0)
        self.time_field.setValue(25.0)
        # Length field
        self.length_field = QDoubleSpinBox()
        self.length_field.setRange(0.01, 10000.0)
        self.length_field.setDecimals(2)
        self.length_field.setValue(100)
        # a constant field
        self.a_field = QDoubleSpinBox()
        self.a_field.setRange(10, 5000)
        self.a_field.setValue(110)
        # dt field
        self.dt_field = QDoubleSpinBox()
        self.dt_field.setRange(1e-8, 1.0)
        self.dt_field.setDecimals(8)
        self.dt_field.setValue(0.001)
        # dx field
        self.dx_field = QDoubleSpinBox()
        self.dx_field.setRange(1e-4, 1.0)
        self.dx_field.setDecimals(4)
        self.dx_field.setValue(1.0)
        # Start temp
        self.left_temp_field = QDoubleSpinBox()
        self.left_temp_field.setRange(-273.16, 3000.0)
        self.left_temp_field.setValue(100.0)
        self.right_temp_field = QDoubleSpinBox()
        self.right_temp_field.setRange(-273.16, 3000.0)
        self.right_temp_field.setValue(100.0)
        # Temperature layout
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.left_temp_field)
        temp_layout.addWidget(self.right_temp_field)
        # Start button
        self.run_button = QPushButton("simulate")
        self.run_button.clicked.connect(self.run_simulation)
        # Set control panel
        control_layout.addRow(QLabel("<b>Simulation Parameters<b>"))
        control_layout.addRow("t [s]:", self.time_field)
        control_layout.addRow("l [m]:", self.length_field)
        control_layout.addRow("a [m^2/s]:", self.a_field)
        control_layout.addRow("dt [s]:", self.dt_field)
        control_layout.addRow("dx [m]:", self.dx_field)
        control_layout.addRow("T [°C]:", temp_layout)
        control_layout.addRow(self.run_button)

        main_layout.addWidget(control_panel)

        matplot_panel = QWidget()
        matplot_layout = QVBoxLayout(matplot_panel)

        self.canvas = MplCanvas(self)
        matplot_layout.addWidget(NavigationToolbar(self.canvas, self))
        matplot_layout.addWidget(self.canvas)

        main_layout.addWidget(matplot_panel)

        self.run_simulation()

    def run_simulation(self):
        """ Runs simulation with the data from the fields. """
        nodes = int(self.length_field.value() / self.dx_field.value())
        initial_conditions = [self.left_temp_field.value()] + [0.0] * nodes + [self.right_temp_field.value()]

        results = np.array(simulation.simulation_init(
            initial_conditions,
            self.time_field.value(),
            self.dt_field.value(),
            self.dx_field.value(),
            self.a_field.value()
        ))
        self.canvas.update_heatmap(results, self.dx_field.value(), self.time_field.value())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(900, 600)
    w.show()
    sys.exit(app.exec())

