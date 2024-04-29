import tkinter as tk
from PIL import ImageTk, Image
import list_interfaces
import start_page

from functions import wifi_scanner, wifi_connecter


def show_next_page(root):
    root.destroy()
    list_interfaces.main()


def show_start_page(root):
    root.destroy()
    start_page.main()


def refresh_page(listbox):
    listbox.delete(0, tk.END)
    populate_list(listbox)


def create_password_popup(wifi_name):
    popup = tk.Toplevel()
    popup.title("Enter Password")
    popup.geometry("600x300")

    label = tk.Label(popup, text=f"Enter password for {wifi_name}:", font=("Georgia", 15))
    label.pack(pady=10)

    password_entry = tk.Entry(popup, show="*", font=("Georgia", 15))
    password_entry.pack(pady=5)

    connect_button = tk.Button(popup, text="Connect",
                               command=lambda: wifi_connecter.update_wifi_profile(wifi_name, password_entry.get(),
                                                                                  'Wi-Fi-' + wifi_name + '.xml', popup),
                               font=("Georgia", 15), bg="#46428a", fg="white")
    connect_button.pack(side=tk.RIGHT, padx=10)

    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy,
                              font=("Georgia", 15), bg="#46428a", fg="white")
    cancel_button.pack(side=tk.RIGHT, padx=10)


def on_item_click(event):
    widget = event.widget
    index = widget.curselection()[0]
    wifi_name = widget.get(index)
    status = wifi_connecter.connect_to_wifi(wifi_name)
    if not status:
        create_password_popup(wifi_name)


def populate_list(listbox):
    wifi_list = wifi_scanner.list_available_wifi_networks()
    for wifi_name in wifi_list:
        listbox.insert(tk.END, wifi_name)


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
    listbox.bind("<ButtonRelease-1>", on_item_click)
    bottom_panel = tk.Frame(root, bg="#020024")
    bottom_panel.place(relx=0.5, rely=1.0, anchor="s", width=window_width, height=50)
    back_button = tk.Button(bottom_panel, text="Back", command=lambda: show_start_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)
    refresh_button = tk.Button(bottom_panel, text="Refresh", command=lambda: refresh_page(listbox),
                               font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100,
                               pady=10)
    refresh_button.pack(side=tk.LEFT, padx=200, pady=10)
    next_button = tk.Button(bottom_panel, text="Next", command=lambda: show_next_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    next_button.pack(side=tk.RIGHT, padx=10, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
