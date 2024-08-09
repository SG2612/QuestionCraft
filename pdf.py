from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import pymysql
from pymysql.err import MySQLError
import tkinter as tk
from tkinter import simpledialog, filedialog

# Function to create PDF
def create_pdf(data, path):
    if not data:
        print("No data to generate PDF.")
        return

    class_info, mcq_questions, saq_questions, long_questions, broad_questions, mcq_answers = data

    # Calculate marks for each question type
    saq_marks = len(saq_questions) * 2
    mcq_marks = len(mcq_questions)
    long_marks = len(long_questions) * 5
    broad_marks = len(broad_questions) * 10

    # Calculate total marks
    total_marks = saq_marks + mcq_marks + long_marks + broad_marks

    # Create a canvas object and set the page size
    c = canvas.Canvas(path, pagesize=letter)

    # Add a border and background color
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(0, 0, 8.5 * inch, 11 * inch, fill=True, stroke=False)

    # Draw a header rectangle
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.rect(0, 10.5 * inch, 8.5 * inch, 0.5 * inch, fill=True, stroke=False)

    # Add the title
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(4.25 * inch, 10.6 * inch, 'XYZ School')

    # Add class information in black
    c.setFillColorRGB(0, 0, 0)  # Set font color to black
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25 * inch, 10.3 * inch, f'Class: {class_info}')

    # Add total marks in black
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(4.25 * inch, 10.0 * inch, f'Full marks: {total_marks}')

    # Draw a line below the header
    c.setStrokeColorRGB(0, 0, 0)
    c.line(0.5 * inch, 9.9 * inch, 8 * inch, 9.9 * inch)

    # Function to add questions
    def add_questions(heading, questions, marks, y_pos, question_type=None):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1 * inch, y_pos, f"Answer the following {heading} ({marks} marks):")
        y_pos -= 0.3 * inch  # Adjust space below the heading

        if questions:
            c.setFont("Helvetica", 12)
            for idx, question in enumerate(questions, 1):
                if y_pos < 1 * inch:
                    c.showPage()
                    y_pos = 10.5 * inch
                    # Skip the header on new pages
                    if question_type != 'mcq':
                        y_pos = 10.0 * inch
                    c.setFont("Helvetica", 12)
                c.drawString(1 * inch, y_pos, f"{idx}. {question[0]}")
                y_pos -= 0.3 * inch

                if question_type == 'mcq':
                    for option_label, option in zip(['A', 'B', 'C', 'D'], question[1:]):
                        c.drawString(1.2 * inch, y_pos, f"{option_label}. {option}")
                        y_pos -= 0.2 * inch
        return y_pos

    # Add the questions
    y_position = 9.5 * inch
    y_position = add_questions('MCQ questions', mcq_questions, mcq_marks, y_position, question_type='mcq')
    y_position -= 0.5 * inch  # Add space before the next section
    y_position = add_questions('SAQ questions', saq_questions, saq_marks, y_position)
    y_position -= 0.5 * inch  # Add space before the next section
    y_position = add_questions('Long questions', long_questions, long_marks, y_position)
    y_position -= 0.5 * inch  # Add space before the next section
    y_position = add_questions('Broad questions', broad_questions, broad_marks, y_position)

    # Add a new page for MCQ answers
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25 * inch, 10.5 * inch, 'MCQ Answers')

    y_position = 10.0 * inch
    c.setFont("Helvetica", 12)
    for idx, answer in enumerate(mcq_answers, 1):
        c.drawString(1 * inch, y_position, f"Q{idx}. {answer}")
        y_position -= 0.3 * inch

    # Save the PDF
    c.save()

# Fetch data from MySQL database
def fetch_data():
    data = []
    my_conn = None

    try:
        # MySQL connection
        my_conn = pymysql.connect(
            host='localhost',
            user='root',
            password='krishnendu@2003',
            database='project'
        )

        with my_conn.cursor() as cursor:
            # Fetch class information
            cursor.execute("SELECT class FROM final LIMIT 1")
            class_info = cursor.fetchone()[0]

            # Fetch questions
            question_types = ['mcq', 'saq', 'long', 'broad']
            questions = {q_type: [] for q_type in question_types}
            for q_type in question_types:
                if q_type == 'mcq':
                    cursor.execute(f"SELECT QUESTION, A, B, C, D FROM final WHERE QUESTION_TYPE='{q_type}'")
                    questions[q_type] = [row for row in cursor.fetchall()]
                else:
                    cursor.execute(f"SELECT QUESTION FROM final WHERE QUESTION_TYPE='{q_type}'")
                    questions[q_type] = [(row[0],) for row in cursor.fetchall()]

            # Fetch MCQ answers
            cursor.execute("SELECT answer FROM final WHERE QUESTION_TYPE='mcq'")
            mcq_answers = [row[0] for row in cursor.fetchall()]

            data = (class_info, questions['mcq'], questions['saq'], questions['long'], questions['broad'], mcq_answers)
            print("Data fetched from database:", data)

    except MySQLError as e:
        print("Error: ", e)

    finally:
        if my_conn:
            my_conn.close()

    return data

# Function to select folder and file name
def select_folder_and_filename():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask for the directory
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return None, None

    # Ask for the file name
    file_name = simpledialog.askstring("Input", "Enter the file name (without extension):")
    if not file_name:
        return None, None

    return folder_selected, file_name

# Main execution
if __name__ == "__main__":
    data = fetch_data()
    if data:
        folder_path, file_name = select_folder_and_filename()
        if folder_path and file_name:
            pdf_path = f"{folder_path}/{file_name}.pdf"
            create_pdf(data, pdf_path)
        else:
            print("No folder or file name selected.")
    else:
        print("No data fetched to create the document.")
