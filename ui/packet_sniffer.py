import tkinter as tk
import time
import sqlite3
from datetime import datetime
from tkinter import filedialog
import shutil
from PIL import ImageTk, Image
import show_devices
import start_page
from functions import packet_manager
from tkinter import messagebox
import os


def show_notification(msg, title="Notification"):
    messagebox.showinfo(title, msg)


def show_prev_page(root):
    root.destroy()
    show_devices.main()


def open_wifi_list(root):
    root.destroy()
    start_page.main()


def save_file_in_db(output_file, mac, summary_got, time_now):
    conn = sqlite3.connect('../db/file_storage.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Files
                      (mac TEXT, filename TEXT PRIMARY KEY, summary TEXT, time TEXT)''')
    cursor.execute("INSERT INTO Files (mac, filename, summary, time) VALUES (?, ?, ?, ?)",
                   (mac, output_file, summary_got, time_now))
    conn.commit()
    show_notification("Saved the file as " + output_file + " successfully!!", "Save Complete")


def delete_capture_packets(summary, output_file):
    try:
        os.remove("../" + output_file)
        delete_file_in_db(output_file)
        show_notification("Deleted the file " + output_file.split("/")[1] + " successfully!!", "Delete Complete")
        summary.insert(tk.END, "")
    except Exception as e:
        print(f"An error occurred while deleting captured packets: {e}")


def delete_file_in_db(output_file):
    conn = sqlite3.connect('../db/file_storage.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Files
                      (mac TEXT, filename TEXT PRIMARY KEY, summary TEXT, time TEXT)''')
    cursor.execute("DELETE FROM Files WHERE filename = ?", (output_file.split("/")[1],))
    conn.commit()


def capture_set_packets(root, packet_count, interface, info):
    time_now = str(datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d_%H_%M_%S"))
    output_file = "packet-captures/" + info.split("|")[0] + "-" + info.split("|")[2].replace(":",
                                                                                             ".") + "-" + time_now + ".pcap"
    output_dir = os.path.dirname("../" + output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    packet_manager.capture_packets(interface, info.split("|")[1], int(packet_count), output_file)
    summary_got = "\n".join(packet.summary() for packet in (packet_manager.read_packets(output_file)))
    save_file_in_db(output_file.split("/")[1], info.split("|")[2], summary_got, time_now)
    frame2 = tk.Frame(root)
    frame2.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
    label1 = tk.Label(frame2, text=f"Summary of the capture:", font=("Georgia", 16))
    label1.pack(pady=10, padx=10)

    summary_text = tk.Text(frame2, font=("Georgia", 10), wrap="word", height=10, width=100)
    summary_text.insert(tk.END, summary_got)
    summary_text.config(state="disabled")
    summary_text.pack(pady=10)

    save_button = tk.Button(frame2, text="Download",
                            command=lambda: download_capture_packets(output_file),
                            font=("Georgia", 15), bg="#46428a", fg="white")
    save_button.pack(side=tk.LEFT, pady=10, padx=10)

    delete_button = tk.Button(frame2, text="Delete",
                              command=lambda: delete_capture_packets(summary_text, output_file),
                              font=("Georgia", 15), bg="#ff6969", fg="black")
    delete_button.pack(side=tk.LEFT, pady=10, padx=10)

    frame2.place_configure(relx=0.5, rely=0.5, anchor="center", x=-250, y=100)


def download_capture_packets(filename):
    try:
        destination_file = filedialog.asksaveasfilename(defaultextension=".pcap",
                                                        filetypes=[("PCAP files", "*.pcap"), ("All files", "*.*")])

        shutil.copyfile("../" + filename, destination_file)
        messagebox.showinfo("Save Complete", f"File saved successfully to {destination_file}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving file: {e}")


def main(info="OppoReno8T|192.168.137.4|bc:64:d9:37:37:4d|Unknown", interface="Local Area Connection* 2"):
    root = tk.Tk()
    root.title("Packet Sniffer")

    # Set window size
    window_width = 1280
    window_height = 720
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)

    # Load background image
    background_image = Image.open("../assets/bg.jpeg")
    background_image = background_image.resize((window_width, window_height))
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a canvas to place the background image
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label1 = tk.Label(frame, text=f"Enter the number of packets to capture:", font=("Georgia", 16))
    label1.pack(pady=10)
    packet_count = tk.Entry(frame, font=("Georgia", 20, "bold"))
    packet_count.pack(padx=10)
    save_button = tk.Button(frame, text="Start Capture",
                            command=lambda: capture_set_packets(root, packet_count.get(), interface, info),
                            font=("Georgia", 15), bg="#46428a", fg="white")
    save_button.pack(side=tk.RIGHT, pady=10, padx=10)

    frame.place_configure(relx=0.5, rely=0.5, anchor="center", x=-250, y=-250)

    bottom_panel = tk.Frame(root, bg="#020024")
    bottom_panel.place(relx=0.5, rely=1.0, anchor="s", width=window_width, height=50)
    back_button = tk.Button(bottom_panel, text="Back", command=lambda: show_prev_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
