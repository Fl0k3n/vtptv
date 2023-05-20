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


if __name__ == '__main__':
    for i in range(33):
        print(convert_to_dot_notation(i))
