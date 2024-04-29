import tkinter as tk
from PIL import ImageTk, Image
import list_interfaces
import sqlite3

from functions import arp_scanner
import packet_sniffer
import history


def show_capture_page(root, info, interface):
    root.destroy()
    packet_sniffer.main(info, interface)


def show_history_page(root, mac):
    root.destroy()
    history.main(mac)


def show_prev_page(root):
    root.destroy()
    list_interfaces.main()


def refresh_page(listbox, interface, net_range):
    listbox.delete(0, tk.END)
    populate_list(listbox, interface, net_range)


def save_device_info(popup, mac, device_name):
    conn = None
    try:
        conn = sqlite3.connect('../db/devices.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                                mac TEXT PRIMARY KEY,
                                device_name TEXT
                              )''')
        cursor.execute("INSERT OR REPLACE INTO devices VALUES (?, ?)", (mac, device_name))
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if conn:
            conn.close()
        popup.destroy()


def fetch_device_name(mac):
    conn = None
    try:
        conn = sqlite3.connect('../db/devices.db')
        cursor = conn.cursor()
        cursor.execute("SELECT device_name FROM devices WHERE mac=?", (mac,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None
    finally:
        if conn:
            conn.close()


def add_info_popup(info):
    popup = tk.Toplevel()
    ip = info.split("|")[1]
    mac = info.split("|")[2]
    device_info = info.split("|")[0]
    manuf = info.split("|")[3]
    popup.title("Edit Device information")
    popup.geometry("900x300")
    popup.resizable(False, False)
    label1 = tk.Label(popup, text=f"IP Address:  {ip}", font=("Georgia", 15))
    label1.pack(pady=10)
    label2 = tk.Label(popup, text=f"MAC Address:  {mac}", font=("Georgia", 15))
    label2.pack(pady=10)
    label4 = tk.Label(popup,
                      text=f"Manufacturer:  {"Not registered(Device using dynamic MAC)" if manuf == "Unknown" else manuf}",
                      font=("Georgia", 15))
    label4.pack(pady=10)
    label3 = tk.Label(popup, text=f"Device name(or Nickname):", font=("Georgia", 20))
    label3.pack(pady=10)
    device_name = tk.Entry(popup, font=("Georgia", 15))
    device_name.insert(0, device_info)
    device_name.pack(pady=5, fill=tk.X)

    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy,
                              font=("Georgia", 15), bg="#46428a", fg="white")
    cancel_button.pack(side=tk.RIGHT, padx=10)
    save_button = tk.Button(popup, text="Save", command=lambda: save_device_info(popup, mac, device_name.get()),
                            font=("Georgia", 15), bg="#46428a", fg="white")
    save_button.pack(side=tk.RIGHT, padx=10)


def options_popup(root, info, interface):
    popup = tk.Toplevel()
    popup.title("Device information")
    popup.geometry("600x300")
    popup.resizable(False, False)

    device_info_button = tk.Button(popup, text="Add device info", command=lambda: add_info_popup(info),
                                   font=("Georgia", 15), bg="#46428a", fg="white")
    device_info_button.pack(side=tk.TOP, pady=10)

    capture_button = tk.Button(popup, text="Capture Packets", command=lambda: show_capture_page(root, info, interface),
                               font=("Georgia", 15), bg="#46428a", fg="white")
    capture_button.pack(side=tk.TOP, pady=10)

    history_button = tk.Button(popup, text="Capture History", command=lambda: show_history_page(root, info.split("|")[2]),
                               font=("Georgia", 15), bg="#46428a", fg="white")
    history_button.pack(side=tk.TOP, pady=10)

    cancel_button = tk.Button(popup, text="Back", command=popup.destroy, font=("Georgia", 15), bg="#46428a", fg="white")
    cancel_button.pack(side=tk.TOP, pady=10)


def on_item_click(root, event, interface):
    widget = event.widget
    index = widget.curselection()[0]
    device = widget.get(index)
    options_popup(root, device, interface)


def populate_list(listbox, interface, net_range):
    devices = arp_scanner.arp_scan(interface, net_range)
    for device in devices:
        fetched = fetch_device_name(device['MAC Address'])
        if fetched is not None:
            display_name = fetched + "|" + device['IP'] + "|" + device['MAC Address'] + "|" + device['MAC Vendor']
        else:
            display_name = "Unnamed_device|" + device['IP'] + "|" + device['MAC Address'] + "|" + device['MAC Vendor']
        listbox.insert(tk.END, display_name)


def main(interface="Local Area Connection* 2", net_range="192.168.137.0/24"):
    root = tk.Tk()
    root.title("Available Devices")
    window_width = 1280
    window_height = 720
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    background_image = Image.open("../assets/bg.jpeg")
    background_image = background_image.resize((window_width, window_height))
    background_photo = ImageTk.PhotoImage(background_image)
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    list_frame = tk.Frame(root, bg="#020024")
    list_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400, x=-300)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(list_frame, font=("Georgia", 20, "bold"), width=40, height=15, yscrollcommand=scrollbar.set)
    listbox.pack(fill="both", expand=True)

    scrollbar.config(command=listbox.yview)

    listbox.bind("<ButtonRelease-1>", lambda event: on_item_click(root, event, interface))

    bottom_panel = tk.Frame(root, bg="#020024")
    bottom_panel.place(relx=0.5, rely=1.0, anchor="s", width=window_width, height=50)

    back_button = tk.Button(bottom_panel, text="Back", command=lambda: show_prev_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    def enable_refresh_button():
        refresh_button.config(state="normal")

    def refresh_and_disable():
        refresh_button.config(state="disabled")
        refresh_page(listbox, interface, net_range)
        root.after(60000, enable_refresh_button)

    refresh_button = tk.Button(bottom_panel, text="Refresh",
                               command=lambda: refresh_and_disable(),
                               font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100,
                               pady=10)
    refresh_button.pack(side=tk.LEFT, padx=200, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
