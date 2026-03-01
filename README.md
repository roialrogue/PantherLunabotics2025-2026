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

Phase 1:
1. Just run the robot and generally verify everything is working
2. Test new motor directions
3. Slove drive math

4. Clean up client server code 

Phase 2:
1. Figure out all the required sensor for auto and how to use all of them 

