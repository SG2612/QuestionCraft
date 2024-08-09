from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk
import subprocess
from database_connect import mycursor, con

def callpdf():
    subprocess.run(["python", "pdf.py"])

def calldocx():
    subprocess.run(["python", "generate_docx.py"])

def check_generate():
    if (
            subject_input.get() == '' or class_input.get() == '' or mcq_input.get() == '' or saq_input.get() == '' or long_input.get() == '' or broad_input.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        subject = subject_input.get()
        mcq = int(mcq_input.get())
        saq = int(saq_input.get())
        broad = int(broad_input.get())
        long = int(long_input.get())
        classin = class_input.get()

        try:
            query_mcq = f"INSERT INTO final(class, question_type, question, a, b, c, d, answer) SELECT class, question_type, question, a, b, c, d, answer FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {mcq}"
            mycursor.execute(query_mcq, (classin, "MCQ"))

            query_saq = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {saq}"
            mycursor.execute(query_saq, (classin, "SAQ"))

            query_long = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {long}"
            mycursor.execute(query_long, (classin, "LONG"))

            query_broad = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {broad}"
            mycursor.execute(query_broad, (classin, "BROAD"))

            con.commit()
            callpdf()
            messagebox.showinfo("GENERATE", "Question paper generated successfully")

            # Delete data from final table
            mycursor.execute("DELETE FROM final")
            con.commit()

            # Close the current window and redirect to main.py
            root.destroy()
            subprocess.run(["python", "mainpage.py"])

        except Exception as e:
            messagebox.showerror('Error', str(e))
        finally:
            con.close()

def check_generate_docx():
    if (
            subject_input.get() == '' or class_input.get() == '' or mcq_input.get() == '' or saq_input.get() == '' or long_input.get() == '' or broad_input.get() == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        subject = subject_input.get()
        mcq = int(mcq_input.get())
        saq = int(saq_input.get())
        broad = int(broad_input.get())
        long = int(long_input.get())
        classin = class_input.get()

        try:
            query_mcq = f"INSERT INTO final(class, question_type, question, a, b, c, d, answer) SELECT class, question_type, question, a, b, c, d, answer FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {mcq}"
            mycursor.execute(query_mcq, (classin, "MCQ"))

            query_saq = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {saq}"
            mycursor.execute(query_saq, (classin, "SAQ"))

            query_long = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {long}"
            mycursor.execute(query_long, (classin, "LONG"))

            query_broad = f"INSERT INTO final(class, question_type, question) SELECT class, question_type, question FROM {subject} WHERE class=%s AND question_type=%s ORDER BY RAND() LIMIT {broad}"
            mycursor.execute(query_broad, (classin, "BROAD"))

            con.commit()
            calldocx()
            messagebox.showinfo("GENERATE", "Question paper generated successfully")

            # Delete data from final table
            mycursor.execute("DELETE FROM final")
            con.commit()

            # Close the current window and redirect to main.py
            root.destroy()
            subprocess.run(["python", "mainpage.py"])

        except Exception as e:
            messagebox.showerror('Error', str(e))
        finally:
            con.close()

def go_back():
    root.destroy()
    subprocess.run(["python", "mainpage.py"])

# GUI
root = Tk()
root.title("Question Paper Generator")
root.geometry("1680x1050")
#root.attributes('-fullscreen', True)  # Make the window full-screen

# Background Image
bgImage = ImageTk.PhotoImage(file='3.png')
bgLabel = Label(root, image=bgImage)
bgLabel.place(relwidth=1, relheight=1)

# Title Label
title_label = Label(root, text='GENERATE QUESTION PAPER', font=('TIMES NEW ROMAN', 30, 'bold'), bg='#FCFFF9', fg='black')
title_label.pack(pady=20)

# Input Frame
input_frame = Frame(root, bg='#FCFFF9', bd=10)
input_frame.place(relx=0.5, rely=0.4, anchor=CENTER)

# Input Fields
fields = [
    ('SUBJECT:', ['Science', 'Social Science', 'Maths', 'Computer'], 'subject_input'),
    ('CLASS:', ['VI', 'VII', 'VIII', 'IX', 'X'], 'class_input'),
    ('MCQ (1 mark):', None, 'mcq_input'),
    ('SAQ (2 marks):', None, 'saq_input'),
    ('LONG (5 marks):', None, 'long_input'),
    ('BROAD (10 marks):', None, 'broad_input')
]

for idx, (label_text, combo_values, var_name) in enumerate(fields):
    label = Label(input_frame, text=label_text, font=('TIMES NEW ROMAN', 20, 'bold'), bg='#FCFFF9', fg='black')
    label.grid(row=idx, column=0, pady=10, padx=20, sticky=E)
    if combo_values:
        combo = ttk.Combobox(input_frame, values=combo_values, font=('Lucida Fax', 14))
        combo.grid(row=idx, column=1, pady=10, padx=20, sticky=W)
        globals()[var_name] = combo
    else:
        entry = Entry(input_frame, bg='white', font=('Lucida Fax', 14))
        entry.grid(row=idx, column=1, pady=10, padx=20, sticky=W)
        globals()[var_name] = entry

# Button Frame
button_frame = Frame(root, bg='#FCFFF9', bd=10)
button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

# Generate PDF Button
generate_pdf_button = Button(button_frame, text="Save as pdf", font=('Times new roman', 20, 'bold'), bd=1, fg='white', bg='#00A2C6',
                             cursor='hand2', width=12, height=2, activebackground='black', activeforeground='white',
                             command=check_generate)
generate_pdf_button.grid(row=0, column=0, padx=20, pady=10)

# Generate DOCX Button
generate_docx_button = Button(button_frame, text="Save as docx", font=('Times new roman', 20, 'bold'), bd=1, fg='white', bg='#00A2C6',
                              cursor='hand2', width=12, height=2, activebackground='black', activeforeground='white',
                              command=check_generate_docx)
generate_docx_button.grid(row=0, column=1, padx=20, pady=10)

# Back Button
back_button = Button(button_frame, text="BACK", font=('Times new roman', 20, 'bold'), bd=1, fg='white', bg='#FF5733',
                     cursor='hand2', width=10, height=2, activebackground='black', activeforeground='white',
                     command=go_back)
back_button.grid(row=0, column=2, padx=20, pady=10)

root.mainloop()
