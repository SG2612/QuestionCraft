from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
import hashlib


def generate():
    root.destroy()
    import generating


def add():
    root.destroy()
    import adding


def edit():
    def check_sec_password():
        entered_password = sec_password_entry.get()
        hashed_password = encryption(entered_password)

        try:
            from database_connect import mycursor

            # Fetch the hashed security password from the database
            query = 'SELECT sec_password FROM login'
            mycursor.execute(query)
            stored_hashed_password = mycursor.fetchone()

            if stored_hashed_password and stored_hashed_password[0] == hashed_password:
                sec_password_window.destroy()
                root.destroy()
                import editing
            else:
                messagebox.showerror('Error', 'Incorrect Security Password')

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database Error: {e}')

    sec_password_window = Toplevel(root)
    sec_password_window.title('Enter Security Password')
    sec_password_window.geometry('400x200')

    Label(sec_password_window, text='Enter Security Password', font=('Open Sans', 14)).pack(pady=20)
    sec_password_entry = Entry(sec_password_window, font=('Open Sans', 14), show='*')
    sec_password_entry.pack(pady=10)
    Button(sec_password_window, text='Submit', font=('Open Sans', 14), command=check_sec_password).pack(pady=10)


def exit_app():
    root.destroy()


def encryption(password):
    h = hashlib.new("SHA256")
    h.update(password.encode())
    return h.hexdigest()


root = Tk()
root.title('Question Paper Generator')
root.geometry('1680x1050')
# root.attributes('-fullscreen', True)
bgImage = ImageTk.PhotoImage(file='3.png')
bgLabel = Label(root, image=bgImage)
bgLabel.pack()

generate_button = Button(root, text='Generate Question Paper', font=('Open Sans', 16, 'bold'), fg='white', bg='gray1',
                         activeforeground='white', activebackground='gray1', cursor='hand2', bd=0, width=25,
                         command=generate)
generate_button.place(x=602, y=200)

add_button = Button(root, text='Add Question', font=('Open Sans', 16, 'bold'), fg='white', bg='gray1',
                    activeforeground='white', activebackground='gray1', cursor='hand2', bd=0, width=25, command=add)
add_button.place(x=602, y=300)

edit_button = Button(root, text='View and Edit Questions', font=('Open Sans', 16, 'bold'), fg='white', bg='gray1',
                     activeforeground='white', activebackground='gray1', cursor='hand2', bd=0, width=25, command=edit)
edit_button.place(x=602, y=400)

exit_button = Button(root, text='Exit', font=('Open Sans', 16, 'bold'), fg='white', bg='red', activeforeground='white',
                     activebackground='red', cursor='hand2', bd=0, width=25, command=exit_app)
exit_button.place(x=602, y=500)

root.mainloop()
