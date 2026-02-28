# Start Up commands

## Start up the robot power up

sudo ip link set can0 type can bitrate 1000000 restart-ms 100

```bash
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

## Start venv on onboard server

```bash
source lunaenv/bin/activate
```

## TODO:

