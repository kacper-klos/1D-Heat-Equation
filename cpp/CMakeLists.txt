cmake_minimum_required(VERSION 3.16)
project(simulation_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(simulation
    binding.cpp
    heat_equation.cpp
)

target_compile_options(simulation PRIVATE -O3 -Wall -Wextra)
