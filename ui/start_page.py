import tkinter as tk

import wifi_scanner
from PIL import ImageTk, Image


def open_wifi_list(root):
    root.destroy()
    wifi_scanner.main()


def main():
    root = tk.Tk()
    root.title("Scan IOT Devices")
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

    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    start_button = tk.Button(frame, text="START", command=lambda: open_wifi_list(root), font=("Georgia", 20, "bold"),
                             bg="light grey", fg="Black", relief="raised", padx=100, pady=10)
    start_button.pack()
    frame.place_configure(relx=0.5, rely=0.5, anchor="center", x=-200)

    root.mainloop()


if __name__ == "__main__":
    main()
