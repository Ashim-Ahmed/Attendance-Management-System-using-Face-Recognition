import os
import cv2
import numpy as np
import datetime
import csv
import platform
import threading
import time
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Toplevel,messagebox,Label
from tkinter.ttk import Combobox,Progressbar
from PIL import Image,ImageTk

ASSETS_PATH = Path(__file__).parent/"assets"
toggle_indeterminate_progress=False

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def show_progress(total_steps, title="Progress", message="Processing...", on_complete=None):
    """
    Displays a progress bar window for determinate progress.
    
    Parameters:
        total_steps (int): Total number of steps to complete.
        title (str): Title of the progress window.
        message (str): Message displayed above the progress bar.
        on_complete (callable): Function to call when progress is complete.
    """
    # Create a progress bar window
    progress_window = Toplevel()
    progress_window.iconbitmap("assets/windowIcon.ico")
    progress_window.title(title)
    progress_window.geometry("400x130")
    progress_window.resizable(False, False)

    canvas = Canvas(progress_window, width=400, height=130)
    canvas.pack()
    
    # Message Label
    canvas.create_text(200, 30, text=message, font=("Arial", 12))
    
    # Progress Bar Widget
    progress_bar = Progressbar(progress_window, orient="horizontal", length=350, mode="determinate")
    progress_bar.place(x=25, y=55)
    
    # Configure progress bar
    progress_bar["maximum"] = total_steps
    
    # Progress Label
    progress_label = canvas.create_text(200, 100, text=f"0/{total_steps} completed", font=("Arial", 10))
    
    def update_progress(current_step):
        """Updates the progress bar and label."""
        progress_bar["value"] = current_step
        canvas.itemconfig(progress_label, text=f"{(current_step/total_steps)*100} completed")
        progress_window.update_idletasks()
        
        if current_step >= total_steps:
            if on_complete:
                on_complete()
            progress_window.destroy()
    
    # Return the update function for external control
    return update_progress

def get_video_capture():
    system = platform.system()
    if system == "Windows":
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow (faster on Windows)
    elif system == "Linux":
        return cv2.VideoCapture(0, cv2.CAP_V4L2)   # Video4Linux (common on Linux)
    elif system == "Darwin":  # macOS
        return cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # AVFoundation (macOS default)
    else:
        return cv2.VideoCapture(0)  # Fallback for unknown systems
#To fetch Name by refering id of the student
def fetch_name(id):
    with open("database/attendance_report/student_details.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == f"{id}":
                    return row[1]

# To create a file
def create_file(folderPath,fileName):
    if not (os.path.exists(f"{folderPath}")):
        os.makedirs(f"{folderPath}")
    new_file=open(f"{folderPath}/{fileName}","a")
    new_file.close()

# Student Portal Window
def studentPortal(root):
    root.destroy()
    StudentPortal_window = Tk()
    StudentPortal_window.iconbitmap("assets/windowIcon.ico")

    StudentPortal_window.title("Student Portal")
    StudentPortal_window.geometry("512x216")
    StudentPortal_window.configure(bg = "#FFFFFF")

    canvas = Canvas(
        StudentPortal_window,
        bg = "#FFFFFF",
        height = 216,
        width = 512,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        305.0,
        42.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        44.0,
        2.0,
        anchor="nw",
        text="Student Portal",
        fill="#FFFFFF",
        font=("Inter", 32 * -1)
    )

    button_1 = Button(StudentPortal_window,
        text="Mark Attendance",
        font=("Inter", 14),
        fg="black",
        bg="lightgrey",
        borderwidth=4,
        highlightthickness=4,
        command=lambda: markAttendance(StudentPortal_window),
        relief="raised"
    )
    button_1.place(
        x=23.0,
        y=61.0,
        width=260.0,
        height=40.0
    )


    button_2 = Button(StudentPortal_window,
        text="Register",
        font=("Inter", 14),
        fg="black",
        bg="lightgrey",
        borderwidth=4,
        highlightthickness=4,
        command=lambda: register(StudentPortal_window),
        relief="raised"
    )
    button_2.place(
        x=23.0,
        y=125.0,
        width=260.0,
        height=40.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("Student_Portal_Pic.png"))
    image_1 = canvas.create_image(
        408.0,
        94.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        0.0,
        188.0,
        512.0,
        216.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        32.0,
        193.0,
        anchor="nw",
        text="If you are a new user, Register before you Mark Attendance",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )
    StudentPortal_window.resizable(False, False)
    StudentPortal_window.mainloop()

# Register Window

def register(StudentPortal_window):
    def processRegistration(entry_1,entry_2,window):
        if not (os.path.isfile("database/trainer.yml")) :
            create_file("database","trainer.yml")
        if not(os.path.isfile("database/attendance_report/student_details.csv")):
            create_file("database/attendance_report","student_details.csv")
            with open("database/attendance_report/student_details.csv","a") as file:
                file.write("ID,Name\n")
        if not(os.path.exists("database/TrainingImages")):
            os.makedirs("database/TrainingImages")
        name=entry_1.get().strip().upper()
        id=entry_2.get().strip()
        if name=="" or id=="":
            messagebox.showerror("Empty Input","Both fields are required to Register")
            return
        if not(id.isdigit()):
            messagebox.showerror("Invalid Input","ID field requires a whole, non-negative numeric value")
            return
        user_found=False
        with open("database/attendance_report/student_details.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == id:
                    user_found=True
                    break
        if user_found:
            messagebox.showerror("Duplicate Registration","This ID is already registered")
            return
            
        window.destroy()
        messagebox.showwarning(
            "Things to Note",
            "Before registering your face, please ensure :\n"
            "    - Your environment is bright enough without\n      harsh shadows or excessive brightness.\n\n"
            "    - You are positioned at a comfortable distance\n      (neither too far nor too close).\n\n"
            "    - Keep your face straight and\n      avoid tilting too much or bending sideways.\n"
            "Follow these steps to ensure flawless registration. Thank you!"
        )

        cam = get_video_capture()
        detector = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

        captured_frames = []  # List to store the frames captured within the 1-minute duration
        face_samples=[] # List to store the squared gray scaled faces captured within the 1-minute duration
        ids=[] # List to store the ID value of the User

        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to capture image.")
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            # Draw rectangle around faces
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 7)
                captured_frames.append(face_img)
            
            # Display instructions and countdown timer
            cv2.putText(img, "Analyzing your face.. | Tilt your head slightly each way", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(img, f"Images Captured: {len(captured_frames)}/200 | Press 'Q' to force quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.imshow('Capturing Images', img)  # Display the frame
            
            # Exit conditions
            if len(captured_frames)>=200:
                # Release resources
                cam.release()
                cv2.destroyAllWindows()
                update=show_progress(len(captured_frames),"Saving Images","Saving the captured images, Please wait..")
                i=1
                # After capturing 300 frames, save all the captured frames
                for idx, frame in enumerate(captured_frames):
                        cv2.imwrite(f"database/TrainingImages/{idx}.{name}.{id}.jpg", frame)
                        update(i)
                        i=i+1
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                if messagebox.askyesno("Warning: Unsaved Progress","All progress will be lost. Do you want to force quit?\n\n[Note: If you choose 'No', click the 'Capturing Images' window again to resume interaction]"):
                    # Release resources
                    cam.release()
                    cv2.destroyAllWindows()
                    return
                else:
                    pass
          
        #Training the saved images
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        imagePaths = [os.path.join("database/TrainingImages", f) for f in os.listdir("database/TrainingImages")] # get the path of all the files in the folder
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L') # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[-2]) # getting the Id from the image
            face_samples.append(imageNp)# Directly append the face-cropped image
            ids.append(Id)

        recognizer.train(face_samples, np.array(ids))
        recognizer.save('database/trainer.yml')

        with open("database/attendance_report/student_details.csv","a") as file:
                file.write(f"{id},{name}\n")

        messagebox.showinfo("Success","Registration is successfully completed\nFrom now on, you can mark your attendance")
        

    Register_window = Toplevel(StudentPortal_window)
    Register_window.iconbitmap("assets/windowIcon.ico")
    Register_window.title("Student Register")
    Register_window.geometry("519x216")
    Register_window.configure(bg = "#FFFFFF")

    Register_window.grab_set()
    Register_window.protocol("WM_DELETE_WINDOW", lambda: [Register_window.grab_release(), Register_window.destroy()])

    canvas = Canvas(
        Register_window,
        bg = "#FFFFFF",
        height = 216,
        width = 519,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        519.0,
        51.0,
        fill="#000000",
        outline="")

    canvas.create_text(
        118.0,
        5.0,
        anchor="nw",
        text="Registration Form",
        fill="#FFFFFF",
        font=("Inter", 34 * -1)
    )

    canvas.create_text(
        34.0,
        66.0,
        anchor="nw",
        text="Name :",
        fill="#000000",
        font=("Inter", 25 * -1)
    )

    canvas.create_text(
        79.0,
        104.0,
        anchor="nw",
        text="ID :",
        fill="#000000",
        font=("Inter", 25 * -1)
    )

    entry_1 = Entry(Register_window,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    entry_1.place(
        x=131.0,
        y=68.0,
        width=236.0,
        height=24.0
    )

    entry_2 = Entry(Register_window,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 12)
    )
    entry_2.place(
        x=131.0,
        y=106.0,
        width=236.0,
        height=24.0
    )

    button_1 = Button(Register_window,
        text="REGISTER",
        font=("Inter", 12),
        fg="black",
        bg="lightgreen",
        borderwidth=3,
        highlightthickness=3,
        command=lambda: processRegistration(entry_1,entry_2,Register_window),
        relief="raised"
    )
    button_1.place(
        x=150.0,
        y=152.0,
        width=117.0,
        height=28.0
    )

    canvas.create_rectangle(
        0.0,
        199.0,
        519.0,
        216.0,
        fill="#000000",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("Face_Register_Pic.png"))
    image_1 = canvas.create_image(
        452.0,
        125.0,
        image=image_image_1
    )
    Register_window.resizable(False, False)
    Register_window.mainloop()

# Mark Attendance

def markAttendance(StudentPortal_window):
    if not (os.path.isfile("database/trainer.yml")) :
            create_file("database","trainer.yml")
    if os.path.getsize("database/trainer.yml")==0:
            messagebox.showerror("No Registered Users","No users are registered yet. Please register")
            return
    if not(messagebox.askyesno("Quick Question","Are you a Registered User?")):
            messagebox.showerror("Access Denied","Registration is required to mark your attendance.\nPlease register to proceed.")
            return
    messagebox.showwarning(
    "Things to Note",
    "Before marking attendance using the camera, please ensure :\n"
    "    - Your environment is bright enough without\n      harsh shadows or excessive brightness.\n\n"
    "    - You are positioned at a comfortable distance\n      (neither too far nor too close).\n\n"
    "    - Keep your face straight and\n      avoid tilting or bending sideways.\n"
    "Follow these steps to ensure accurate face recognition. Thank you!"
    )
    detector=None
    recognizer=None
    
    def init_components():
        nonlocal detector, recognizer
        detector = cv2.CascadeClassifier("assets/haarcascade_frontalface_default.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('database/trainer.yml')

    def faceRecognition(window = None):
        nonlocal detector,recognizer
        thread = threading.Thread(target=init_components)
        thread.start()
        if(window != None):
            window.destroy()

        cam = get_video_capture() # Initialize the camera
        details={}
        countdown_time = datetime.timedelta(seconds=30)  # Set the countdown time in seconds
        font = cv2.FONT_HERSHEY_SIMPLEX
        start_time = datetime.datetime.now()  # Start the countdown display and recognition process

        while True:
            ret, img = cam.read()
            elapsed_time = datetime.datetime.now() - start_time # Get the remaining time for the countdown
            remaining_time = (countdown_time - elapsed_time).total_seconds()

            # Show a message and the countdown
            cv2.putText(img, f"Trying to fetch details... | Press 'Q' to force quit", (10, 30), font, 0.7, (0, 0, 255), 2)
            cv2.putText(img, f"Time remaining: {int(remaining_time)}s", (10, 60), font, 0.7, (255, 0, 0), 2)

            # Process faces if detected
            if not(thread.is_alive()):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 7)
                    id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    cv2.putText(img,f"ID = {id_} Confidence = {conf:.2f}%", (x, y-40), font, 0.5, (0, 255, 0), 3)

                    if id_:  # Confidence threshold for face recognition
                        details["id"]=id_
                        details["dateNtime"]=datetime.datetime.now()
                        # Clean up and close
                        cam.release()
                        cv2.destroyAllWindows()
                        attendanceConfirmation(details)
                        return

            cv2.imshow('Face Recognition', img) # Display the video feed with the overlayed message
                    
            if remaining_time <= 0.9:
                if messagebox.askyesno("Recognition Failed","Failed to fetch your details. Do you want to retry?\n"):                    
                    # Clean up and close
                    cam.release()
                    cv2.destroyAllWindows()
                    faceRecognition()
                else:
                    if messagebox.askokcancel("Manual Attendance Request","Do you want to take Manual Attendance?"):
                        # Clean up and close
                        cam.release()
                        cv2.destroyAllWindows()
                        manualAttendance(details)
                break # Stop the process if time runs out

            elif cv2.waitKey(1) & 0xFF == ord("q"):
                break # force quit

        # Clean up and close
        cam.release()
        cv2.destroyAllWindows()

    #To save the data in CSV file

    def processAutoAttendance(window,details,combobox):
        if not(os.path.isfile("database/attendance_report/attendance_log.csv")):
            create_file("database/attendance_report","attendance_log.csv")
        details["subject"]=combobox.get()
        if details["subject"]=="Select subject":
            messagebox.showerror("Empty Input","Please choose any subject")
            return
        window.destroy()
        details['name']=fetch_name(details['id'])
        with open("database/attendance_report/attendance_log.csv","a") as file:
            fieldnames = ["Id", "Name","Subject","Date","Time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({"Id":details["id"],"Name":details["name"],"Subject":details["subject"],"Date":details["dateNtime"].strftime(f"%d-%m-%Y"),"Time":details["dateNtime"].strftime("%H:%M:%S")})
        messagebox.showinfo("Success","Attendance marked successfully")

    def manualAttendanceConfirmation(details,frame):
        ManualAttendanceConfirmation_window = Toplevel(StudentPortal_window)
        ManualAttendanceConfirmation_window.iconbitmap("assets/windowIcon.ico")

        ManualAttendanceConfirmation_window.title("Details Confirmation")
        ManualAttendanceConfirmation_window.geometry("521x272")
        ManualAttendanceConfirmation_window.configure(bg = "#FFFFFF")

        ManualAttendanceConfirmation_window.grab_set()
        ManualAttendanceConfirmation_window.protocol("WM_DELETE_WINDOW", lambda: [ManualAttendanceConfirmation_window.grab_release(), ManualAttendanceConfirmation_window.destroy()])

        canvas = Canvas(
            ManualAttendanceConfirmation_window,
            bg = "#FFFFFF",
            height = 272,
            width = 521,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            521.0,
            51.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            165.0,
            5.0,
            anchor="nw",
            text="Your Details",
            fill="#FFFFFF",
            font=("Inter", 34 * -1)
        )

        canvas.create_text(
            31.0,
            65.0,
            anchor="nw",
            text="Name :",
            fill="#000000",
            font=("Inter", 26 * -1)
        )

        canvas.create_text(
            19.0,
            155.0,
            anchor="nw",
            text="Subject :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            77.0,
            110.0,
            anchor="nw",
            text="ID :",
            fill="#000000",
            font=("Inter", 26 * -1)
        )

        canvas.create_text(
            131.0,
            67.0,
            anchor="nw",
            text="Anyx Namexxx",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            131.0,
            112.0,
            anchor="nw",
            text="Anyx Namexxx",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            131.0,
            156.0,
            anchor="nw",
            text="Anyx Namexxx",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        button_1 = Button(
            text="CONFIRM",
            font=("Inter", 12),
            fg="black",
            bg="lightgreen",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: [cv2.imwrite(f"database/manual_attendance_images/{details['id']}.{details['subject']}.{details['dateNtime'].strftime(f'%d-%m-%Y')}.{details['dateNtime'].strftime('%H:%M:%S')}.jpg", frame),ManualAttendanceConfirmation_window.destroy(), messagebox.showinfo("Verification in Progress","Your details have been submitted. Attendance will be marked upon verification.")],
            relief="raised"
        )
        button_1.place(
            x=42.0,
            y=204.0,
            width=116.0,
            height=27.0
        )

        button_2 = Button(
            text="RE-TAKE",
            font=("Inter", 12),
            fg="black",
            bg="lightcoral",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: [manualAttendance(details),ManualAttendanceConfirmation_window.destroy()],
            relief="raised"
        )
        button_2.place(
            x=179.0,
            y=204.0,
            width=105.0,
            height=27.0
        )

        canvas.create_rectangle(
            0.0,
            251.0,
            521.0,
            272.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            10.0,
            254.0,
            anchor="nw",
            text="Click “Confirm” to mark manual attendance | If your details are incorrect, click “Re-Take”",
            fill="#FFFFFF",
            font=("Inter", 13 * -1)
        )

        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            413.0,
            139.0,
            image=image_image_1
        )
        ManualAttendanceConfirmation_window.resizable(False, False)
        ManualAttendanceConfirmation_window.mainloop()

    def processManualAttendance(entry_1,entry_2,combobox,details,window):
        if not(os.path.isfile("database/attendance_report/attendance_log.csv")):
            create_file("database/attendance_report","attendance_log.csv")
        details["name"]=entry_1.get().strip().upper()
        details["id"]=entry_2.get().strip()
        details["subject"]=combobox.get()
        if details["name"]=="" or details["id"]=="" or details["subject"]=="Select subject":
            messagebox.showerror("Empty Input","All fields are required to mark Manual Attendance")
            return
        if not (details["id"].isdigit()):
            messagebox.showerror("Invalid Input","ID field requires a whole, non-negative numeric value")
            return
        user_found=False
        with open("database/attendance_report/student_details.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == details["id"]:
                    user_found=True
                    break
        if not user_found:
            messagebox.showerror("Identification Failed","This user doesn't exist. Please register or try another user")
            return 
        
        window.destroy()

        if not os.path.exists("database/manual_attendance_images"):
            os.makedirs("database/manual_attendance_images")
        messagebox.showwarning("Keep in Mind","Make sure you capture a clear photo of yourself\nto avoid identification issues")
        cam = get_video_capture()
        while True:
            ret, frame = cam.read()
            if ret:
                frame_copy = frame.copy()
            cv2.putText(frame, "Press 'C' to capture your photo", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Press 'Q' to quit and return to Manual Attendance Form", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            cv2.imshow('Capture Photo', frame)

            # Wait for the user to press 'c' to capture or 'q' to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                cam.release()
                cv2.destroyAllWindows()
                details["dateNtime"]=datetime.datetime.now()
                manualAttendanceConfirmation(details,frame_copy)
                return
            elif key == ord('q'):
                # Release the camera and close the window
                cam.release()
                cv2.destroyAllWindows()
                manualAttendance(details)
                break

    
# Manual Attendance Window

    def manualAttendance(details):
        ManualAttendance_window = Toplevel(StudentPortal_window)
        ManualAttendance_window.iconbitmap("assets/windowIcon.ico")

        ManualAttendance_window.title("Manual Attendance Form")
        ManualAttendance_window.geometry("516x269")
        ManualAttendance_window.configure(bg = "#FFFFFF")

        ManualAttendance_window.grab_set()
        ManualAttendance_window.protocol("WM_DELETE_WINDOW", lambda: [ManualAttendance_window.grab_release(), ManualAttendance_window.destroy()])

        canvas = Canvas(
            ManualAttendance_window,
            bg = "#FFFFFF",
            height = 269,
            width = 516,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            516.0,
            48.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            87.0,
            7.0,
            anchor="nw",
            text="Manual Attendance Form",
            fill="#FFFFFF",
            font=("Inter", 29 * -1)
        )

        canvas.create_text(
            36.0,
            70.0,
            anchor="nw",
            text="Name :",
            fill="#000000",
            font=("Inter", 29 * -1)
        )

        canvas.create_text(
            88.0,
            112.0,
            anchor="nw",
            text="ID :",
            fill="#000000",
            font=("Inter", 29 * -1)
        )

        canvas.create_text(
            13.0,
            150.0,
            anchor="nw",
            text="Subject :",
            fill="#000000",
            font=("Inter", 29 * -1)
        )

        entry_1 = Entry(ManualAttendance_window,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 12)
        )
        entry_1.place(
            x=142.0,
            y=73.0,
            width=213.0,
            height=26.0
        )

        entry_2 = Entry(ManualAttendance_window,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 12)
        )
        entry_2.place(
            x=142.0,
            y=115.0,
            width=213.0,
            height=26.0
        )


        options = ["Mathematics","Physics","Chemistry"]
        # Create a Combobox with the specified size and coordinates
        combobox = Combobox(ManualAttendance_window, values=options, state="readonly", font=("Inter",12))
        combobox.set("Select subject")  # Default option

        combobox.place(
            x = 142.0,
            y = 154.0,
            width = 213.0,
            height = 28.0
        )

        button_1 = Button(ManualAttendance_window,
            text="TAKE PHOTO",
            font=("Inter", 14),
            fg="black",
            bg="lightgreen",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: processManualAttendance(entry_1,entry_2,combobox,details,ManualAttendance_window),
            relief="raised"
        )
        button_1.place(
            x=167.0,
            y=200.0,
            width=183.0,
            height=31.0
        )


        canvas.create_rectangle(
            0.0,
            249.0,
            516.0,
            269.0,
            fill="#000000",
            outline="")

        image_image_1 = PhotoImage(
            file=relative_to_assets("Manual_Attendance_Logo.png"))
        image_1 = canvas.create_image(
            439.0,
            132.0,
            image=image_image_1
        )
        ManualAttendance_window.resizable(False, False)
        ManualAttendance_window.mainloop()

    def manualAttendanceConfirmation(details,frame):
        frame_resized = cv2.resize(frame, (188, 141))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(frame_rgb) # Convert the frame to a PIL Image
        image_tk = ImageTk.PhotoImage(image_pil) # Convert PIL Image to PhotoImage

        ManualAttendanceConfirmation_window = Toplevel(StudentPortal_window)
        ManualAttendanceConfirmation_window.iconbitmap("assets/windowIcon.ico")

        ManualAttendanceConfirmation_window.title("Details Confirmation")
        ManualAttendanceConfirmation_window.geometry("521x272")
        ManualAttendanceConfirmation_window.configure(bg = "#FFFFFF")

        ManualAttendanceConfirmation_window.grab_set()
        ManualAttendanceConfirmation_window.protocol("WM_DELETE_WINDOW", lambda: [ManualAttendanceConfirmation_window.grab_release(), ManualAttendanceConfirmation_window.destroy()])

        canvas = Canvas(
            ManualAttendanceConfirmation_window,
            bg = "#FFFFFF",
            height = 272,
            width = 521,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            521.0,
            51.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            165.0,
            5.0,
            anchor="nw",
            text="Your Details",
            fill="#FFFFFF",
            font=("Inter", 34 * -1)
        )

        canvas.create_text(
            31.0,
            65.0,
            anchor="nw",
            text="Name :",
            fill="#000000",
            font=("Inter", 26 * -1)
        )

        canvas.create_text(
            19.0,
            155.0,
            anchor="nw",
            text="Subject :",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            77.0,
            110.0,
            anchor="nw",
            text="ID :",
            fill="#000000",
            font=("Inter", 26 * -1)
        )

        canvas.create_text(
            131.0,
            67.0,
            anchor="nw",
            text=f"{details['name']}",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            131.0,
            112.0,
            anchor="nw",
            text=f"{details['id']}",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        canvas.create_text(
            131.0,
            156.0,
            anchor="nw",
            text=f"{details['subject']}",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        button_1 = Button(ManualAttendanceConfirmation_window,
            text="CONFIRM",
            font=("Inter", 12),
            fg="black",
            bg="lightgreen",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: [cv2.imwrite(f"database/manual_attendance_images/{details['id']}.{details['subject']}.{details['dateNtime'].strftime(f'%d-%m-%Y')}.{details['dateNtime'].strftime('%H-%M-%S')}.jpg", frame),ManualAttendanceConfirmation_window.destroy(), messagebox.showinfo("Verification in Progress","Your details have been submitted.\nAttendance will be marked upon verification.")],
            relief="raised"
        )
        button_1.place(
            x=42.0,
            y=204.0,
            width=116.0,
            height=27.0
        )

        button_2 = Button(ManualAttendanceConfirmation_window,
            text="RE-TAKE",
            font=("Inter", 12),
            fg="black",
            bg="lightcoral",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: [ManualAttendanceConfirmation_window.destroy(),manualAttendance(details)],
            relief="raised"
        )
        button_2.place(
            x=179.0,
            y=204.0,
            width=105.0,
            height=27.0
        )

        canvas.create_rectangle(
            0.0,
            251.0,
            521.0,
            272.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            10.0,
            254.0,
            anchor="nw",
            text="Click “Confirm” to mark manual attendance | If your details are incorrect, click “Re-Take”",
            fill="#FFFFFF",
            font=("Inter", 13 * -1)
        )

        image_1 = canvas.create_image(
            413.0,
            139.0,
            image=image_tk
        )
        ManualAttendanceConfirmation_window.resizable(False, False)
        ManualAttendanceConfirmation_window.mainloop()
        
# Attendance Confirmation Window

    def attendanceConfirmation(details):

        AttendanceConfirmation_window = Toplevel(StudentPortal_window)
        AttendanceConfirmation_window.iconbitmap("assets/windowIcon.ico")

        AttendanceConfirmation_window.title("Details Confirmation")
        AttendanceConfirmation_window.geometry("558x324")
        AttendanceConfirmation_window.configure(bg = "#FFFFFF")

        AttendanceConfirmation_window.grab_set()
        AttendanceConfirmation_window.protocol("WM_DELETE_WINDOW", lambda: [AttendanceConfirmation_window.grab_release(), AttendanceConfirmation_window.destroy()])


        canvas = Canvas(
            AttendanceConfirmation_window,
            bg = "#FFFFFF",
            height = 324,
            width = 558,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            558.0,
            52.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            143.0,
            2.0,
            anchor="nw",
            text="Your Details",
            fill="#FFFFFF",
            font=("Inter", 40 * -1)
        )

        canvas.create_text(
            37.0,
            60.0,
            anchor="nw",
            text="Name :",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            87.0,
            104.0,
            anchor="nw",
            text="ID :",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            14.0,
            148.0,
            anchor="nw",
            text="Subject :",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            157.0,
            60.0,
            anchor="nw",
            text=fetch_name(details["id"]),
            fill="#000000",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            157.0,
            104.0,
            anchor="nw",
            text=f"{details['id']}",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

        options = ["Mathematics", "Chemistry", "Physics"] # Dropdown options

        combobox = Combobox(AttendanceConfirmation_window, values=options, state="readonly", font=("Inter",12))
        combobox.set("Select subject")  # Default option

        combobox.place(
            x=159.0,
            y=153.0,
            width=170.0,
            height=31.0
        )


        canvas.create_text(
            157.0,
            184.0,
            anchor="nw",
            text="*please choose a subject*",
            fill="#FF0000",
            font=("Inter", 14 * -1)
        )

        button_1 = Button(AttendanceConfirmation_window,
            text="CONFIRM",
            font=("Inter", 12,),
            fg="black",
            bg="lightgreen",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: processAutoAttendance(AttendanceConfirmation_window,details,combobox),
            relief="raised"
        )
        button_1.place(
            x=27.0,
            y=230.0,
            width=117.0,
            height=36.0
        )

        button_2 = Button(AttendanceConfirmation_window,
            text="TAKE MANUAL ATTENDANCE",
            font=("Inter", 11,),
            fg="black",
            bg="lightcoral",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: [AttendanceConfirmation_window.destroy(),manualAttendance(details)],
            relief="raised"
        )
        button_2.place(
            x=271.0,
            y=230.0,
            width=262.0,
            height=36.0
        )

        button_3 = Button(AttendanceConfirmation_window,
            text="RE-TRY",
            font=("Inter", 12,),
            fg="black",
            bg="lightgrey",
            borderwidth=3,
            highlightthickness=3,
            command=lambda: faceRecognition(AttendanceConfirmation_window),
            relief="raised"
        )
        button_3.place(
            x=159.0,
            y=230.0,
            width=97.0,
            height=36.0
        )

        canvas.create_rectangle(
            0.0,
            283.0,
            558.0,
            324.0,
            fill="#000000",
            outline="")

        image_image_1 = PhotoImage(
            file=relative_to_assets("User_Info_Logo.png"))
        image_1 = canvas.create_image(
            444.0,
            141.0,
            image=image_image_1
        )

        canvas.create_text(
            35.0,
            285.0,
            anchor="nw",
            text="Click “Confirm” to mark attendance | If your details are incorrect,\n either re-try or take manual attendance",
            fill="#FFFFFF",
            font=("Inter", 16 * -1)
        )
        AttendanceConfirmation_window.resizable(False, False)
        AttendanceConfirmation_window.mainloop()

    faceRecognition() # tries to recognize the face first