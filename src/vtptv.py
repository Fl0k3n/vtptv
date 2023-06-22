import logging

import click
from dotenv import dotenv_values

from configurer.consoleutils.SerialDeviceConsolePortManager import \
    SerialDeviceConsolePort
from configurer.DeviceConfigurer import DeviceConfigurer
from configurer.DeviceInitializer import DeviceInitializer
from configurer.hints.hints import ConfigurationHintsExtractor
from configurer.netconfutils.NetconfManager import NetconfManager
from configurer.VirtualConfigurer import VirtualConfigurer
from PhysicalToVirtualConverter import PhysicalToVirtualConverter
from utils.TopologyVisualizer import TopologyVisualizer
from VirtualToPhysicalConverter import VirtualToPhysicalConverter

DOTENV_FILE_NAME = ".env"


def init_config():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    return dotenv_values(DOTENV_FILE_NAME)


def init_device_initializer(config) -> DeviceInitializer:
    serial_console_port_mgr = SerialDeviceConsolePort(
        config['SERIAL_DEVICE_PATH'],
        int(config['SERIAL_BAUD_RATE']),
        float(config['SERIAL_TIMEOUT_SECONDS'])
    )

    return DeviceInitializer(
        serial_console_port_mgr, config['SSH_LOGIN'], config['SSH_PASS'])


@click.command('vtp', help="convert virtual configuration to physical")
def virtual_to_physical():
    config = init_config()

    device_initializer = init_device_initializer(config)
    netconf_mgr = NetconfManager(config['SSH_LOGIN'], config['SSH_PASS'])
    device_configurer = DeviceConfigurer(netconf_mgr)

    converter = VirtualToPhysicalConverter(
        config['LAB_PATH'], device_initializer, device_configurer)

    converter.convert()


@click.command('ptv', help="convert physical configuration to virtual, command expectes "
                           "number of ROUTERS and SWITCHES in physical topology")
@click.argument('routers', default=False, type=int)
@click.argument('switches', default=False, type=int)
def physical_to_virtual(routers: int, switches: int):
    config = init_config()

    device_initializer = init_device_initializer(config)
    netconf_mgr = NetconfManager(config['SSH_LOGIN'], config['SSH_PASS'])
    hints_extractor = ConfigurationHintsExtractor()
    configurer = VirtualConfigurer(netconf_mgr, hints_extractor)

    converter = PhysicalToVirtualConverter(device_initializer, configurer)

    topo = converter.convert(routers_count=routers, switches_count=switches)

    TopologyVisualizer().visualize(topo)


@click.command('visualize', help="visualize virtual topology graph")
def visualize_virtual():
    config = init_config()
    converter = VirtualToPhysicalConverter(config['LAB'], None, None)
    topo = converter.convert(configure_devices=False)

    TopologyVisualizer().visualize(topo)


@click.group(help="Create .env file as described in Readme, then choose conversion direction, "
                  "or just visualize virtual topology without configuring anything.")
def cli():
    pass


if __name__ == '__main__':
    cli.add_command(virtual_to_physical)
    cli.add_command(physical_to_virtual)
    cli.add_command(visualize_virtual)
    cli()
