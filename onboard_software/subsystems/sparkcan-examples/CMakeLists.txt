cmake_minimum_required(VERSION 3.10)
project(sparkcan-examples VERSION 1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. Find the sparkcan package
find_package(sparkcan REQUIRED)

# 2. MANUALLY SET PYBIND11 PATHS (Bypassing find_package)
# These paths come directly from your 'python3 -m pybind11 --includes' output
set(PYBIND_INC_ENV "/home/luna01/Lunabotics/PantherLunabotics2025-2026/lunaenv/lib/python3.10/site-packages/pybind11/include")
set(PYTHON_INC_ENV "/usr/local/python3.10/include/python3.10")

# --- Original Executables ---
add_executable(example_control src/control.cpp)
add_executable(example_status src/status.cpp)
target_link_libraries(example_control PRIVATE ${sparkcan_LIBRARIES})
target_link_libraries(example_status PRIVATE ${sparkcan_LIBRARIES})

# --- New Python Binding ---
# We use 'add_library' with MODULE type since pybind11_add_module might 
# fail if find_package(pybind11) failed.
add_library(motor_lib MODULE src/motor_control.cpp)

# This makes it a .so file without the "lib" prefix, which Python requires
set_target_properties(motor_lib PROPERTIES PREFIX "" OUTPUT_NAME "motor_lib")

# FORCE the compiler to use your lunaenv headers
target_include_directories(motor_lib PRIVATE 
    ${PYBIND_INC_ENV} 
    ${PYTHON_INC_ENV}
)

# Link the python module to sparkcan
target_link_libraries(motor_lib PRIVATE ${sparkcan_LIBRARIES})