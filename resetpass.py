from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import pymysql
import hashlib
import re
import subprocess

def passcheck(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[_@$#%-+/!^&*]", password):
        return False
    return True

def encryption(password):
    h = hashlib.new("SHA256")
    h.update(password.encode())
    return h.hexdigest()

def reset():
    if mob_input.get() == '' or password_input.get() == '' or confirm_password_input.get() == '':
        messagebox.showerror('Error', 'All Fields are Required...')
    elif password_input.get() != confirm_password_input.get():
        messagebox.showerror('Error', 'Password Mismatch...')
    else:
        try:
            from database_connect import mycursor
            from database_connect import con

            if not passcheck(password_input.get()):
                messagebox.showerror("Error", "Invalid Password Format")
                return

            hashpass = encryption(password_input.get())
            mobile = mob_input.get()
            query = 'UPDATE login SET password=%s WHERE mob_no=%s'
            mycursor.execute(query, (hashpass, mobile))

            con.commit()
            con.close()

            messagebox.showinfo('Success', 'Password changed successfully!')
            root.destroy()
            import login

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Error: {e}')

def info():
    messagebox.showinfo("Password Rules",
                        "1. Not less than 8 characters\n2. At least one uppercase character\n3. At least one lowercase character\n4. At least one digit\n5. At least one special character (_ @ $ # % - + / ! ^ & *)")

def hide():
    closeye.config(file='closeye.png')
    password_input.config(show='*')
    eyeButton.config(command=show)

def show():
    closeye.config(file='openeye.png')
    password_input.config(show='')
    eyeButton.config(command=hide)

def go_back():
    root.destroy()
    subprocess.run(["python", "forgotpass.py"])

root = Tk()
root.title('Reset Password')

# Make the window full screen
root.attributes('-fullscreen', True)

bg_image = Image.open('3.png')
bg_image = bg_image.resize((1680, 1050))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

form_frame = Frame(root, bg='#FCFFF9', bd=10)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=700, height=500)

title_label = Label(form_frame, text="Reset Password", font=('TIMES NEW ROMAN', 24, 'bold'), bg='#FCFFF9', fg='black')
title_label.pack(pady=20)

mob_label = Label(form_frame, text="Mobile No.", bg='#FCFFF9', fg='black', font=('times new roman', 20))
mob_label.pack(pady=10)
mob_input = Entry(form_frame, bg='white', font=('Lucida Fax', 14))
mob_input.pack()

password_label = Label(form_frame, text="New Password", bg='#FCFFF9', fg='black', font=('times new roman', 20))
password_label.pack(pady=10)
password_input = Entry(form_frame, bg='white', font=('Lucida Fax', 14), show='*')
password_input.pack()

closeye = PhotoImage(file='closeye.png')
eyeButton = Button(form_frame, image=closeye, bd=-1, bg='#FCFFF9', activebackground='#FCFFF9', cursor='hand2',
                   command=show)
eyeButton.place(x=620, y=215)

infob = PhotoImage(file='ibutton.png')
ibutton = Button(form_frame, image=infob, bd=-1, bg='#FCFFF9', activebackground='#FCFFF9', cursor='hand2', command=info)
ibutton.place(x=660, y=215)

confirm_password_label = Label(form_frame, text="Confirm Password", bg='#FCFFF9', fg='black',
                               font=('times new roman', 20))
confirm_password_label.pack(pady=10)
confirm_password_input = Entry(form_frame, bg='white', font=('Lucida Fax', 14), show='*')
confirm_password_input.pack()

button = Button(form_frame, text="RESET", width=20, bg='blue', fg='white', font=('Copperplate Gothic Bold', 14, 'bold'),
                cursor='hand2', command=reset)
button.pack(pady=20)

back_button = Button(form_frame, text="BACK", width=20, bg='red', fg='white', font=('Copperplate Gothic Bold', 14, 'bold'),
                     cursor='hand2', command=go_back)
back_button.pack(pady=10)

root.mainloop()
