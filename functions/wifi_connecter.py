import os
import subprocess
import xml.etree.ElementTree as ET


def update_wifi_profile(ssid, password, output_file, popup):
    tree = ET.parse(os.path.join(os.path.dirname(__file__), "Wi-Fi-Sample.xml"))
    root = tree.getroot()
    for elem in root.iter():
        if elem.tag.endswith('name'):
            elem.text = ssid
        elif elem.tag.endswith('hex'):
            elem.text = ''.join(hex(ord(c))[2:].upper() for c in ssid)  # Convert SSID to hex
        elif elem.tag.endswith('keyMaterial'):
            elem.text = password

    tree.write(output_file.replace("f?T", "\'"))
    with open(output_file, 'a'):
        pass
    print("Profile updated successfully.")
    create_wifi_profile(ssid, output_file)
    popup.destroy()


def create_wifi_profile(ssid, output_file):
    try:
        result1 = subprocess.run(['netsh', 'wlan', 'add', 'profile', output_file], capture_output=True, text=True)
        if result1.returncode == 0:
            os.remove(output_file)
            connect_to_wifi(ssid)
        else:
            print("Error")
    except Exception as e:
        print(f"Error: {e}")


def connect_to_wifi(ssid):
    try:
        result = subprocess.run(['netsh', 'wlan', 'connect', 'name=' + ssid], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully connected to Wi-Fi network '{ssid}'.")
            return True
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
