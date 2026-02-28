import os
import datetime


class TelemetryLogger:
    """
    Reusable telemetry file logger for robot subsystems.

    Usage:
        logger = TelemetryLogger("auger")
        logger.start_logging(["Velocity (RPM)", "Current (A)"])
        logger.log_row("[T+00:01.00]", [120.4, 2.1])
        logger.stop_logging()

    Output is a markdown table suitable for spreadsheet import.
    """

    def __init__(self, name: str, log_dir: str = None):
        """
        name:    subsystem label used in the filename and header (e.g. "auger")
        log_dir: directory to write log files into; defaults to
                 <this file's location>/../../logs/  (i.e. onboard_software/logs/)
        """
        self.name = name
        if log_dir is None:
            self.log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        else:
            self.log_dir = log_dir

        self._file = None
        self._filepath = None
        self._row_count = 0

    @property
    def is_logging(self) -> bool:
        return self._file is not None

    def start_logging(self, columns: list):
        """
        Open a new log file and write the markdown table header.

        columns: ordered list of column header strings, e.g.
                 ["Duty Cycle", "Velocity (RPM)", "Position (ticks)"]
                 A "Timestamp" column is always prepended automatically.
        """
        if self._file is not None:
            return  # already logging

        os.makedirs(self.log_dir, exist_ok=True)

        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        file_tag = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.name}_{file_tag}.md"
        self._filepath = os.path.join(self.log_dir, filename)

        self._file = open(self._filepath, 'w', encoding='utf-8')
        self._row_count = 0

        all_columns = ["Timestamp"] + columns
        header_row = "| " + " | ".join(all_columns) + " |"
        sep_row = "|" + "|".join(
            ":---------:" if i > 0 else "-----------"
            for i in range(len(all_columns))
        ) + "|"

        self._file.write(f"# {self.name.capitalize()} Telemetry Log\n")
        self._file.write(f"- Date: {date_str}\n")
        self._file.write(f"- Log file: {filename}\n")
        self._file.write("\n")
        self._file.write(header_row + "\n")
        self._file.write(sep_row + "\n")
        self._file.flush()

        print(f"[{self.name.capitalize()}] Logging started -> {self._filepath}")

    def log_row(self, timestamp: str, values: list):
        """
        Write one data row to the log table.

        timestamp: string from robot_params.robot_timer.timestamp()
        values:    list of raw numbers matching the column order from start_logging()
        """
        if self._file is None:
            return

        cells = [timestamp] + [str(v) for v in values]
        row = "| " + " | ".join(cells) + " |"
        self._file.write(row + "\n")
        self._file.flush()
        self._row_count += 1

    def stop_logging(self):
        """Finalize the log file and close it."""
        if self._file is None:
            return

        self._file.write(f"\n*Session ended — {self._row_count} rows recorded*\n")
        self._file.close()
        self._file = None

        print(f"[{self.name.capitalize()}] Logging stopped — {self._row_count} rows saved to {self._filepath}")
        self._filepath = None
        self._row_count = 0
