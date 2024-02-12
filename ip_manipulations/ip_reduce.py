"""
A module that provides the ability to obtain different
representations of IP addresses (get_solution)
and the function of finding a minimum subnet(ip_to_int, ip_to_bin, bin_to_ip)
"""
import ipaddress


def ip_to_int(ip_adress: str, v6=False) -> int:
    """_summary_

    Args:
        ip_adress (str): classic representation of ip
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        int: representation of ip as int
    """
    if v6:
        return int(ipaddress.IPv6Address(ip_adress))
    return int(ipaddress.IPv4Address(ip_adress))


def xnor_bits_of_ips(ips_list: list[str], v6=False) -> int:
    """The function adds the bitwise representations
    of IP addresses from a list using the XNOR
    operation and returns the result as an integer.
    Uses the default mask_init to extract the raw
    bits starting from the first two IP addresses in the list

    Args:
        ips_list (list[str]): List with ip addresses
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        int: _description_
    """
    mask_init = (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                 if v6 else 0XFFFFFFFF)  # default mask
    temp_intersection_bits = (mask_init  # xnor with the first two addresses
                              & ~(ip_to_int(ips_list[0], v6)
                                  ^ ip_to_int(ips_list[1], v6)))
    for i in range(2, len(ips_list)):  # xnor with other addresses
        temp_intersection_bits = (temp_intersection_bits
                                  & ~(ip_to_int(ips_list[i], v6)
                                      ^ ip_to_int(ips_list[i - 1], v6)))
    return temp_intersection_bits


def count_prefix_bits(bits: int, v6=False) -> int:
    """Counting the number of bits representing
    minimum common IPv4/IPv6 subnet coverage

    Args:
        bits (int): an integer representing the bits to be analyzed.
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        int: number of significant bits
    """
    mask, counter, full = ((0x80000000000000000000000000000000, 0, 128)
                           if v6 else (0X80000000, 0, 32))
    for index in range(full):
        if (mask & bits) != 0:
            counter += 1
        else:
            break
        mask >>= 1
    return counter


def ip_to_bin(ip_address: str, v6=False) -> str:
    """Returns the binary representation of ip

    Args:
        ip_address (str): classic representation of ip
        (Example: 128.0.0.0 or ffe0::2:0:0:0)
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        str: binary representation of ip
    """
    if v6:
        return bin(int(ipaddress.IPv6Address(ip_address)))[2:].zfill(128)
    return bin(int(ipaddress.IPv4Address(ip_address)))[2:].zfill(32)


def bin_to_ip(binary_str: str, v6=False) -> str:
    """Returns the classic representation of ip by
    restoring it from binary notation

    Args:
        binary_str (str): binary representation of ip
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        str: classic representation of ip
    """
    full, parts = (128, 16) if v6 else (32, 8)
    padded_binary = binary_str.zfill(full)
    groups = [padded_binary[i:i+parts] for i in range(0, full, parts)]
    if v6:
        hex_groups = [hex(int(group, 2))[2:] for group in groups]
        return ":".join(hex_groups)
    decimal_groups = [str(int(group, 2)) for group in groups]
    return ".".join(decimal_groups)


def get_solution(ip_addresses: list[str], v6=False) -> str:
    """
    Returns the minimum subnet for a given list of IP addresses

    Args:
        ip_addresses (list[str]): list of ip-adress str's
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Returns:
        str: minimum subnet

    >>> get_solution(['10.168.1.1',
    ...                        '10.168.1.3',
    ...                        '10.168.1.5'])
    '10.168.1.0/29'

    >>> get_solution(["ffe0::1:0:0:0",
    ...                        "ffe0::2:0:0:0",
    ...                        "ffe0::4:0:0:0",
    ...                        "ffe0::8:0:0:0",
    ...                        "ffe0::10:0:0:0",
    ...                        "ffe0::20:0:0:0",
    ...                        "ffe0::40:0:0:0",
    ...                        "ffe0::80:0:0:0"], True)
    'ffe0::/72'
    """
    validate_adresses(ip_addresses, v6)
    if len(ip_addresses) == 1:
        return f"{ip_addresses[0]}/{128 if v6 else 32}"
    result = xnor_bits_of_ips(ip_addresses, v6)
    prefix_bits = count_prefix_bits(result, v6)
    temp = ip_to_bin(ip_addresses[0], v6)[:prefix_bits]
    if v6:
        prefix = ipaddress.IPv6Address(bin_to_ip(f"{temp:<0128}", v6))
        return f"{prefix}/{prefix_bits}"
    prefix = ipaddress.IPv4Address(bin_to_ip(f"{temp:<032}"))
    return f"{prefix}/{prefix_bits}"


def validate_adresses(ip_addresses: list[str], v6=False):
    """
    A function that checks IP addresses for correctness.
    If bad entries are present, a ValueError exception is raised.

    Args:
        ip_addresses (list[str]): list of ip-adress str's
        v6 (bool, optional): version flag True if ipv6. Defaults to False.

    Raises:
        ValueError: if ip is incorrect
    """
    constructor = ipaddress.IPv6Address if v6 else ipaddress.IPv4Address
    for adr in ip_addresses:
        try:
            constructor(adr)
        except ipaddress.AddressValueError:
            raise ValueError(f"Incorrect ip values {adr}")


# Пример использования:
if __name__ == "__main__":
    ip_addresses_v4 = ['10.168.1.1',
                       '10.168.1.3',
                       '10.168.1.5']
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
