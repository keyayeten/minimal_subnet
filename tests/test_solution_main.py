from ip_manipulations import ip_reduce
import pytest


def test_correct_ipv4():
    ip_addresses_v4 = ['192.168.1.1',
                       '192.168.1.3',
                       '192.168.1.5']
    assert ip_reduce.get_solution(ip_addresses_v4) == "192.168.1.0/29"


def test_correct_ipv6():
    ip_addresses_v6 = ["ffe0::1:0:0:0",
                       "ffe0::2:0:0:0",
                       "ffe0::4:0:0:0",
                       "ffe0::8:0:0:0",
                       "ffe0::10:0:0:0",
                       "ffe0::20:0:0:0",
                       "ffe0::40:0:0:0",
                       "ffe0::80:0:0:0"]
    assert ip_reduce.get_solution(ip_addresses_v6, True) == "ffe0::/72"


def test_edge_cases():
    ip_addresses_edge_min = [
        '0.0.0.0', '0.0.0.1',
        '0.0.0.2', '0.0.0.3',
        '0.0.0.4', '0.0.0.5',
        '0.0.0.6', '0.0.0.7',
        '0.0.0.8', '0.0.0.9'
    ]
    assert ip_reduce.get_solution(ip_addresses_edge_min) == "0.0.0.0/28"
    ip_addresses_edge_max = [
        '255.255.255.0', '255.255.255.1',
        '255.255.255.2', '255.255.255.3',
        '255.255.255.4', '255.255.255.5',
        '255.255.255.6', '255.255.255.7',
        '255.255.255.255', '255.255.255.9'
    ]
    assert ip_reduce.get_solution(ip_addresses_edge_max) == "255.255.255.0/24"


def test_single_ipv4():
    ip_address_single_v4 = ['192.168.1.1']
    assert ip_reduce.get_solution(ip_address_single_v4) == "192.168.1.1/32"


def test_single_ipv6():
    ip_address_single_v6 = ['2001:db8::1']
    assert (ip_reduce.get_solution(ip_address_single_v6, True)
            == "2001:db8::1/128")


def test_same_subnet():
    ip_addresses_same_subnet = [
        '192.168.1.1', '192.168.1.2',
        '192.168.1.3', '192.168.1.4'
    ]
    assert ip_reduce.get_solution(ip_addresses_same_subnet) == "192.168.1.0/29"


def test_different_versions():
    ip_addresses = [
        '192.168.1.1', '192.168.1.2',
        '2001:db8::1', '192.168.1.4'
    ]
    with pytest.raises(ValueError):
        ip_reduce.get_solution(ip_addresses) == "192.168.1.0/29"
