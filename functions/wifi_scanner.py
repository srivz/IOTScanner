import subprocess


def list_available_wifi_networks():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)
        if result.returncode == 0:
            networks = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'SSID' in line]
            return networks
        else:
            print("Error: Failed to execute 'netsh wlan show networks' command.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
