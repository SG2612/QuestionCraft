import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

def fetch_questions(class_val, subject_val):
    try:
        print("Connecting to database...")
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="krishnendu@2003",
            database="project"
        )
        print("Connection successful")
        cursor = conn.cursor()
        query = f"SELECT question FROM {subject_val} WHERE class=%s"
        cursor.execute(query, (class_val,))
        rows = cursor.fetchall()
    except pymysql.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        rows = []
    finally:
        cursor.close()
        conn.close()
    return rows

def view_questions():
    for widget in view_frame.winfo_children():
        widget.destroy()

    class_val = class_combobox.get()
    subject_val = subject_combobox.get()
    if not class_val or not subject_val:
        messagebox.showwarning("Input Error", "Please select both class and subject")
        return

    questions = fetch_questions(class_val, subject_val)

    if questions:
        for question in questions:
            Label(view_frame, text=question[0], font=('Open Sans', 14), bg='lightyellow').pack(anchor='w', padx=10, pady=5)
    else:
        Label(view_frame, text="No questions found", font=('Open Sans', 14), bg='lightyellow').pack(anchor='w', padx=10, pady=5)

    view_canvas.update_idletasks()
    view_canvas.config(scrollregion=view_canvas.bbox("all"))

def go_back():
    root.destroy()
    import mainpage  # Assuming mainpage.py is in the same directory

root = Tk()
root.geometry("1920x1080")
root.title('View Questions')
#root.attributes('-fullscreen', True)  # Make the window full-screen

# Load background image
bg_image = Image.open("3.png")
bg_image = bg_image.resize((1680, 1050))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background label
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a frame for input fields and button
input_frame = Frame(root, bg='white', bd=5)
input_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.2, anchor='n')

Label(input_frame, text="Class", font=('Open Sans', 14)).place(relx=0.05, rely=0.5, anchor='w')
class_combobox = ttk.Combobox(input_frame, values=["vi", "vii", "viii", "ix", "x"], font=('Open Sans', 14))
class_combobox.place(relx=0.2, rely=0.5, anchor='w')

Label(input_frame, text="Subject", font=('Open Sans', 14)).place(relx=0.45, rely=0.5, anchor='w')
subject_combobox = ttk.Combobox(input_frame, values=["Science", "Social_Science", "Maths", "Computer"], font=('Open Sans', 14))
subject_combobox.place(relx=0.6, rely=0.5, anchor='w')

Button(input_frame, text="View Questions", font=('Open Sans', 14), command=view_questions).place(relx=0.85, rely=0.5, anchor='w')

# Create a back button
back_button = Button(input_frame, text="Back", font=('Open Sans', 14), command=go_back, bg='black', fg='white')
back_button.place(relx=0.46, rely=0.79, anchor='w')

# Create a frame for displaying questions with a scrollbar
view_canvas = Canvas(root, bg='lightyellow')
view_canvas.place(relx=0.5, rely=0.35, relwidth=0.85, relheight=0.6, anchor='n')

view_scrollbar = Scrollbar(root, orient=VERTICAL, command=view_canvas.yview)
view_scrollbar.place(relx=0.925, rely=0.35, relheight=0.6, anchor='n')

view_canvas.configure(yscrollcommand=view_scrollbar.set)

view_frame = Frame(view_canvas, bg='lightyellow')
view_canvas.create_window((0, 0), window=view_frame, anchor='nw')

root.mainloop()
