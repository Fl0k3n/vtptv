from dataclasses import dataclass


@dataclass
class SNat:
    original_src_ipv4: str
    target_src_ipv4: str

@dataclass
class DNat:
    original_dest_ipv4: str
    target_dest_ipv4: str

@dataclass
class OverloadNat:
    src_ipv4: str
    src_netmask: int
