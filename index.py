import tkinter as tk
from tkinter import PhotoImage
import subprocess
from tkinter import ttk
import pymysql

def check_login_records():
    try:
        con = pymysql.connect(
            host='localhost',
            user='root',
            password='krishnendu@2003',
            database='project'
        )
        cursor = con.cursor()
        cursor.execute('SELECT COUNT(*) FROM login')
        result = cursor.fetchone()
        con.close()
        return result[0] > 0
    except pymysql.Error as e:
        print(f"Database Error: {e}")
        return False

def redirect_to_script():
    if check_login_records():
        script = 'login.py'
    else:
        script = 'signup.py'
    try:
        subprocess.run(['python', script])
    except Exception as e:
        print(f"Error running script {script}: {e}")
    finally:
        root.destroy()

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Automated Question Paper Generator")
root.attributes('-fullscreen', True)
root.configure(bg='#2c2c2c')

img = PhotoImage(file='C:/Users/msi/Desktop/New folder (3)/questionpapergenerator/abc.png')
img_label = tk.Label(root, image=img, bg='#292929')
img_label.pack(pady=(50, 20))

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton",
                font=("Arial", 16),
                padding=10,
                background="#4CAF50",
                foreground="white",
                borderwidth=1,
                relief="flat")
style.map("TButton",
          background=[("active", "#45a049"), ("!active", "#4CAF50")],
          foreground=[("active", "white"), ("!active", "white")],
          relief=[("active", "groove"), ("!active", "flat")])

start_button = ttk.Button(root, text="Start", command=redirect_to_script, style="TButton")
start_button.pack(pady=20)

exit_button = ttk.Button(root, text="Exit", command=exit_app, style="TButton")
exit_button.pack(pady=20)

root.mainloop()
