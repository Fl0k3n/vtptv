from abc import ABC, abstractmethod
from typing import Callable


class DeviceConsolePortManager(ABC):

    @abstractmethod
    def write(self, command: str) -> None:
        pass

    @abstractmethod
    def write_and_get_output(self, command: str) -> str:
        pass

    @abstractmethod
    def flush_input(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> "DeviceConsolePortManager":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

    def write_failable(self, command: str,
                       success_predicate: Callable[[str], bool] = lambda resp: 'invalid' not in resp.lower()) -> bool:
        return success_predicate(self.write_and_get_output(command))

    def write_newline(self) -> None:
        self.write("\n")


class TimeoutException(Exception):
    def __init__(self, input_command: str, output: str) -> None:
        super().__init__(
            f'Reading output of command: "{input_command.strip()}" timed out\ngot output: {output}')
