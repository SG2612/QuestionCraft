from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk
from database_connect import mycursor, con

def closing():
    con.close()
    root.destroy()
    import mainpage

def login_page():
    root.destroy()
    import login

def delete():
    question_input.delete(1.0, END)
    a_input.delete(1.0, END)
    b_input.delete(1.0, END)
    c_input.delete(1.0, END)
    d_input.delete(1.0, END)
    answer_input.delete(1.0, END)

def check():
    if qtype_input.get() == "MCQ":
        if (subject_input.get() =='' or class_input.get()=='' or qtype_input.get()=='' or question_input.get(1.0, END).strip() =='' or a_input.get(1.0, END).strip() =='' or b_input.get(1.0, END).strip() =='' or c_input.get(1.0, END).strip() =='' or d_input.get(1.0, END).strip() =='' or answer_input.get(1.0, END).strip() ==''):
            messagebox.showerror('Error', 'All fields required')
            login_page()
    if subject_input.get() =='' or class_input.get()=='' or qtype_input.get()=='' or question_input.get(1.0, END).strip() =='':
        messagebox.showerror("Error", "All fields are required")
        login_page()
    else:
        table=subject_input.get()
        query=f'INSERT INTO {table} (CLASS, QUESTION_TYPE, QUESTION, A, B, C, D, ANSWER) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(query,(class_input.get(), qtype_input.get(), question_input.get(1.0, END).strip(), a_input.get(1.0, END).strip(), b_input.get(1.0, END).strip(), c_input.get(1.0, END).strip(), d_input.get(1.0, END).strip(), answer_input.get(1.0, END).strip()))
        messagebox.showinfo('SUCCESS','Question Successfully Added')
        delete()
    con.commit()

# GUI
root = Tk()
root.title("Add Question")
root.attributes('-fullscreen', True)  # Make the window fullscreen

# Background Image
bgImage = ImageTk.PhotoImage(file='3.png')
bgLabel = Label(root, image=bgImage)
bgLabel.place(relwidth=1, relheight=1)

frame = Frame(root, bg='#FCFFF9', bd=10)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

heading = Label(frame, text="Add Question", font=('Bookman Old Style', 25, 'bold'), bg='#FCFFF9', fg='black')
heading.grid(row=0, columnspan=2, pady=10)

# SUBJECT
subject_label = Label(frame, text='SUBJECT:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
subject_label.grid(row=1, column=0, pady=10, padx=20, sticky=E)
subject_input = ttk.Combobox(frame, values=["Science", "Social_Science", "Maths", "Computer"], font=('Lucida Fax', 12))
subject_input.grid(row=1, column=1, pady=10, padx=20, sticky=W)

# CLASS
class_label = Label(frame, text='CLASS:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
class_label.grid(row=2, column=0, pady=10, padx=20, sticky=E)
class_input = ttk.Combobox(frame, values=["VI", "VII", "VIII", "IX", "X"], font=('Lucida Fax', 12))
class_input.grid(row=2, column=1, pady=10, padx=20, sticky=W)

# QUESTION TYPE
qtype_label = Label(frame, text='QUESTION TYPE:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
qtype_label.grid(row=3, column=0, pady=10, padx=20, sticky=E)
qtype_input = ttk.Combobox(frame, values=["MCQ", "SAQ", "LONG", "BROAD"], font=('Lucida Fax', 12))
qtype_input.grid(row=3, column=1, pady=10, padx=20, sticky=W)

# QUESTION
question_label = Label(frame, text='QUESTION:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
question_label.grid(row=4, column=0, pady=10, padx=20, sticky=E)
question_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=4, width=40)
question_input.grid(row=4, column=1, pady=10, padx=20, sticky=W)

# OPTIONS
label = Label(frame, text='OPTIONS:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
label.grid(row=5, column=0, pady=10, padx=20, sticky=E)
a_label = Label(frame, text='Option A:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
a_label.grid(row=6, column=0, pady=10, padx=20, sticky=E)
a_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=2, width=40)
a_input.grid(row=6, column=1, pady=10, padx=20, sticky=W)

b_label = Label(frame, text='Option B:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
b_label.grid(row=7, column=0, pady=10, padx=20, sticky=E)
b_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=2, width=40)
b_input.grid(row=7, column=1, pady=10, padx=20, sticky=W)

c_label = Label(frame, text='Option C:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
c_label.grid(row=8, column=0, pady=10, padx=20, sticky=E)
c_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=2, width=40)
c_input.grid(row=8, column=1, pady=10, padx=20, sticky=W)

d_label = Label(frame, text='Option D:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
d_label.grid(row=9, column=0, pady=10, padx=20, sticky=E)
d_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=2, width=40)
d_input.grid(row=9, column=1, pady=10, padx=20, sticky=W)

# ANSWER
answer_label = Label(frame, text='ANSWER:', font=('Times New Roman', 14), bg='#FCFFF9', fg='black')
answer_label.grid(row=10, column=0, pady=10, padx=20, sticky=E)
answer_input = Text(frame, bg='white', font=('Lucida Fax', 12), height=2, width=40)
answer_input.grid(row=10, column=1, pady=10, padx=20, sticky=W)

# BUTTONS
button = Button(frame, text='ADD THE QUESTION', command=check, font=('Times New Roman', 14, 'bold'), bg='#4CAF50', fg='white', width=20)
button.grid(row=11, column=0, pady=20, padx=20, columnspan=2)

button2 = Button(frame, text='Back', command=closing, font=('Times New Roman', 14, 'bold'), bg='#f44336', fg='white', width=20)
button2.grid(row=12, column=0, pady=10, padx=20, columnspan=2)

root.mainloop()
