from abc import ABC, abstractmethod
from typing import Callable


class DeviceConsolePortManager(ABC):

    @abstractmethod
    def write(self, data: str) -> None:
        pass

    @abstractmethod
    def read(self) -> str:
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

    def write_failable(self, data: str,
                       success_predicate: Callable[[str], bool] = lambda resp: 'invalid' not in resp.lower()) -> bool:
        self.flush_input()
        self.write(data)
        resp = self.read()
        return success_predicate(resp)
