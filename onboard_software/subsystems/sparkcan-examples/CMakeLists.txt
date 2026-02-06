cmake_minimum_required(VERSION 3.10)
project(sparkcan-examples VERSION 1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find the sparkcan package
find_package(sparkcan REQUIRED)

# 2. Find pybind11 (Required for the Python module)
# This requires 'pip install pybind11' to be run on your system first
find_package(pybind11 REQUIRED)

# Define the executables and link with the sparkcan library
add_executable(example_control src/control.cpp)
add_executable(example_status src/status.cpp)

# --- New Python Binding ---
# Assuming your code with the 'run_motor' function is in src/motor_control.cpp
pybind11_add_module(motor_lib src/motor_control.cpp)

# Link the python module to sparkcan
target_link_libraries(motor_lib PRIVATE ${sparkcan_LIBRARIES})

target_link_libraries(example_control PRIVATE ${sparkcan_LIBRARIES})
target_link_libraries(example_status PRIVATE ${sparkcan_LIBRARIES})