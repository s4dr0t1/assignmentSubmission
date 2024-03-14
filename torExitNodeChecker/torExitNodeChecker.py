#!/usr/bin/env python3

"""
Rohit Dhill <rohit.dhill.533@gmail.com>

Assignment 1: A Python script which checks whether a given IP or an exit node for the Tor network
"""

import argparse
import csv
import requests
import re


def is_exit_node(ip_address, exit_nodes):
    return ip_address in exit_nodes


def check_single_ip(ip_address, exit_nodes):
    ipv4_regex = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address)

    if bool(ipv4_regex) == True:
        result = is_exit_node(ip_address, exit_nodes)
        print(f"{ip_address} is a Tor exit node: {result}")
    else:
        print(f"{ip_address} is not a correct IPv4 address")


def check_ip_list(ip_list_file, exit_nodes):
    try:
        with open(ip_list_file, "r") as f:
            csvfile = open("results.csv", "w", newline="")
            fieldnames = ["IP", "Exit node"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ip_address in f:
                ip_address = ip_address.strip()
                result = is_exit_node(ip_address, exit_nodes)
                writer.writerow({"IP": ip_address, "Exit node": str(result)})
            print(f"Results saved to ./results.csv")
    except FileNotFoundError:
        print(f"File {ip_list_file} does not exist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if an IP address(es) is a Tor exit node"
    )
    parser.add_argument("--ip", type=str, help="Check a single IP address")
    parser.add_argument(
        "--ip-list",
        type=str,
        help="Check a list of IP addresses specified through a text file",
    )
    args = parser.parse_args()

    exit_nodes_url = "https://check.torproject.org/exit-addresses"
    response = requests.get(exit_nodes_url)
    response.raise_for_status()  # Exception if status code != 200

    exit_nodes = set()
    for line in response.text.splitlines():
        if line.startswith("ExitAddress "):
            ip_address = line.split()[1]
            exit_nodes.add(ip_address)

    if args.ip:
        check_single_ip(args.ip, exit_nodes)
    elif args.ip_list:
        check_ip_list(args.ip_list, exit_nodes)
    else:
        parser.print_help()
