def dot_notation_to_decimal(dotted: str) -> int:
    return sum(int(byte) * (256 ** (3 - i)) for i, byte in enumerate(dotted.split('.')))


def mask_size_to_decimal(mask: int) -> int:
    return sum((1 << i) for i in range((32 - mask), 32))


def decimal_to_dot_notation(dec: int) -> str:
    parts = []
    for i in range(4):
        parts.append(str(dec % 256))
        dec //= 256
    return '.'.join(reversed(parts))


def netmask_to_dot_notation(netmask: int) -> str:
    full_ones = netmask // 8
    full_zeros = 4 - full_ones
    parts = ['255' for _ in range(full_ones)]

    remaining_ones = netmask % 8
    if remaining_ones > 0:
        full_zeros -= 1
        partial_submask = sum(2 ** (7 - i) for i in range(remaining_ones))
        parts.append(str(partial_submask))

    parts.extend(['0' for _ in range(full_zeros)])

    return '.'.join(parts)


def is_in_same_subnet(ipv4_1: str, netmask1: int, ipv4_2: str, netmask2: int) -> bool:
    mask = mask_size_to_decimal(min(netmask1, netmask2))
    ip1 = dot_notation_to_decimal(ipv4_1)
    ip2 = dot_notation_to_decimal(ipv4_2)
    return ((ip1 & mask) ^ (ip2 & mask)) == 0


def get_subnet(ipv4: str, netmask: int) -> str:
    return decimal_to_dot_notation(
        dot_notation_to_decimal(ipv4) & mask_size_to_decimal(netmask))


def netmask_from_dot_notation(netmask: str) -> int:
    decimal_mask = dot_notation_to_decimal(netmask)
    return sum((decimal_mask & (1 << i)) >> i for i in range(32))
