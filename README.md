# Start Up commands

## SSH into onboard rPi

```bash
ssh rmcnasa@100.76.221.110
```

## Start venv on onboard server

```bash
source lunaenv/bin/activate
```

## Start up the robot power up

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 txqueuelen 1000
sudo ip link set can0 up
python robot.py
```

## Restart the robot after power up

```bash
python robot.py
```

## Start mission control on laptop

```bash
python control.py
```

# TODO:

# Phase 1: TeleOp/Gen:
1. Fix joysticks stick drift and check driveing with joysticks
2. Setup new jetson
3. Setup vision streaming for camera and Lidar throught ssh

5. Clean up client server code (Do we need telemetry)

# Phase 2: Auto/Automations:
1. Figure out all the required sensor for auto and how to use all of them

- How do we track x, y, and heading? 
- How do we localize them at the start of the match how do we localize mid match if position drifts?
(Sam and Nico might need to be in for this conversation)
