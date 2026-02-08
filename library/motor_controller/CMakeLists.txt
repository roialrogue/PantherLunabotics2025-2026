cmake_minimum_required(VERSION 3.10)
project(motor_controller VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. SET PATHS
set(SPARKCAN_DIR "${CMAKE_CURRENT_SOURCE_DIR}/sparkcan")

# 2. FIND PYTHON AND PYBIND11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# 3. DEFINE THE MODULE
# Create Python module from MotorControler.cpp
pybind11_add_module(motor_controller
    MotorControler.cpp
    ${SPARKCAN_DIR}/src/SparkBase.cpp
    ${SPARKCAN_DIR}/src/SparkMax.cpp
    ${SPARKCAN_DIR}/src/SparkFlex.cpp
)

# 4. INCLUDE DIRECTORIES
target_include_directories(motor_controller PRIVATE
    ${SPARKCAN_DIR}/include
)

# 5. LINK SYSTEM DEPENDENCIES
# The Jetson needs pthread to handle the CAN heartbeats
target_link_libraries(motor_controller PRIVATE pthread)

# 6. SET OUTPUT PROPERTIES
# Remove the 'lib' prefix and set the output name
set_target_properties(motor_controller PROPERTIES
    PREFIX ""
    OUTPUT_NAME "motor_controller"
)
