import tkinter as tk
from PIL import ImageTk, Image
import show_devices
import wifi_scanner

from functions import network_interfaces


def show_next_page(root, interface, network_range):
    root.destroy()
    show_devices.main(interface, network_range)


def show_prev_page(root):
    root.destroy()
    wifi_scanner.main()


def refresh_page(listbox):
    listbox.delete(0, tk.END)
    populate_list(listbox)


def create_info_popup(interface, info, root):
    popup = tk.Toplevel()
    popup.title("Interface information")
    popup.geometry("600x300")
    popup.resizable(False, False)
    ip = info[0]
    subnet = info[1]
    network_range = network_interfaces.calculate_network_range(info[0], info[1])
    label1 = tk.Label(popup, text=f"IP Address:  {ip}:", font=("Georgia", 20))
    label1.pack(pady=10)
    label2 = tk.Label(popup, text=f"Subnet mask: {subnet}:", font=("Georgia", 20))
    label2.pack(pady=10)
    label3 = tk.Label(popup, text=f"Network range: {network_range}:",
                      font=("Georgia", 20))
    label3.pack(pady=10)
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy,
                              font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    cancel_button.pack(side=tk.LEFT, padx=10, pady=10)
    next_button = tk.Button(popup, text="Next", command=lambda: show_next_page(root, interface, network_range),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    next_button.pack(side=tk.RIGHT, padx=10, pady=10)


def on_item_click(event, root):
    widget = event.widget
    index = widget.curselection()[0]
    interface = widget.get(index)
    status = network_interfaces.get_network_details(interface)
    create_info_popup(interface, status, root)


def populate_list(listbox):
    interfaces = network_interfaces.get_network_interfaces()
    for interface in interfaces:
        listbox.insert(tk.END, interface)


def main():
    root = tk.Tk()
    root.title("Wifi Scanner")
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
    populate_list(listbox)
    listbox.bind("<ButtonRelease-1>", lambda event: on_item_click(event, root))
    bottom_panel = tk.Frame(root, bg="#020024")
    bottom_panel.place(relx=0.5, rely=1.0, anchor="s", width=window_width, height=50)
    back_button = tk.Button(bottom_panel, text="Back", command=lambda: show_prev_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
