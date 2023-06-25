from dataclasses import dataclass, field
from typing import Tuple, Union


@dataclass
class RedistributeConfig:
    connected: bool = False
    static: bool = False


@dataclass
class RIPTimers:
    update: int
    timeout: int
    garbage: int


@dataclass
class RIPConfig:
    redistribute: RedistributeConfig = field(
        default_factory=RedistributeConfig)
    version: int = 2
    enabled_interfaces: list[str] = field(default_factory=list)
    enabled_networks: list[Tuple[str, int]] = field(default_factory=list)
    neighbors: list[str] = field(default_factory=list)
    timers: Union[RIPTimers, None] = None


@dataclass
class OspfNetworkInfo:
    ipv4: str
    netmask: int
    area: str


@dataclass
class OSPFConfig:
    redistribute: RedistributeConfig = field(
        default_factory=RedistributeConfig)
    router_id: str = None
    enabled_networks: list[OspfNetworkInfo] = field(default_factory=list)
