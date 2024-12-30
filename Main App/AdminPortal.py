import os
import csv
import subprocess
import sys
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Toplevel,messagebox
from PIL import Image,ImageTk

ASSETS_PATH = Path(__file__).parent/"assets"

image_files=[]
current_index=0

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def verifyUser(AdminLogin_window,entry_1,entry_2):
    username=entry_1.get().strip()
    password=entry_2.get().strip()
    if username=="" or password=="":
        print("Give values")
        messagebox.showerror("Empty Input","Both fields are required to Login")
    elif username=="Admin123" and password=="passwordxyz":
        AdminLogin_window.destroy()
        adminPortal()
    else:
        messagebox.showerror("Login failed","Incorrect Name or Password. Please try again")

#Admin Login Window

def adminLogin(root):
    root.destroy()
    AdminLogin_window = Tk()
    AdminLogin_window.iconbitmap("assets/windowIcon.ico")

    AdminLogin_window.title("Admin Login")
    AdminLogin_window.geometry("581x251")
    AdminLogin_window.configure(bg = "#FFFFFF")

    canvas = Canvas(
        AdminLogin_window,
        bg = "#FFFFFF",
        height = 251,
        width = 581,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)

    entry_1 = Entry(AdminLogin_window,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Inter",12)
    )
    entry_1.place(
        x=131.0,
        y=69.0,
        width=220.0,
        height=27.0
    )

    entry_2 = Entry(AdminLogin_window,           
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Inter",12)
    )
    entry_2.place(
        x=131.0,
        y=120.0,
        width=220.0,
        height=27.0
    )

    canvas.create_text(
        56.0,
        69.0,
        anchor="nw",
        text="Name :",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        20.0,
        122.0,
        anchor="nw",
        text="Password :",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    button_1 = Button(AdminLogin_window,
        text="LOGIN",
        font=("inter", 12),
        fg="black",
        bg="lightgreen",
        borderwidth=4,
        highlightthickness=4,
        command=lambda: verifyUser(AdminLogin_window,entry_1,entry_2),
        relief="raised"
    )
    button_1.place(
        x=141.0,
        y=173.0,
        width=83.0,
        height=28.0
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        368.0,
        40.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        90.0,
        1.0,
        anchor="nw",
        text="Admin Login",
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    canvas.create_rectangle(
        0.0,
        223.0,
        581.0,
        251.0,
        fill="#000000",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("Admin_Login_Pic.png"))
    image_1 = canvas.create_image(
        474.0,
        111.0,
        image=image_image_1
    )
    AdminLogin_window.resizable(False, False)
    AdminLogin_window.mainloop()

#Admin Portal Window

def adminPortal():

    def open_folder(directory_path):
        if not(os.path.exists(directory_path)):
            messagebox.showinfo("Empty Report","Attendance Report doesn't exist. Try registering students\nand make them mark attendance")
            return
        try:
            if sys.platform == "win32":
                os.startfile(directory_path)  # For Windows
            elif sys.platform == "darwin":
                subprocess.run(["open", directory_path])  # For macOS
            else:  # For Linux
                subprocess.run(["xdg-open", directory_path])
        except Exception as e:
            messagebox.showerror("Error Occured",f"Error in opening folder: {e}")

    AdminPortal_window = Tk()
    AdminPortal_window.iconbitmap("assets/windowIcon.ico")

    AdminPortal_window.title("Admin Portal")
    AdminPortal_window.geometry("550x188")
    AdminPortal_window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        AdminPortal_window,
        bg = "#FFFFFF",
        height = 188,
        width = 550,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("Admin_Portal_Pic.png"))
    image_1 = canvas.create_image(
        439.0,
        84.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        328.0,
        39.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        67.0,
        0.0,
        anchor="nw",
        text="Admin Portal",
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    button_1 = Button(AdminPortal_window,
        text="Attendance Report",
        bg="gray",
        fg="black",
        font=("Inter", 18),
        borderwidth=3,
        highlightthickness=3,
        command=lambda: open_folder(os.path.abspath("database/attendance_report")),
        relief="raised"
    )
    button_1.place(
        x=18.0,
        y=56.0,
        width=293.0,
        height=36.0
    )

    button_2 = Button(AdminPortal_window,
        text="Verify Manual Attendance",
        bg="gray",
        fg="black",
        font=("Inter", 15),
        borderwidth=3,
        highlightthickness=3,
        command=lambda: VerifyManualAttendance(AdminPortal_window),
        relief="raised"
    )
    button_2.place(
        x=18.0,
        y=113.0,
        width=293.0,
        height=34.0
    )

    canvas.create_rectangle(
        0.0,
        169.0,
        550.0,
        188.0,
        fill="#000000",
        outline="")
    AdminPortal_window.resizable(False, False)
    AdminPortal_window.mainloop()

# Verify Manual Attendance Window

def VerifyManualAttendance(AdminPortal_window):
    try:
        if len(os.listdir("database/manual_attendance_images"))==0:
            messagebox.showinfo("No Entries Found", "There are no manual attendance entries available for verification.")
            return
    except FileNotFoundError:
        messagebox.showinfo("No Entries Found", "There are no manual attendance entries available for verification.")
        return

    global image_files,current_index
    current_index=0

    def update_canvas():
        nonlocal image_display, student_name_text, student_id_text, student_subject_text, remaining_text

        # Update image
        image_file = image_files[current_index]
        image_file_name = os.path.basename(image_file).split(".")
        
        pil_image = Image.open(image_file)
        pil_image.thumbnail((320, 240))
        image_display = ImageTk.PhotoImage(pil_image)
        canvas.itemconfig(image_1, image=image_display)

        # Fetch student details
        student_name = ""
        with open("database/attendance_report/student_details.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == image_file_name[0]:
                    student_name = row[1]
                    break

        # Update text fields
        canvas.itemconfig(student_name_text, text=student_name)
        canvas.itemconfig(student_id_text, text=image_file_name[0])
        canvas.itemconfig(student_subject_text, text=image_file_name[1])
        canvas.itemconfig(remaining_text, text=f"Number of Students remaining: {len(image_files) - current_index}/{len(image_files)}")

    def VerifyStudent(details,student_name,image_file):
        global current_index
        try:
            os.remove(image_file)
        except Exception as e:
            messagebox.showerror("Error Occured",f"Error: {e}")
            return
        with open("database/attendance_report/attendance_log.csv","a") as file:
            writer = csv.writer(file)
            writer.writerow(["Id", "Name", "Subject", "Date", "Time"])
            writer.writerow([details[0],student_name,details[1],details[2],details[3].replace("-",":")])
        current_index += 1
        if current_index < len(image_files):
            update_canvas()
        else:
            VerifyManualAttendance_window.destroy()
            messagebox.showinfo("Completed", "All entries have been processed.")
    def RejectStudent(image_file):
        global current_index
        try:
            os.remove(image_file)
        except Exception as e:
            messagebox.showerror("Error Occured",f"Error: {e}")
            return
        current_index += 1
        if current_index < len(image_files):
            update_canvas()
        else:
            VerifyManualAttendance_window.destroy()
            messagebox.showinfo("Completed", "All entries have been processed.")
   
    VerifyManualAttendance_window = Toplevel(AdminPortal_window)
    VerifyManualAttendance_window.iconbitmap("assets/windowIcon.ico")
    VerifyManualAttendance_window.title("Attendance Verification")
    VerifyManualAttendance_window.geometry("428x486")
    VerifyManualAttendance_window.configure(bg="#FFFFFF")

    VerifyManualAttendance_window.grab_set()
    VerifyManualAttendance_window.protocol("WM_DELETE_WINDOW", lambda: [VerifyManualAttendance_window.grab_release(), VerifyManualAttendance_window.destroy()])

    image_files = [os.path.join("database/manual_attendance_images", f) for f in os.listdir("database/manual_attendance_images") if os.path.isfile(os.path.join("database/manual_attendance_images", f))]

    canvas = Canvas(
        VerifyManualAttendance_window,
        bg="#FFFFFF",
        height=486,
        width=428,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas.create_rectangle(0.0, 0.0, 428.0, 44.0, fill="#000000", outline="")
    canvas.create_text(22.0, 5.0, anchor="nw", text="Manual Attendance Verification", fill="#FFFFFF", font=("Inter", 28 * -1))

    image_display = None
    image_1 = canvas.create_image(214.0, 176.0, image=None)

    canvas.create_text(68.0, 308.0, anchor="nw", text="Name :", fill="#000000", font=("Inter", 23 * -1))
    student_name_text = canvas.create_text(158.0, 310.0, anchor="nw", text="", fill="#000000", font=("Inter", 21 * -1))

    canvas.create_text(106.0, 336.0, anchor="nw", text="ID :", fill="#000000", font=("Inter", 23 * -1))
    student_id_text = canvas.create_text(158.0, 338.0, anchor="nw", text="", fill="#000000", font=("Inter", 21 * -1))

    canvas.create_text(53.0, 364.0, anchor="nw", text="Subject :", fill="#000000", font=("Inter", 23 * -1))
    student_subject_text = canvas.create_text(158.0, 366.0, anchor="nw", text="", fill="#000000", font=("Inter", 21 * -1))

    button_1 = Button(
        VerifyManualAttendance_window,
        text="VERIFIED",
        bg="lightgreen",
        fg="black",
        font=("Inter", 14),
        borderwidth=3,
        highlightthickness=3,
        command=lambda: VerifyStudent(os.path.basename(image_files[current_index]).split("."), canvas.itemcget(student_name_text, "text"), image_files[current_index]),
        relief="raised"
    )
    button_1.place(x=87.0, y=409.0, width=119.0, height=28.0)

    button_2 = Button(
        VerifyManualAttendance_window,
        text="REJECT",
        bg="lightcoral",
        fg="black",
        font=("Inter", 14),
        borderwidth=3,
        highlightthickness=3,
        command=lambda: RejectStudent(image_files[current_index]),
        relief="raised"
    )
    button_2.place(x=233.0, y=409.0, width=103.0, height=28.0)

    canvas.create_rectangle(0.0, 451.0, 428.0, 486.0, fill="#000000", outline="")
    remaining_text = canvas.create_text(10.0, 456.0, anchor="nw", text="", fill="#FFFFFF", font=("Inter", 21 * -1))

    update_canvas()
    VerifyManualAttendance_window.resizable(False, False)
    VerifyManualAttendance_window.mainloop()