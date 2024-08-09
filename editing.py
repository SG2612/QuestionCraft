import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def fetch_questions(class_val, subject_val, question_type_val):
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
        if question_type_val == "MCQ":
            query = f"SELECT question, a, b, c, d FROM {subject_val} WHERE class=%s AND question_type=%s"
        else:
            query = f"SELECT question FROM {subject_val} WHERE class=%s AND question_type=%s"
        cursor.execute(query, (class_val, question_type_val))
        rows = cursor.fetchall()
    except pymysql.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        rows = []
    finally:
        cursor.close()
        conn.close()
    return rows

def view_questions():
    for widget in view_frame_content.winfo_children():
        widget.destroy()

    class_val = class_combobox.get()
    subject_val = subject_combobox.get()
    question_type_val = question_type_combobox.get()

    if not class_val or not subject_val or not question_type_val:
        messagebox.showwarning("Input Error", "Please select class, subject, and question type")
        return

    questions = fetch_questions(class_val, subject_val, question_type_val)

    if questions:
        for question in questions:
            question_frame = Frame(view_frame_content, bg='lightyellow')
            question_frame.pack(fill='x', padx=10, pady=5)

            question_text_frame = Frame(question_frame, bg='lightyellow')
            question_text_frame.pack(side=TOP, fill='x')

            question_label = Label(question_text_frame, text=question[0], font=('Open Sans', 14), bg='lightyellow')
            question_label.pack(side=LEFT, anchor='w')

            delete_button = Button(question_text_frame, text="Delete", font=('Open Sans', 12), command=lambda q=question[0]: delete_question(class_val, subject_val, question_type_val, q))
            delete_button.pack(side=RIGHT, padx=10)

            if question_type_val == "MCQ":
                options_frame = Frame(question_frame, bg='lightyellow')
                options_frame.pack(side=TOP, anchor='w')

                option_a_label = Label(options_frame, text=f"a. {question[1]}", font=('Open Sans', 12), bg='lightyellow')
                option_a_label.pack(side=LEFT, padx=10)
                option_b_label = Label(options_frame, text=f"b. {question[2]}", font=('Open Sans', 12), bg='lightyellow')
                option_b_label.pack(side=LEFT, padx=10)
                option_c_label = Label(options_frame, text=f"c. {question[3]}", font=('Open Sans', 12), bg='lightyellow')
                option_c_label.pack(side=LEFT, padx=10)
                option_d_label = Label(options_frame, text=f"d. {question[4]}", font=('Open Sans', 12), bg='lightyellow')
                option_d_label.pack(side=LEFT, padx=10)
    else:
        Label(view_frame_content, text="No questions found", font=('Open Sans', 14), bg='lightyellow').pack(anchor='w', padx=10, pady=5)

    view_canvas.update_idletasks()
    view_canvas.config(scrollregion=view_canvas.bbox("all"))

def delete_question(class_val, subject_val, question_type_val, question_text):
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
        query = f"DELETE FROM {subject_val} WHERE class=%s AND question=%s AND question_type=%s"
        cursor.execute(query, (class_val, question_text, question_type_val))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Question deleted successfully")
            view_questions()  # Refresh the question list
        else:
            messagebox.showwarning("Not Found", "No matching question found")
    except pymysql.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def go_back():
    root.destroy()
    subprocess.run(["python", "mainpage.py"])  # Ensure mainpage.py is in the same directory

root = Tk()
root.title('Edit Questions')
root.geometry('1920x1080')
root.attributes('-fullscreen', True)  # Make the window full-screen

# Load background image
bg_image = Image.open("3.png")
bg_image = bg_image.resize((1680, 1050))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background label
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Add heading
heading_label = Label(root, text="View and Edit Questions", font=('Open Sans', 24, 'bold'), bg='lightblue')
heading_label.place(relx=0.5, rely=0.05, anchor='n')

# Create a frame for input fields and button
input_frame = Frame(root, bg='white', bd=5)
input_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.2, anchor='n')

Label(input_frame, text="Class", font=('Open Sans', 14)).place(relx=0.05, rely=0.5, anchor='w')
class_combobox = ttk.Combobox(input_frame, values=["VI", "VII", "VIII", "IX", "X"], font=('Open Sans', 14))
class_combobox.place(relx=0.2, rely=0.5, anchor='w')

Label(input_frame, text="Subject", font=('Open Sans', 14)).place(relx=0.5, rely=0.5, anchor='w')
subject_combobox = ttk.Combobox(input_frame, values=["Science", "Social_Science", "Maths", "Computer", "English"], font=('Open Sans', 14))
subject_combobox.place(relx=0.6, rely=0.5, anchor='w')

Label(input_frame, text="Question Type", font=('Open Sans', 14)).place(relx=0.05, rely=0.8, anchor='w')
question_type_combobox = ttk.Combobox(input_frame, values=["MCQ", "SAQ", "Long", "Broad"], font=('Open Sans', 14))
question_type_combobox.place(relx=0.2, rely=0.8, anchor='w')

Button(input_frame, text="View Questions", font=('Open Sans', 14), command=view_questions).place(relx=0.85, rely=0.5, anchor='w')

# Create a frame for displaying questions with scrollbar
view_frame = Frame(root, bg='lightyellow')
view_frame.place(relx=0.5, rely=0.35, relwidth=0.75, relheight=0.6, anchor='n')

view_canvas = Canvas(view_frame, bg='lightyellow')
view_canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(view_frame, orient=VERTICAL, command=view_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

view_canvas.configure(yscrollcommand=scrollbar.set)
view_canvas.bind('<Configure>', lambda e: view_canvas.config(scrollregion=view_canvas.bbox("all")))

view_frame_content = Frame(view_canvas, bg='lightyellow')
view_canvas.create_window((0, 0), window=view_frame_content, anchor='nw')

# Create a back button
back_button = Button(root, text="Back", font=('Open Sans', 14), command=go_back, bg='red', fg='white')
back_button.place(relx=0.78, rely=0.3, anchor='s')

root.mainloop()
