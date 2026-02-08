#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <memory>

#include "SparkMax.hpp"

namespace py = pybind11;

// Feedback structure with all three output data types
struct MotorFeedback 
{
    float dutyCycle;     // Percentage of max output (-1.0 to 1.0)
    float velocity;      // RPM
    float position;      // ticks
};

// Configuration structure for motor initialization
struct MotorConfig 
{
    IdleMode idleMode = IdleMode::kBrake;
    MotorType motorType = MotorType::kBrushless;
    SensorType sensorType = SensorType::kHallSensor;
    float rampRate = 0.1;
    bool inverted = false;
    int motorKv = 565;                  // NEO Vortex default
    int encoderCountsPerRev = 7168;     // NEO Vortex default
    float smartCurrentFreeLimit = 20.0;
    float smartCurrentStallLimit = 20.0;
};

class MotorController 
{
private:
    std::string canbus;
    std::map<int, SparkMax> connectedMotors;
    std::map<int, float> dutyCycles;
    std::map<int, MotorFeedback> motorFeedback;

    // Private constructor for singleton
    MotorController(std::string canbus_name) : canbus(canbus_name) {}

    // Delete copy constructor and assignment operator
    MotorController(const MotorController&) = delete;
    MotorController& operator=(const MotorController&) = delete;

public:
    // Get the singleton instance
    static MotorController& GetInstance(const std::string& canbus_name = "can0") 
    {
        static MotorController instance(canbus_name);

        // Verify that the same canbus is being used
        if (instance.canbus != canbus_name) 
        {
            throw std::runtime_error("MotorController already initialized with CAN bus '" +
                                   instance.canbus + "'. Cannot change to '" + canbus_name + "'.");
        }

        return instance;
    }

    // Get the current CAN bus name
    std::string GetCanBusName() const 
    {
        return canbus;
    }

    // Initialize a motor with custom configuration
    void InitializeMotor(int motor_ID, const MotorConfig& config) 
    {
        // Check if motor is already initialized
        if (connectedMotors.find(motor_ID) != connectedMotors.end()) 
        {
            std::cerr << "Warning: Motor ID " << motor_ID << " is already initialized." << std::endl;
            return;
        }

        // Create new motor object
        connectedMotors.emplace(std::piecewise_construct,
                                std::forward_as_tuple(motor_ID),
                                std::forward_as_tuple(canbus, motor_ID));

        // Configure the motor
        SparkMax& motor = connectedMotors.at(motor_ID);
        motor.SetIdleMode(config.idleMode);
        motor.SetMotorType(config.motorType);
        motor.SetSensorType(config.sensorType);
        motor.SetRampRate(config.rampRate);
        motor.SetInverted(config.inverted);
        motor.SetMotorKv(config.motorKv);
        motor.SetEncoderCountsPerRev(config.encoderCountsPerRev);
        motor.SetSmartCurrentFreeLimit(config.smartCurrentFreeLimit);
        motor.SetSmartCurrentStallLimit(config.smartCurrentStallLimit);
        motor.BurnFlash();

        // Initialize desired duty cycle and feedback to 0
        dutyCycles[motor_ID] = 0.0f;
        motorFeedback[motor_ID] = MotorFeedback{0.0f, 0.0f, 0.0f};
    }

    // Initialize multiple motors with the same configuration
    void InitializeMotors(const std::vector<int>& motor_IDs, const MotorConfig& config) 
    {
        for (int motor_ID : motor_IDs) 
        {
            InitializeMotor(motor_ID, config);
        }
    }

    // Get list of initialized motor IDs
    std::vector<int> GetInitializedMotorIDs() const 
    {
        std::vector<int> ids;
        ids.reserve(connectedMotors.size());
        for (const auto& pair : connectedMotors) 
        {
            ids.push_back(pair.first);
        }
        return ids;
    }

    // Get number of initialized motors
    size_t GetMotorCount() const 
    {
        return connectedMotors.size();
    }

    // Update all motors: send commands and collect feedback (call this in main loop)
    void Update() 
    {
        for (auto& pair : connectedMotors) 
        {
            int motor_ID = pair.first;
            SparkMax& motor = pair.second;

            // Get desired duty cycle (0 if not set)
            float dutyCycle = GetCurrentDutyCycle(motor_ID);

            // Send heartbeat and set duty cycle
            motor.Heartbeat();
            motor.SetDutyCycle(dutyCycle);

            // Collect and cache feedback
            MotorFeedback data;
            data.dutyCycle = motor.GetDutyCycle();
            data.velocity = motor.GetVelocity();
            data.position = motor.GetPosition();

            motorFeedback[motor_ID] = data;
        }
    }

    // Set desired duty cycle for a single motor
    void SetMotorDutyCycle(int motor_ID, float dutyCycle) 
    {
        if (connectedMotors.find(motor_ID) == connectedMotors.end()) 
        {
            throw std::runtime_error("Motor ID " + std::to_string(motor_ID) + " is not initialized.");
        }

        dutyCycles[motor_ID] = dutyCycle;
    }

    // Set desired duty cycles for multiple motors
    void SetMotorsDutyCycles(const std::vector<int>& motor_IDs, const std::vector<float>& dutyCycles) 
    {
        if (motor_IDs.size() != dutyCycles.size()) 
        {
            throw std::invalid_argument("Number of duty cycles does not match the number of motor IDs.");
        }

        for (size_t i = 0; i < motor_IDs.size(); ++i) 
        {
            SetMotorDutyCycle(motor_IDs[i], dutyCycles[i]);
        }
    }

    // Get the desired duty cycle for a motor
    float GetCurrentDutyCycle(int motor_ID) const 
    {
    auto it = dutyCycles.find(motor_ID);
    if (it != dutyCycles.end()) 
    {
        return it->second;
    }
    return 0.0f;  // Default if not found
    }

    // Get feedback for a single motor
    MotorFeedback GetMotorFeedback(int motor_ID) const 
    {
        if (connectedMotors.find(motor_ID) == connectedMotors.end()) 
        {
            throw std::runtime_error("Motor ID " + std::to_string(motor_ID) + " is not initialized.");
        }

        // Return cached feedback data
        auto it = motorFeedback.find(motor_ID);
        return it->second;
    }

    // Get all feedback for all initialized motors
    std::map<int, MotorFeedback>& GetAllFeedback() const 
    {
        return motorFeedback;
    }
};


// PYBIND11 BINDINGS
PYBIND11_MODULE(motor_controller, m) 
{
    m.doc() = "Motor controller module for managing SPARK MAX motor controllers";

    // Bind IdleMode enum
    py::enum_<IdleMode>(m, "IdleMode")
        .value("COAST", IdleMode::kCoast)
        .value("BRAKE", IdleMode::kBrake)
        .export_values();

    // Bind MotorType enum
    py::enum_<MotorType>(m, "MotorType")
        .value("BRUSHED", MotorType::kBrushed)
        .value("BRUSHLESS", MotorType::kBrushless)
        .export_values();

    // Bind SensorType enum
    py::enum_<SensorType>(m, "SensorType")
        .value("NO_SENSOR", SensorType::kNoSensor)
        .value("HALL_SENSOR", SensorType::kHallSensor)
        .export_values();

    // Bind MotorFeedback structure
    py::class_<MotorFeedback>(m, "MotorFeedback")
        .def(py::init<>())
        .def_readwrite("duty_cycle", &MotorFeedback::dutyCycle)
        .def_readwrite("velocity", &MotorFeedback::velocity)
        .def_readwrite("position", &MotorFeedback::position)
        .def("__repr__", [](const MotorFeedback &fb) {
            return "MotorFeedback(duty_cycle=" + std::to_string(fb.dutyCycle) +
                   ", velocity=" + std::to_string(fb.velocity) + " RPM" +
                   ", position=" + std::to_string(fb.position) + " ticks)";
        });

    // Bind MotorConfig structure
    py::class_<MotorConfig>(m, "MotorConfig")
        .def(py::init<>())
        .def_readwrite("idle_mode", &MotorConfig::idleMode)
        .def_readwrite("motor_type", &MotorConfig::motorType)
        .def_readwrite("sensor_type", &MotorConfig::sensorType)
        .def_readwrite("ramp_rate", &MotorConfig::rampRate)
        .def_readwrite("inverted", &MotorConfig::inverted)
        .def_readwrite("motor_kv", &MotorConfig::motorKv)
        .def_readwrite("encoder_counts_per_rev", &MotorConfig::encoderCountsPerRev)
        .def_readwrite("smart_current_free_limit", &MotorConfig::smartCurrentFreeLimit)
        .def_readwrite("smart_current_stall_limit", &MotorConfig::smartCurrentStallLimit);

    // Bind MotorController class (singleton)
    py::class_<MotorController>(m, "MotorController")
        .def_static("get_instance", &MotorController::GetInstance,
                    py::arg("canbus_name") = "can0",
                    py::return_value_policy::reference,
                    "Get the singleton instance of MotorController")
        .def("get_canbus_name", &MotorController::GetCanBusName,
             "Get the CAN bus name this controller is using")
        .def("initialize_motor", &MotorController::InitializeMotor,
             py::arg("motor_id"), py::arg("config"),
             "Initialize a motor with custom configuration")
        .def("initialize_motors", &MotorController::InitializeMotors,
             py::arg("motor_ids"), py::arg("config"),
             "Initialize multiple motors with the same configuration")
        .def("get_motor_feedback", &MotorController::GetMotorFeedback,
             py::arg("motor_id"),
             "Get feedback for a single motor")
        .def("get_all_feedback", &MotorController::GetAllFeedback,
             "Get feedback for all initialized motors")
        .def("get_initialized_motor_ids", &MotorController::GetInitializedMotorIDs,
             "Get list of initialized motor IDs")
        .def("get_motor_count", &MotorController::GetMotorCount,
             "Get number of initialized motors")
        .def("set_motor_duty_cycle", &MotorController::SetMotorDutyCycle,
             py::arg("motor_id"), py::arg("duty_cycle"),
             "Set desired duty cycle for a motor (doesn't send immediately)")
        .def("set_motors_duty_cycles", &MotorController::SetMotorsDutyCycles,
             py::arg("motor_ids"), py::arg("duty_cycles"),
             "Set desired duty cycles for multiple motors (doesn't send immediately)")
        .def("get_current_duty_cycle", &MotorController::GetCurrentDutyCycle,
             py::arg("motor_id"),
             "Get the current duty cycle for a motor")
        .def("update", &MotorController::Update,
             "Process all motors: send commands and collect feedback (call in main loop)");
}
