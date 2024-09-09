import sqlite3
from tkinter import Tk, Frame, Label, Entry, Button, Listbox, StringVar, IntVar, RIDGE, W, END
from tkinter import messagebox

# Create a database connection
def connect_db():
    con = sqlite3.connect("hospital.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS patients 
                   (id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    age INTEGER, 
                    gender TEXT, 
                    disease TEXT)''')
    con.commit()
    con.close()

# Add a new patient
def add_patient():
    con = sqlite3.connect("hospital.db")
    cur = con.cursor()
    cur.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)", 
                (name_var.get(), age_var.get(), gender_var.get(), disease_var.get()))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Patient added successfully")
    view_patients()

# View all patients
def view_patients():
    con = sqlite3.connect("hospital.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    patient_list.delete(0, END)
    for row in rows:
        patient_list.insert(END, row)
    con.close()

# Select a patient
def select_patient(event):
    global selected_patient
    index = patient_list.curselection()[0]
    selected_patient = patient_list.get(index)

    name_var.set(selected_patient[1])
    age_var.set(selected_patient[2])
    gender_var.set(selected_patient[3])
    disease_var.set(selected_patient[4])

# Update patient data
def update_patient():
    con = sqlite3.connect("hospital.db")
    cur = con.cursor()
    cur.execute("UPDATE patients SET name=?, age=?, gender=?, disease=? WHERE id=?", 
                (name_var.get(), age_var.get(), gender_var.get(), disease_var.get(), selected_patient[0]))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Patient updated successfully")
    view_patients()

# Delete patient data
def delete_patient():
    con = sqlite3.connect("hospital.db")
    cur = con.cursor()
    cur.execute("DELETE FROM patients WHERE id=?", (selected_patient[0],))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "Patient deleted successfully")
    view_patients()

# Main GUI setup
root = Tk()
root.title("Hospital Management System")
root.geometry("620x500")
root.config(bg="#2c2f33")  # Dark background

# Style settings
label_font = ("Arial", 12)
btn_font = ("Arial", 10, "bold")
input_font = ("Arial", 10)
frame_bg = "#23272a"  # Dark frame background
btn_bg = "#7289da"    # Soft blue button color
btn_fg = "#ffffff"    # White button text
text_fg = "#ffffff"   # White text color

# Patient Information Frame
info_frame = Frame(root, bg=frame_bg, bd=3, relief=RIDGE, padx=10, pady=10)
info_frame.place(x=20, y=20, width=580, height=180)

# Labels and Entry fields
Label(info_frame, text="Patient Name:", bg=frame_bg, fg=text_fg, font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky=W)
name_var = StringVar()
Entry(info_frame, textvariable=name_var, font=input_font).grid(row=0, column=1, padx=10, pady=10)

Label(info_frame, text="Age:", bg=frame_bg, fg=text_fg, font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky=W)
age_var = IntVar()
Entry(info_frame, textvariable=age_var, font=input_font).grid(row=1, column=1, padx=10, pady=10)

Label(info_frame, text="Gender:", bg=frame_bg, fg=text_fg, font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky=W)
gender_var = StringVar()
Entry(info_frame, textvariable=gender_var, font=input_font).grid(row=2, column=1, padx=10, pady=10)

Label(info_frame, text="Disease:", bg=frame_bg, fg=text_fg, font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky=W)
disease_var = StringVar()
Entry(info_frame, textvariable=disease_var, font=input_font).grid(row=3, column=1, padx=10, pady=10)

# Listbox to show records
patient_list = Listbox(root, height=8, width=50, font=input_font, bd=3, relief=RIDGE, bg="#2c2f33", fg=text_fg)
patient_list.place(x=20, y=220)
patient_list.bind('<<ListboxSelect>>', select_patient)

# Buttons Frame
btn_frame = Frame(root, bg=frame_bg, padx=10, pady=20)
btn_frame.place(x=20, y=400, width=580, height=80)

# Buttons
add_btn = Button(btn_frame, text="Add Patient", command=add_patient, font=btn_font, bg=btn_bg, fg="#2c2f33")
add_btn.grid(row=0, column=0, padx=5, pady=10)

update_btn = Button(btn_frame, text="Update Patient", command=update_patient, font=btn_font, bg="#FFB600", fg="#2c2f33")
update_btn.grid(row=0, column=1, padx=5, pady=10)

delete_btn = Button(btn_frame, text="Delete Patient", command=delete_patient, font=btn_font, bg="#FF4C4C", fg="#2c2f33")
delete_btn.grid(row=0, column=2, padx=5, pady=10)

view_btn = Button(btn_frame, text="View All Patients", command=view_patients, font=btn_font, bg="#4CAF50", fg="#2c2f33")
view_btn.grid(row=0, column=3, padx=5, pady=10)

close_btn = Button(btn_frame, text="Close", command=root.quit, font=btn_font, bg="#7289da", fg="#2c2f33")
close_btn.grid(row=0, column=4, padx=5, pady=10)






# Connect to the database and run the app
connect_db()
view_patients()
root.mainloop()
