import logging

from dotenv import dotenv_values

from configurer.DeviceInitializer import DeviceInitializer
from configurer.utils.SerialDeviceConsolePortManager import \
    SerialDeviceConsolePort
from utils.TopologyVisualizer import TopologyVisualizer
from VirtualToPhysicalConverter import VirtualToPhysicalConverter

DOTENV_FILE_NAME = ".env"


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    config = dotenv_values(DOTENV_FILE_NAME)

    serial_console_port_mgr = SerialDeviceConsolePort(
        config['SERIAL_DEVICE_PATH'],
        int(config['SERIAL_BAUD_RATE']),
        float(config['SERIAL_WAIT_BEFORE_READ_SECONDS'])
    )

    device_initializer = DeviceInitializer(
        serial_console_port_mgr, "cisco", "testing")

    converter = VirtualToPhysicalConverter(
        config['LAB_PATH'], device_initializer)

    topo = converter.convert()

    TopologyVisualizer().visualize(topo)


if __name__ == '__main__':
    main()
