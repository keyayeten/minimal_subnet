import ipaddress


def ip_to_int(ipv4_address: str, v6=False) -> int:
    if v6:
        return int(ipaddress.IPv6Address(ipv4_address))
    return int(ipaddress.IPv4Address(ipv4_address))


def xnor_bits_of_ips(list_test: list, v6=False) -> int:
    mask_init = (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                 if v6 else 0XFFFFFFFF)
    temp_intersection_bits = (mask_init
                              & ~(ip_to_int(list_test[0], v6)
                                  ^ ip_to_int(list_test[1], v6)))
    for i in range(2, len(list_test)):
        temp_intersection_bits = (temp_intersection_bits
                                  & ~(ip_to_int(list_test[i], v6)
                                      ^ ip_to_int(list_test[i - 1], v6)))
    return temp_intersection_bits


def count_prefix_bits(bits: int, v6=False) -> int:
    mask, counter, full = ((0x80000000000000000000000000000000, 0, 128)
                           if v6 else (0X80000000, 0, 32))
    for index in range(full):
        if (mask & bits) != 0:
            counter += 1
        else:
            break
        mask >>= 1
    return counter


def ip_to_bin(ip_address, v6=False):
    if v6:
        return bin(int(ipaddress.IPv6Address(ip_address)))[2:]
    return bin(int(ipaddress.IPv4Address(ip_address)))[2:]


def bin_to_ip(binary_str, v6=False):
    full, parts = (128, 16) if v6 else (32, 8)
    padded_binary = binary_str.zfill(full)
    groups = [padded_binary[i:i+parts] for i in range(0, full, parts)]
    if v6:
        hex_groups = [hex(int(group, 2))[2:] for group in groups]
        return ":".join(hex_groups)
    decimal_groups = [str(int(group, 2)) for group in groups]
    return ".".join(decimal_groups)


def get_solution(ip_addresses, v6=False):
    result = xnor_bits_of_ips(ip_addresses, v6)
    prefix_bits = count_prefix_bits(result, v6)
    temp = ip_to_bin(ip_addresses[0], v6)[:prefix_bits]
    if v6:
        prefix = ipaddress.IPv6Address(bin_to_ip(f"{temp:<0128}", v6))
        return f"{prefix}/{prefix_bits}"
    prefix = ipaddress.IPv4Address(bin_to_ip(f"{temp:<032}"))
    return f"{prefix}/{prefix_bits}"


# Пример использования:
ip_addresses_v4 = ['192.168.1.1',
                   '192.168.1.3',
                   '192.168.1.5']
print(get_solution(ip_addresses_v4))

ip_addresses_v6 = ["ffe0::1:0:0:0",
                   "ffe0::2:0:0:0",
                   "ffe0::4:0:0:0",
                   "ffe0::8:0:0:0",
                   "ffe0::10:0:0:0",
                   "ffe0::20:0:0:0",
                   "ffe0::40:0:0:0",
                   "ffe0::80:0:0:0"]
print(get_solution(ip_addresses_v6, True))
