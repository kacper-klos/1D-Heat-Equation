# 1D-Heat-Equation

A simple 1D heat-equation solver with a C++ core (performance) exposed to Python via **pybind11** and a **Python GUI** for visualization.

![Temperature graph](/images/temperature_graph.png)
![GUI 1](/images/simulation_1.png)
![GUI 2](/images/simulation_2.png)

## Build

Requirements: C++17 compiler, CMake, Python 3.x, pybind11 (via CMake or your package manager).

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
````

> **Import note (Python):** ensure Python can see the compiled extension (e.g., `simulation*.so`).
>
> * Easiest: run from the repo root and add the build dir to `PYTHONPATH`:
>
>   ```bash
>   export PYTHONPATH="$PWD/build${PYTHONPATH:+:$PYTHONPATH}"
>   ```
> * Or configure CMake to place/copy the module next to `main.py`.

## Run

If you use **uv**:

```bash
uv run python main.py
```

(Plain Python works too: create/activate a venv, install deps, then `python main.py`.)

## How it works

Starting from energy conservation and Fourier’s law,

$$
Q = mc\Delta T, \qquad \frac{Q}{\Delta t} = -k A \frac{\Delta T}{\Delta x},
$$

you arrive at the 1D heat equation

$$
\frac{\partial T}{\partial t} = \alpha\frac{\partial^2 T}{\partial x^2}, \qquad \alpha=\frac{k}{\rho c}\ \text{(thermal diffusivity)}.
$$

We use an explicit FTCS (Forward-Time, Centered-Space) finite-difference scheme:

$$
T_i^{j+1} = T_i^{j} + r\left(T_{i+1}^{j} - 2T_i^{j} + T_{i-1}^{j}\right), \qquad r=\frac{\alpha\Delta t}{\Delta x^{2}}.
$$

Here, $i$ indexes space (slice) and $j$ indexes time step (frame).

### Stability

For the explicit scheme in 1D, choose $\Delta t$ and $\Delta x$ so that

$$
r=\frac{\alpha\Delta t}{\Delta x^{2}} \le \tfrac{1}{2}.
$$

## Parameters

* $t$: times of simulation
* $l$: length of the rod
* $\alpha$: thermal diffusivity
* $\Delta t$: time step
* $\Delta x$: spatial step
* boundary & initial conditions: temperatures at both ends of the rod, set in the Python GUI / config

## Notes

* GUI uses Python (e.g., PyQt/Matplotlib). If you’re on WSL or Wayland and see Qt platform plugin errors, ensure the proper X/Wayland libraries are installed or set a compatible backend.
* Images above are in `/images/`.

