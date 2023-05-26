import time

import serial

from configurer.consoleutils.DeviceConsolePortManager import (
    DeviceConsolePortManager, TimeoutException)


class SerialDeviceConsolePort(DeviceConsolePortManager):
    _COMMAND_PROMPT_CHAR = "#"
    _ENTER_COMMAND_CHAR = "\r"
    _CONSOLE_ENCODING = "utf-8"

    def __init__(self, device_path: str, baud_rate: str, command_read_timeout_s: float = 5) -> None:
        super().__init__()
        self.device_path = device_path
        self.baud_rate = baud_rate
        self.command_read_timeout_s = command_read_timeout_s

        self._serial_conn = None
        self._last_write_timestamp_s = None
        self._was_initially_open = None

    def __enter__(self) -> "DeviceConsolePortManager":
        if self._serial_conn is None:
            self._serial_conn = serial.Serial(
                port=self.device_path,
                baudrate=self.baud_rate,
                timeout=self.command_read_timeout_s,
                parity="N",
                bytesize=8,
                stopbits=1
            )

            if self._was_initially_open is None:
                self._was_initially_open = self._serial_conn.is_open

            if not self._serial_conn.is_open:
                self._serial_conn.open()
            else:
                self._serial_conn.reset_input_buffer()
                self._serial_conn.reset_output_buffer()

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._serial_conn is not None:
            if self._was_initially_open:
                self._serial_conn.close()
            self._serial_conn = None

    def write(self, command: str) -> None:
        command_to_send = command + self._ENTER_COMMAND_CHAR
        self._serial_conn.write(command_to_send.encode(self._CONSOLE_ENCODING))

    def write_and_get_output(self, command: str, timeout_s: float = 10) -> str:
        self.flush_input()
        self.write(command)

        output_buff = ""
        start_timestamp = time.time()
        echo_removed = False

        while True:
            output_buff += self._serial_conn.read(
                max(self._serial_conn.in_waiting, 1)).decode(self._CONSOLE_ENCODING)

            if not echo_removed:
                echo_removed, output_buff = self._try_removing_echo_and_old_output(
                    command, output_buff)

            if echo_removed and self._is_output_ready(output_buff):
                break

            if time.time() - start_timestamp > timeout_s:
                raise TimeoutException(command, output_buff)

        return self._clear_command_output(output_buff)

    def flush_input(self) -> None:
        self._serial_conn.reset_input_buffer()

    def _is_output_ready(self, output_buff: str) -> bool:
        return output_buff.count(self._COMMAND_PROMPT_CHAR) >= 1

    def _try_removing_echo_and_old_output(self, command: str, output_buff: str) -> tuple[bool, str]:
        stripped_cmd = command.strip()
        command_echo_idx = output_buff.find(stripped_cmd)
        if command_echo_idx == -1:
            return False, output_buff
        return True, output_buff[command_echo_idx + len(stripped_cmd):]

    def _clear_command_output(self, output_buff: str) -> str:
        def valid_line_predicate(line: str):
            return not self._COMMAND_PROMPT_CHAR in line and len(line.strip()) > 0

        return "\n".join([line for line in output_buff.splitlines() if valid_line_predicate(line)])
