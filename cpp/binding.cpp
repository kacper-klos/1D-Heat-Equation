#include <pybind11/pybind11.h>
#include "heat_equation.h"

PYBIND11_MODULE(simulation, module) {
    module.doc() = "1D heat equation simulation in C++";
    module.def("heat_equation", &simulation_init, "Simulation of 1D heat equation");
}
