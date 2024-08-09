from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from database_connect import mycursor
from database_connect import con
import subprocess

def check():
    query = 'SELECT * FROM login WHERE squestion=%s AND answer=%s'
    mycursor.execute(query, (squestion_input.get(), answer_input.get()))
    row = mycursor.fetchone()

    if row is None:
        messagebox.showerror('Error', 'Invalid question or answer')
    else:
        root.destroy()
        import resetpass

def go_back():
    root.destroy()
    subprocess.run(["python", "login.py"])

root = Tk()
root.title("Question Paper Generator")

# Make the window full screen
root.attributes('-fullscreen', True)

# Get screen width and height for dynamic image resizing
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set background image
bg_image = Image.open('3.png')
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Frame for form
form_frame = Frame(root, bg='#FCFFF9', bd=10)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=600, height=400)

# Title label
title_label = Label(form_frame, text="Security Question", font=('TIMES NEW ROMAN', 24, 'bold'), bg='#FCFFF9', fg='black')
title_label.pack(pady=20)

# Security question
squestion_label = Label(form_frame, text='Security Question:', font=('TIMES NEW ROMAN', 20), bg='#FCFFF9', fg='black')
squestion_label.pack(pady=10)
squestion_input = ttk.Combobox(form_frame, width=50, values=[
    "What is the name of your first school?",
    "What is your favourite movie?",
    "What is your favourite animal?"
])
squestion_input.pack()

# Answer
answer_label = Label(form_frame, text="Answer: ", bg='#FCFFF9', fg='black', font=('TIMES NEW ROMAN', 20))
answer_label.pack(pady=10)
answer_input = Entry(form_frame, bg='white', font=('Lucida Fax', 14))
answer_input.pack()

# Submit button
submit_button = Button(form_frame, text="SUBMIT", width=20, bg='blue', fg='white', font=('Copperplate Gothic Bold', 14, 'bold'), cursor='hand2', command=check)
submit_button.pack(pady=20)

# Back button
back_button = Button(form_frame, text="BACK", width=20, bg='red', fg='white', font=('Copperplate Gothic Bold', 14, 'bold'), cursor='hand2', command=go_back)
back_button.pack(pady=10)

root.mainloop()
