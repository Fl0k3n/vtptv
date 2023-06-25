# Virtual To Physical To Virtual

Project created for the Future Internet Technologies course. Docs (in Polish) can be found at [docs_pl.pdf](./docs_pl.pdf).

The goal of this project is to convert the configuration of a virtual (Kathara project) topology with various networking protocols running to the same working topology with the same protocols but on physical Cisco devices, and vice versa.

## Installation

In `src` directory run: `pip install -r requirements.txt`

Kathara is installed alongside as a Python library, refer to [their installation guide](https://github.com/KatharaFramework/Kathara/wiki/Installation-Guides) if CLI is needed.

## Requirements:

- Python>=3.10
- Physical devices must support Netconf protocol with yang models.

## Running

Modify `src/.env` file according to your needs, you will most likely need to change:
- `VIRT_TO_PHY_INITIAL_PATH` - path to Kathara lab with configuration of virtual network
- `PHY_TO_VIRT_RESULT_PATH`  - path where configuration of physical network should be saved as a Kathara lab
- `SERIAL_DEVICE_PATH`       - path (Linux) or name (Windows) of serial device that will be connected to console ports of devices
- `SERIAL_BAUD_RATE`         - baud rate of that device
- `NETCONF_NETWORK_IP`       - if topology (either virtual or physical) contains such network change it to something else


In `src` directory run for usage details:

`python vtptv.py --help`


For running Kathara refer to their [docs](https://github.com/KatharaFramework/Kathara/wiki) or [tutorial](https://github.com/KatharaFramework/Kathara-Labs/blob/master/001-kathara-introduction.pdf), if you don't need CLI you can also use `python utils/labrunner.py <lab path>`.


