import time

import serial

from configurer.utils.DeviceConsolePortManager import DeviceConsolePortManager


class SerialDeviceConsolePort(DeviceConsolePortManager):
    def __init__(self, device_path: str, baud_rate: str, wait_before_read_time_s: float) -> None:
        super().__init__()
        self.device_path = device_path
        self.baud_rate = baud_rate
        self.wait_before_read_time_s = wait_before_read_time_s

        self._serial_conn = None
        self._last_write_timestamp_s = None

    def __enter__(self) -> "DeviceConsolePortManager":
        if self._serial_conn is None:
            self._serial_conn = serial.Serial(self.device_path, self.baud_rate)
            self._update_last_write_timestamp()
            self._serial_conn.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._serial_conn is not None:
            self._serial_conn.close()
            self._serial_conn = None

    def write(self, data: str) -> None:
        command_to_send = data + "\r"
        self._serial_conn.write(command_to_send.encode('utf-8'))
        self._update_last_write_timestamp()

    def read(self) -> str:
        self._assert_waited_before_reading()
        return self._serial_conn.read(self._serial_conn.in_waiting).decode('utf-8')

    def flush_input(self) -> None:
        self._assert_waited_before_reading()
        self._serial_conn.reset_input_buffer()

    def _update_last_write_timestamp(self):
        self._last_write_timestamp_s = time.time()

    def _assert_waited_before_reading(self):
        delta = time.time() - self._last_write_timestamp_s
        if delta < self.wait_before_read_time_s:
            time.sleep(delta)
