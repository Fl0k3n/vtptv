def convert_to_dot_notation(netmask: int) -> str:
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


def network_contains(network_ip: str, network_mask: int, ip: str, mask: int = 32) -> bool:
    network_ip = network_ip.split('.')
    network_mask = [255 for _ in range(network_mask // 8)] + [256 - 2 ** (
        8 - network_mask % 8)] + [0 for _ in range(3 - network_mask // 8)]
    ip = ip.split('.')
    mask = [255 for _ in range(mask // 8)] + [256 - 2 **
                                              (8 - mask % 8)] + [0 for _ in range(3 - mask // 8)]
    for network_byte, network_mask_byte, ip_byte, mask_byte in zip(network_ip, network_mask, ip, mask):
        if int(network_byte) & int(network_mask_byte) != (int(ip_byte) & int(mask_byte)) & int(network_mask_byte):
            return False
    return True


def get_wildcard_mask(prefix_mask: int) -> str:
    wildcard_mask = (1 << 32) - 1
    wildcard_mask = wildcard_mask ^ ((1 << (32 - prefix_mask)) - 1)
    return ".".join([str((wildcard_mask >> (8 * i)) & 255) for i in range(3, -1, -1)])


if __name__ == '__main__':
    for i in range(33):
        print(convert_to_dot_notation(i))
