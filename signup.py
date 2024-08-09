from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk
import pymysql
import hashlib
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def login_page():
    signup_window.destroy()
    import login

def emailcheck(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return 1
    else:
        return 0

def passcheck(password):
    if len(password) < 8:
        return 0
    elif not re.search("[A-Z]", password):
        return 0
    elif not re.search("[a-z]", password):
        return 0
    elif not re.search("[0-9]", password):
        return 0
    elif not re.search("[_@$#%-+/!^&*]", password):
        return 0
    else:
        return 1

def encryption(password):
    h = hashlib.new("SHA256")
    h.update(password.encode())
    return h.hexdigest()

def send_email(email, name, password, sec_password):
    try:
        sender_email = "automaticquestiongenarate24@gmail.com"
        sender_password = "cwqm jjej ulgk oibg"
        receiver_email = email

        message = MIMEMultipart("alternative")
        message["Subject"] = "Signup Confirmation"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = (f"Hello {name},\n\nYour account has been created successfully.\n\n"
                f"Your details are as follows:\n\n"
                f"Name: {name}\n"
                f"Password: {password}\n"
                f"Security Password: {sec_password}\n\n"
                f"Best regards,\nTeam QUESTION CRAFT")
        part = MIMEText(text, "plain")

        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        messagebox.showinfo('Success', 'Confirmation email sent successfully!')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to send email: {e}')

def connect_database():
    if (email_input.get() == '' or name_input.get() == '' or mob_input.get() == '' or
        password_input.get() == '' or Confirm_password_input.get() == '' or
        squestion_input.get() == '' or answer_input.get() == '' or
        sec_password_input.get() == '' or confirm_sec_password_input.get() == ''):
        messagebox.showerror('Error', 'All Fields are Required...')
    elif password_input.get() != Confirm_password_input.get():
        messagebox.showerror('Error', 'Password Mismatch...')
    elif sec_password_input.get() != confirm_sec_password_input.get():
        messagebox.showerror('Error', 'Security Password Mismatch...')
    else:
        try:
            from database_connect import mycursor
            from database_connect import con

            echeck = emailcheck(email_input.get())
            if echeck == 0:
                messagebox.showerror("Error", "Invalid Email Format")
                return

            pcheck = passcheck(password_input.get())
            if pcheck == 0:
                messagebox.showerror("Error", "Invalid Password Format")
                return

            if len(mob_input.get()) != 10:
                messagebox.showerror("Error", "Invalid Mobile number")
                return

            # Check if email already exists
            query_check_email = 'SELECT email FROM login WHERE email = %s'
            mycursor.execute(query_check_email, (email_input.get(),))
            if mycursor.fetchone():
                messagebox.showerror("Error", "User already exists with this email")
                return

            # Check if mobile number already exists
            query_check_mobile = 'SELECT mob_no FROM login WHERE mob_no = %s'
            mycursor.execute(query_check_mobile, (mob_input.get(),))
            if mycursor.fetchone():
                messagebox.showerror("Error", "User already exists with this mobile number")
                return

            # Check if username already exists
            query_check_username = 'SELECT username FROM login WHERE username = %s'
            mycursor.execute(query_check_username, (name_input.get(),))
            if mycursor.fetchone():
                messagebox.showerror("Error", "User already exists with this username")
                return

            # Insert new user
            query = 'INSERT INTO login (email, username, password, mob_no, squestion, answer, sec_password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            encrypted_password = encryption(password_input.get())
            encrypted_sec_password = encryption(sec_password_input.get())
            mycursor.execute(query, (email_input.get(), name_input.get(), encrypted_password, mob_input.get(), squestion_input.get(), answer_input.get(), encrypted_sec_password))

            con.commit()
            con.close()

            send_email(email_input.get(), name_input.get(), password_input.get(), sec_password_input.get())
            messagebox.showinfo('Success', 'Account created successfully!')
            login_page()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Error: {e}')

def info():
    messagebox.showinfo("Password Rules", "1. Not less than 8 characters\n2. At least one Uppercase character\n3. At least one lowercase character\n4. At least one digit\n5. At least one special character (_ @ $ # % - + / ! ^ & *)")

def user_enter(event):
    if name_input.get() == 'Name':
        name_input.delete(0, END)

def email_enter(event):
    if email_input.get() == 'Email':
        email_input.delete(0, END)

def mob_enter(event):
    if mob_input.get() == 'Mobile No.':
        mob_input.delete(0, END)

def password_enter(event):
    if password_input.get() == 'Password':
        password_input.delete(0, END)

def confirm_password_enter(event):
    if Confirm_password_input.get() == 'Confirm Password':
        Confirm_password_input.delete(0, END)

def answer_enter(event):
    if answer_input.get() == 'Answer':
        answer_input.delete(0, END)

def sec_password_enter(event):
    if sec_password_input.get() == 'Security Password':
        sec_password_input.delete(0, END)

def confirm_sec_password_enter(event):
    if confirm_sec_password_input.get() == 'Confirm Security Password':
        confirm_sec_password_input.delete(0, END)

def hide():
    closeeye.config(file='closeye.png')
    password_input.config(show='*')
    closeButton.config(command=show)

# Function to show password
def show():
    closeeye.config(file='openeye.png')
    password_input.config(show='')
    closeButton.config(command=hide)

def hide2():
    closeeye2.config(file='closeye2.png')
    sec_password_input.config(show='*')
    closeButton2.config(command=show2)

# Function to show password
def show2():
    closeeye2.config(file='openeye2.png')
    sec_password_input.config(show='')
    closeButton2.config(command=hide2)

def info():
    messagebox.showinfo("Password Rules","1. Not less than 8 characters\n2. Atleast one Uppercase character\n3. Atleast one lowercase character\n4. Atleast one digit\n5. Atleast special character (_ @ $ # % - + / ! ^ & *)")

signup_window = Tk()
signup_window.title('Question Paper Generator')
signup_window.geometry("1920x1080")

bgImage = ImageTk.PhotoImage(file='6.png')
bgLabel = Label(signup_window, image=bgImage)
bgLabel.pack()

heading = Label(signup_window, text='CREATE ACCOUNT', font=('Bookman old style', 28, 'bold'), bg='white', fg='black')
heading.place(x=565, y=120)

# Create a style for the darker separator
style = ttk.Style()
style.configure("TSeparator", background="black")

# Entry Fields
name_label = Label(signup_window, text='Name:', font=('Helvetica', 14), bg='white')
name_label.place(x=570, y=205)
name_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
name_input.place(x=700, y=205)
name_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
name_separator.place(x=700, y=230, width=250)

email_label = Label(signup_window, text='Email:', font=('Helvetica', 14), bg='white')
email_label.place(x=570, y=255)
email_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
email_input.place(x=700, y=255)
email_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
email_separator.place(x=700, y=280, width=250)

mob_label = Label(signup_window, text='Mobile No.:', font=('Helvetica', 14), bg='white')
mob_label.place(x=570, y=305)
mob_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
mob_input.place(x=700, y=305)
mob_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
mob_separator.place(x=700, y=330, width=250)

password_label = Label(signup_window, text='Password:', font=('Helvetica', 14), bg='white')
password_label.place(x=570, y=355)
password_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
password_input.config(show='*')
password_input.place(x=700, y=355)
password_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
password_separator.place(x=700, y=385, width=250)

closeeye = PhotoImage(file='closeye.png')
closeButton = Button(signup_window, image=closeeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=show)
closeButton.place(x=930, y=355)

infob = PhotoImage(file='ibutton.png')
ibutton = Button(signup_window, image=infob, bd=1, bg='#e1e1e1', activebackground='#e1e1e1', cursor='hand2', command=info)
ibutton.place(x=960, y=355)

Confirm_password_label = Label(signup_window, text='Confirm\nPassword:', font=('Helvetica', 14), bg='white')
Confirm_password_label.place(x=570, y=405)
Confirm_password_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
Confirm_password_input.config(show='*')
Confirm_password_input.place(x=700, y=405)
Confirm_password_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
Confirm_password_separator.place(x=700, y=435, width=250)

sec_password_label = Label(signup_window, text='Security\nPassword:', font=('Helvetica', 14), bg='white')
sec_password_label.place(x=570, y=455)
sec_password_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
sec_password_input.config(show='*')
sec_password_input.place(x=700, y=455)
sec_password_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
sec_password_separator.place(x=700, y=485, width=250)

closeeye2 = PhotoImage(file='closeye2.png')
closeButton2 = Button(signup_window, image=closeeye2, bd=0, bg='white', activebackground='white', cursor='hand2', command=show2)
closeButton2.place(x=930, y=455)

infob2 = PhotoImage(file='ibutton.png')
ibutton = Button(signup_window, image=infob, bd=1, bg='#e1e1e1', activebackground='#e1e1e1', cursor='hand2', command=info)
ibutton.place(x=960, y=455)

confirm_sec_password_label = Label(signup_window, text='Confirm\nSecurity:\nPassword', font=('Helvetica', 14), bg='white')
confirm_sec_password_label.place(x=570, y=505)
confirm_sec_password_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
confirm_sec_password_input.config(show='*')
confirm_sec_password_input.place(x=705, y=505)
confirm_sec_password_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
confirm_sec_password_separator.place(x=705, y=530, width=250)

squestion_label = Label(signup_window, text='Security Question:', font=('Helvetica', 14), bg='white')
squestion_label.place(x=570, y=575)
squestion_input = ttk.Combobox(signup_window, width=24, font=('Helvetica', 14))
squestion_input['values'] = ("Select", "What is your first school?", "What is your favourite movie?", "What is your favourite animal?")
squestion_input.place(x=730, y=575)
squestion_input.current(0)

answer_label = Label(signup_window, text='Answer:', font=('Helvetica', 14), bg='white')
answer_label.place(x=570, y=615)
answer_input = Entry(signup_window, width=25, font=('Helvetica', 14), bd=0, fg='gray1')
answer_input.place(x=700, y=615)
answer_separator = ttk.Separator(signup_window, orient='horizontal', style="TSeparator")
answer_separator.place(x=700, y=640, width=250)

# Add event bindings
name_input.bind('<FocusIn>', user_enter)
email_input.bind('<FocusIn>', email_enter)
mob_input.bind('<FocusIn>', mob_enter)
password_input.bind('<FocusIn>', password_enter)
Confirm_password_input.bind('<FocusIn>', confirm_password_enter)
answer_input.bind('<FocusIn>', answer_enter)
sec_password_input.bind('<FocusIn>', sec_password_enter)
confirm_sec_password_input.bind('<FocusIn>', confirm_sec_password_enter)

# Create Account Button with black outline
signup_button = Button(signup_window, text='Create Account', font=('Open Sans', 16, 'bold'), fg='white', bg='gray1',
                       activeforeground='white', activebackground='gray1', cursor='hand2', bd=0, width=19, command=connect_database)
signup_button.place(x=650, y=675)

signup_window.mainloop()
