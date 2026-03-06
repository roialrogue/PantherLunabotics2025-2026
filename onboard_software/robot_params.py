# RobotParams
# Stores all constants and configs used across the robot codebase.

import time

# Global timer instance to be initialized by robot.py on startup
robot_timer = None

class RobotConfig:
    useDrivetrain = True
    useAuger = True

class LoopConfig:
    UPDATE_RATE_HZ = 50  # Change this to adjust loop frequency
    UPDATE_PERIOD_S = 1.0 / UPDATE_RATE_HZ  # 0.02s at 50Hz

class RobotTimer:
    def __init__(self):
        self._start_time = None

    def start(self):
        self._start_time = time.monotonic()

    def elapsed(self):
        if self._start_time is None:
            return 0.0
        return time.monotonic() - self._start_time

    def timestamp(self):
        e = self.elapsed()
        minutes = int(e) // 60
        seconds = e % 60
        return f"[T+{minutes:02d}:{seconds:05.2f}]"