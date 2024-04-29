import tkinter as tk
from PIL import ImageTk, Image
import start_page
import sqlite3
import show_devices
from tkinter import messagebox
from tkinter import filedialog
import shutil
import os


def show_next_page(root):
    root.destroy()
    start_page.main()


def show_prev_page(root):
    root.destroy()
    show_devices.main()


def edit_file_name_in_db(file_name, new_name):
    conn = sqlite3.connect('../db/file_storage.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Files SET filename = ? WHERE filename = ?", (new_name, file_name))
    conn.commit()
    conn.close()


def delete_capture_packets(popup, output_file):
    try:
        os.remove("../packet-captures/" + output_file)
        delete_file_in_db(output_file)
        show_notification("Deleted the file " + output_file + " successfully!!", "Delete Complete")
        popup.destroy()
    except Exception as e:
        print(f"An error occurred while deleting captured packets: {e}")


def delete_file_in_db(output_file):
    conn = sqlite3.connect('../db/file_storage.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Files
                      (mac TEXT, filename TEXT PRIMARY KEY, summary TEXT, time TEXT)''')
    cursor.execute("DELETE FROM Files WHERE filename = ?", (output_file,))
    conn.commit()


def show_notification(msg, title="Notification"):
    messagebox.showinfo(title, msg)


def fetch_files_by_mac(mac):
    conn = sqlite3.connect('../db/file_storage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT filename, summary, time FROM Files WHERE mac = ?", (mac,))
    files_data = cursor.fetchall()
    conn.close()
    file_data = []

    for file in reversed(files_data):
        filename, summary, time = file
        file_info = {
            'filename': filename,
            'summary': summary,
            'time': time
        }
        file_data.append(file_info)

    return file_data


def download_file(file_name):
    try:
        destination_file = filedialog.asksaveasfilename(defaultextension=".pcap",
                                                        filetypes=[("PCAP files", "*.pcap"), ("All files", "*.*")])
        shutil.copyfile("../packet-captures/" + file_name, destination_file)
        show_notification(f"File saved successfully to {destination_file}", "Save Complete")
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving file: {e}")


def edit_download_popup(time, file_name, summary):
    popup = tk.Toplevel()
    popup.title("Capture details")
    popup.geometry("800x500")
    popup.resizable(False, False)

    label1 = tk.Label(popup,
                      text=f"Capture time : {time.replace("_", "-").replace("-", " ", 2).replace("_", ":").replace(" ", "-", 2)}",
                      font=("Georgia", 15))
    label1.pack(pady=10)

    label2 = tk.Label(popup, text=f"File name :", font=("Georgia", 15))
    label2.pack(padx=5)

    file_name_used = tk.Entry(popup, font=("Georgia", 15), width=70)
    file_name_used.insert(0, file_name)
    file_name_used.pack(padx=10)

    connect_button = tk.Button(popup, text="Change",
                               command=lambda: edit_file_name_in_db(file_name, file_name_used.get()),
                               font=("Georgia", 15), bg="#46428a", fg="white")
    connect_button.pack(pady=5, padx=5)

    label3 = tk.Label(popup, text=f"Summary : ", font=("Georgia", 15))
    label3.pack(pady=10)

    summary_text = tk.Text(popup, font=("Georgia", 10), wrap="word", height=10, width=100)
    summary_text.insert(tk.END, summary)
    summary_text.config(state="disabled")
    summary_text.pack(pady=10)

    download_button = tk.Button(popup, text="Download",
                                command=lambda: download_file(file_name),
                                font=("Georgia", 15), bg="#46428a", fg="white")
    download_button.pack(side=tk.RIGHT, pady=5, padx=5)

    delete_button = tk.Button(popup, text="Delete",
                            command=lambda: delete_capture_packets(popup, file_name),
                            font=("Georgia", 15), bg="#ff6969", fg="black")
    delete_button.pack(side=tk.LEFT, pady=10, padx=10)


def on_item_click(event, data):
    widget = event.widget
    index = widget.curselection()[0]
    item = widget.get(index)
    edit_download_popup(item, data[index]["filename"], data[index]["summary"])


def populate_list(listbox, data):
    for timestamp in data:
        listbox.insert(tk.END,
                       timestamp["time"].replace("_", "-").replace("-", " ", 3).replace("-", ":").replace(" ", "-", 2))


def main(mac="bc:64:d9:37:37:4d"):
    root = tk.Tk()
    root.title("History")
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

    data = fetch_files_by_mac(mac)
    populate_list(listbox, data)

    listbox.bind("<ButtonRelease-1>", lambda event: on_item_click(event, data))

    bottom_panel = tk.Frame(root, bg="#020024")
    bottom_panel.place(relx=0.5, rely=1.0, anchor="s", width=window_width, height=50)

    back_button = tk.Button(bottom_panel, text="Back", command=lambda: show_prev_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    next_button = tk.Button(bottom_panel, text="Go to Start", command=lambda: show_next_page(root),
                            font=("Georgia", 15, "bold"), bg="#46428a", fg="white", relief="raised", padx=100, pady=10)
    next_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
