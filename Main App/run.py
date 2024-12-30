import StudentPortal
import AdminPortal

from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Button, PhotoImage

ASSETS_PATH = Path(__file__).parent/"assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

root = Tk()
root.iconbitmap("assets/windowIcon.ico")
root.geometry("592x378")
root.title("Main Application")
root.configure(bg = "#FFFFFF")


canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 378,
    width = 592,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    592.0,
    69.0,
    fill="#000000",
    outline="")

canvas.create_text(
    10.0,
    22.0,
    anchor="nw",
    text="Attendance Management System using Face Recognition",
    fill="#FFFFFF",
    font=("Inter", 23 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("Admin_Logo.png"))
image_1 = canvas.create_image(
    447.0,
    185.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("Student_Logo.png"))
image_2 = canvas.create_image(
    145.0,
    178.0,
    image=image_image_2
)

canvas.create_rectangle(
    295.0,
    92.0,
    296.0,
    315.0,
    fill="#000000",
    outline="")

button_1 = Button(
    text="I'm Admin",
    font=("Inter", 12),
    fg="Black",
    bg="lightgrey",
    borderwidth=3,
    highlightthickness=3,
    command= lambda: AdminPortal.adminLogin(root),
    relief="raised"
)
button_1.place(
    x=375.0,
    y=285.0,
    width=125.0,
    height=26.0
)

button_2 = Button(
    text="I'm Student",
    font=("Inter", 12),
    fg="black",
    bg="lightgrey",
    borderwidth=3,
    highlightthickness=3,
    command= lambda: StudentPortal.studentPortal(root),
    relief="raised"
)
button_2.place(
    x=83.0,
    y=284.0,
    width=125.0,
    height=26.0
)

canvas.create_rectangle(
    0.0,
    336.0,
    592.0,
    378.0,
    fill="black",
    outline="")

canvas.create_text(
    182.0,
    339.0,
    anchor="nw",
    text="WHO ARE YOU ?",
    fill="white",
    font=("Inter", 30 * -1)
)
root.resizable(False, False)
root.mainloop()