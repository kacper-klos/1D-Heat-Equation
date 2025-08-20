from cpp.build import simulation
import numpy as np
import matplotlib.pyplot as plt

# Input data
time = 25
dt = 0.001
dx = 1
a = 110
# One dm rod with 100 and 0 temperature at the end
initial_conditions = [100.0] + [0.0] * 100 + [0.0]

results = np.array(simulation.simulation_init(initial_conditions, time, dt, dx, a))

# Generate heat map
plt.imshow(results, aspect = "auto", origin = "lower",
           extent = [0, results.shape[1] * dx, 0, time],
           cmap = "inferno")

# Describtion of a graph
plt.colorbar(label = r"Temperature [$^\circ C$]")
plt.xlabel("Space [$m$]")
plt.ylabel("Time [$s$]")
plt.title("1D Temperature Distribution over Time")

plt.show()
