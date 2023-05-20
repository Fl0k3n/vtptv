from configurer.utils.DeviceConsolePortManager import DeviceConsolePortManager


class DeviceEnabledMode:
    def __init__(self, console: DeviceConsolePortManager) -> None:
        self.console = console

    def __enter__(self) -> None:
        self.console.write("\n")
        self.console.write("enable")

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.console.write("exit")


class DeviceConfigMode:
    def __init__(self, console: DeviceConsolePortManager) -> None:
        self.console = console

    def __enter__(self) -> None:
        self.console.write("configure terminal")

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.console.write("exit")
