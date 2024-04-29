from scapy.all import ARP, Ether, srp
import requests


def arp_scan(network_interface, net_range):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=net_range)
    result = srp(arp_request, timeout=3, iface=network_interface, verbose=False)[0]
    devices = []
    for sent, received in result:
        devices.append({'IP': received.psrc, 'MAC Address': received.hwsrc,
                        'MAC Vendor': query_mac_address_lookup(received.hwsrc)})
    return devices


def get_mac_address(ip_address, device_list):
    for device in device_list:
        if device['IP'] == ip_address:
            return device['MAC Address']
    return None


def query_mac_address_lookup(mac_address):
    oui = mac_address[:8].replace(':', '')
    url = f"https://api.macvendors.com/{oui}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error querying MAC address lookup service: {e}")
        return "Unknown"
