import argparse
from ip_manipulations.ip_reduce import get_solution


def main():
    parser = argparse.ArgumentParser(description='Process IP addresses.')
    parser.add_argument(
        'ip_file',
        type=str,
        help='the name of the file with IP addresses'
    )
    parser.add_argument(
        'ip_version',
        type=str,
        choices=['ipv4', 'ipv6'],
        help='the IP version (ipv4 or ipv6)'
    )

    args = parser.parse_args()

    return get_solution(load_ips(args.ip_file), args.ip_version == 'ipv6')


def load_ips(ip_file: str) -> list[str]:
    """Loads an IP address from a text file

    Args:
        ip_file (str): Location of text file with ip

    Returns:
        list[str]: List of IP addresses
    """
    with open(ip_file, "r") as source:
        return [line.strip() for line in source if line != '']


if __name__ == '__main__':
    print(main())
