from cpp.build import simulation

# Input data
time = 3
dt = 0.01
dx = 0.1
a = 110
# One dm rod with 100 and 0 temperature at the end
initial_conditions = [100.0] + [0.0] * 100 + [0.0]

results = simulation.simulation_init(initial_conditions, time, dt, dx, a)
print(results)
