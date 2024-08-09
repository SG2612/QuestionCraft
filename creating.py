from fpdf import FPDF
from tkinter import *
from tkinter import messagebox,ttk
from PIL import ImageTk

from database_connect import mycursor
from database_connect import con

mycursor.execute("SELECT question FROM final")
myresult = mycursor.fetchall()
pdf=FPDF('P','mm', 'A4')
pdf.add_page()
pdf.set_font('times','BUI', 16)
pdf.set_text_color(220,50,50)
pdf.cell(120,100,'Hello',ln=True)
for row in myresult:
    pdf.set_font('times', '', 12)
    pdf.cell(80,10,row)
pdf.output('pdf1.pdf')
