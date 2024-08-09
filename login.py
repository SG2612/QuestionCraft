import pymysql
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import hashlib
import random
import string

# Encryption handling
def encryption(password):
    h = hashlib.new("SHA256")
    h.update(password.encode())
    epass = h.hexdigest()
    return epass

# Function to generate CAPTCHA
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    font = ImageFont.truetype("arial.ttf", 40)
    image = Image.new('RGB', (200, 100), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), captcha_text, font=font, fill='black')
    image.save('captcha.png')
    return captcha_text

# Function to refresh CAPTCHA
def refresh_captcha():
    global captcha_text, captchaImage
    captcha_text = generate_captcha()
    captchaImage = ImageTk.PhotoImage(file='captcha.png')
    captchaLabel.config(image=captchaImage)

# Function to handle user login
def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '' or captchaEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif captchaEntry.get() != captcha_text:
        messagebox.showerror('Error', 'Invalid CAPTCHA')
    else:
        try:
            # Establishing connection to the database
            from database_connect import mycursor
            from database_connect import con

            password = encryption(passwordEntry.get())
            # Executing select query with parameters
            query = 'SELECT * FROM login WHERE username=%s AND password=%s'
            mycursor.execute(query, (usernameEntry.get(), password))
            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror('Error', 'Invalid username or password')
            else:
                messagebox.showinfo('Welcome', 'Login successful')
                login_window.destroy()
                import mainpage

            # Commit changes and close connection
            con.commit()
            con.close()

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error: {str(e)}')

# Function to switch to the signup page
def signup_page():
    login_window.destroy()
    import signup

def resetpass_page():
    login_window.destroy()
    import forgotpass

# Function to hide password
def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

# Function to show password
def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

# Function to handle when user enters username
def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

# Function to handle when user enters password
def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

# Function to handle when user enters CAPTCHA
def captcha_enter(event):
    if captchaEntry.get() == 'Enter CAPTCHA':
        captchaEntry.delete(0, END)

# Function to exit the application
def exit_app():
    login_window.destroy()

# Generate CAPTCHA
captcha_text = generate_captcha()

# GUI
login_window = Tk()
login_window.title('Question Paper Generator')
login_window.geometry("1920x1080")
# Make the window fullscreen
#login_window.attributes('-fullscreen', True)

bgImage = ImageTk.PhotoImage(file='6.png')
bgLabel = Label(login_window, image=bgImage)
bgLabel.pack(fill=BOTH, expand=True)

# Adding a Frame for better layout management
frame = Frame(login_window, bg='white')
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

heading = Label(frame, text='USER LOGIN', font=('Bookman old style', 23, 'bold'), bg='white')
heading.grid(row=0, column=0, columnspan=2, pady=20)

usernameEntry = Entry(frame, width=25, font=('Helvetica', 11, 'bold'), bd=0, fg='gray1')
usernameEntry.grid(row=1, column=0, columnspan=2, pady=10)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

Frame1 = Frame(frame, width=250, height=2, bg='gray1')
Frame1.grid(row=2, column=0, columnspan=2)

passwordEntry = Entry(frame, width=25, font=('Helvetica', 11, 'bold'), bd=0, fg='gray1')
passwordEntry.grid(row=3, column=0, columnspan=2, pady=10)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

Frame2 = Frame(frame, width=250, height=2, bg='gray1')
Frame2.grid(row=4, column=0, columnspan=2)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(frame, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.grid(row=3, column=1, sticky='e', padx=5)

captchaImage = ImageTk.PhotoImage(file='captcha.png')
captchaLabel = Label(frame, image=captchaImage, bg='white')
captchaLabel.grid(row=5, column=0, columnspan=2, pady=10)

captchaEntry = Entry(frame, width=25, font=('Helvetica', 11, 'bold'), bd=0, fg='gray1')
captchaEntry.grid(row=6, column=0, columnspan=2, pady=10)
captchaEntry.insert(0, 'Enter CAPTCHA')
captchaEntry.bind('<FocusIn>', captcha_enter)

Frame3 = Frame(frame, width=250, height=2, bg='gray1')
Frame3.grid(row=7, column=0, columnspan=2)

# Add refresh CAPTCHA button
refreshButton = Button(frame, text='Refresh CAPTCHA', bd=0, bg='white', activebackground='white', cursor='hand2',
                       font=('Helvetica', 12, 'bold'), fg='gray1', command=refresh_captcha)
refreshButton.grid(row=8, column=0, columnspan=2, pady=5)

forgetButton = Button(frame, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2',
                      font=('Helvetica', 12, 'bold'), fg='gray1', command=resetpass_page)
forgetButton.grid(row=9, column=0, columnspan=2, pady=5)

loginButton = Button(frame, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='gray1',
                     activeforeground='white', activebackground='gray1', cursor='hand2', bd=0, width=19, command=login_user)
loginButton.grid(row=10, column=0, columnspan=2, pady=20)

#signupLabel = Label(frame, text='Don\'t have an account?', font=('Open Sans', 12, 'bold'), fg='gray2', bg='white')
#signupLabel.grid(row=11, column=0, columnspan=2, pady=5)

#newaccountButton = Button(frame, text='Create new account', font=('Open Sans', 12, 'bold underline'), fg='blue', bg='white',
 #                         activeforeground='blue', activebackground='white', cursor='hand2', bd=0, command=signup_page)
#newaccountButton.grid(row=12, column=0, columnspan=2, pady=10)

# Add exit button
exitButton = Button(frame, text='Exit', font=('Open Sans', 12, 'bold'), fg='red', bg='white',
                    activeforeground='red', activebackground='white', cursor='hand2', bd=0, command=exit_app)
exitButton.grid(row=13, column=0, columnspan=2, pady=10)

login_window.mainloop()
