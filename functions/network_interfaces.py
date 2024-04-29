from ipaddress import IPv4Network
import psutil
import socket


def get_network_interfaces():
    return psutil.net_if_addrs()


def get_network_details(network_interface):
    int_faces = psutil.net_if_addrs()
    if network_interface in int_faces:
        for a in int_faces[network_interface]:
            if a.family == socket.AF_INET:
                return a.address, a.netmask
    return None, None


def calculate_network_range(ipaddress, sub_mask):
    network = IPv4Network(f"{ipaddress}/{sub_mask}", strict=False)
    return str(network.network_address) + "/" + str(network.prefixlen)
