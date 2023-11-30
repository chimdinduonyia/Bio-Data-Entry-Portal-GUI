from tkinter import *
import sqlite3

root = Tk()
root.title("Bio-Data Portal")
root.iconbitmap("C:/Users/USER/Documents/PYTHON PROJECTS/Icons/coffee_icon.ico") 


#----------------------------------------Create Database and Data Table
conn = sqlite3.connect("medicaldb.db")

#Initialize Cursor
c = conn.cursor()

#Delete any existing similar patient_bio data tables to save meory as this is just a demo project
c.execute("DROP TABLE IF EXISTS patient_bio")

#Create Patient Bio Data Table
c.execute(""" CREATE TABLE patient_bio(
            last_name text,
            first_name text,
            age integer,
            genotype text,
            height integer,
            weight integer,
            gender text,
            blood_group text
            )
            """)

conn.commit()

conn.close()

#--------------------------------------------------------Create Frames for Basic Data Form

#Create Frame for Personal Basic Data
data_frame = LabelFrame(root, text = "Personal Information")
data_frame.grid(row = 0, column = 0, rowspan = 2, padx = 15, pady = (0, 15))

#Create Frame for Gender Data
gender_frame = LabelFrame(root, text = "Gender")
gender_frame.grid(row = 0, column = 1, padx = 15, pady = 15)

#Create Frame for Blood Group Data
bg_frame = LabelFrame(root, text = "Blood Group")
bg_frame.grid(row = 1, column = 1, padx = 15, pady = 15)

#----------------------------------------------Create Data Entry Textboxes and Labels
last_name = Entry(data_frame, width = 30)
last_name.grid(row = 0, column = 1, pady = 10, padx = 10)
ln_label = Label(data_frame, text = "Last Name: ")
ln_label.grid(row = 0, column = 0, padx = 10)

first_name = Entry(data_frame, width = 30)
first_name.grid(row = 1, column = 1, pady = 10, padx = 10)
fn_label = Label(data_frame, text = "First Name: ")
fn_label.grid(row = 1, column = 0)

age = Entry(data_frame, width = 30)
age.grid(row = 2, column = 1, pady = 10, padx = 10)
a_label = Label(data_frame, text = "Age: ")
a_label.grid(row = 2, column = 0)

genotype = Entry(data_frame, width = 30)
genotype.grid(row = 3, column = 1, pady = 10, padx = 10)
g_label = Label(data_frame, text = "Genotype: ")
g_label.grid(row = 3, column = 0)

height = Entry(data_frame, width = 30)
height.grid(row = 4, column = 1, pady = 10, padx = 10)
h_label = Label(data_frame, text = "Height: ")
h_label.grid(row = 4, column = 0)

weight = Entry(data_frame, width = 30)
weight.grid(row = 5, column = 1, pady = 10, padx = 10)
w_label = Label(data_frame, text = "Weight: ")
w_label.grid(row = 5, column = 0)

#Create Query Label where Query Results will be displayed
query_label = Label(root, text = "Queried Records are displayed here...", relief = SUNKEN)
query_label.grid(row = 3, column = 0, columnspan = 2, sticky = W+E, pady = 10)

#Create Delete Frame Where Data Records can be deleted by ID
del_frame = LabelFrame(root, text = "Delete Record")
del_frame.grid(row = 4, column = 0, columnspan = 2, pady = (0, 10))

#Create Text Area for Selecting Records by ID
sel_label = Label(del_frame, text = "Select ID: E.g 1 or 2 or 3...")
sel_label.grid(row = 0, column = 0, padx = 15)
sel_entry = Entry(del_frame, width = 40)
sel_entry.grid(row = 0, column = 1, padx = 15)

#Create Radio Buttons for Gender Selection
genders = [
            ("Non-binary", "Non-binary"),
            ("Male", "Male"),
            ("Female", "Female")
            ]

sex = StringVar()
sex.set("Non-binary")

for a, b in genders:
    Radiobutton(gender_frame, text = a, variable = sex, value = b).pack(anchor = W)

#Create Radio Buttons for Blood Group Section
blood_groups = [
                ("A+", "A+"),
                ("A-", "A-"),
                ("B+", "B+"),
                ("B-", "B-"),
                ("AB+", "AB+"),
                ("AB-", "AB-"),
                ("O+", "O+"),
                ("O-", "O-"),
                ]

bg = StringVar()
bg.set("A+")

for a, b in blood_groups:
    Radiobutton(bg_frame, text = a, variable = bg, value = b).pack(anchor = W)

#Define Save Function
def save():

    record_id = sel_entry.get()
    
    conn = sqlite3.connect("medicaldb.db")

    c = conn.cursor()

    c.execute("""UPDATE patient_bio SET
        last_name = :last,
        first_name = :first,
        age = :age,
        genotype = :genotype,
        height = :height,
        weight = :weight,
        gender = :gender,
        blood_group = :blgp

        WHERE oid = :oid""",
        {'first':first_name_editor.get(),
        'last': last_name_editor.get(),
        'age': age_editor.get(),
        'genotype': genotype_editor.get(),
        'height': height_editor.get(),
        'weight': weight_editor.get(),
        'gender': sex_editor.get(),
        'blgp': bg_editor.get(),

        'oid': record_id
        })

    conn.commit()

    conn.close()

    editor.destroy()

#Define Update Function
def update():
    global sel_entry
    global sex_editor
    global bg_editor
    global first_name_editor
    global last_name_editor
    global age_editor
    global genotype_editor
    global height_editor
    global weight_editor
    global editor

    editor = Toplevel()
    editor.title("Update A Record")
    root.iconbitmap("C:/Users/USER/Documents/PYTHON PROJECTS/Icons/coffee_icon.ico") 

    #record_id = sel_entry.get()


    #Query Database for Record 
    conn = sqlite3.connect("medicaldb.db")

    c = conn.cursor()

    c.execute("SELECT * FROM patient_bio WHERE oid = " + sel_entry.get())

    records = c.fetchall()

    conn.commit()

    conn.close()

    #---------------------------------Reproduce the original form in the new window to allow updating of record

    #Create Frame for Basic Data
    data_frame_editor = LabelFrame(editor, text = "Personal Details")
    data_frame_editor.grid(row = 0, column = 0, rowspan = 2, padx = 15, pady = (0, 15))

    #Create Frame for Gender Data
    gender_frame_editor = LabelFrame(editor, text = "Gender")
    gender_frame_editor.grid(row = 0, column = 1, padx = 15, pady = 15)

    #Create Frame for Blood Group Data
    bg_frame_editor = LabelFrame(editor, text = "Blood Group")
    bg_frame_editor.grid(row = 1, column = 1, padx = 15, pady = 15)

    #Create Data Entry Textboxes and Labels
    last_name_editor = Entry(data_frame_editor, width = 30)
    last_name_editor.grid(row = 0, column = 1, pady = 10, padx = 10)
    ln_label_editor = Label(data_frame_editor, text = "Last Name: ")
    ln_label_editor.grid(row = 0, column = 0, padx = 10)

    first_name_editor = Entry(data_frame_editor, width = 30)
    first_name_editor.grid(row = 1, column = 1, pady = 10, padx = 10)
    fn_label_editor = Label(data_frame_editor, text = "First Name: ")
    fn_label_editor.grid(row = 1, column = 0)

    age_editor = Entry(data_frame_editor, width = 30)
    age_editor.grid(row = 2, column = 1, pady = 10, padx = 10)
    a_label_editor = Label(data_frame_editor, text = "Age: ")
    a_label_editor.grid(row = 2, column = 0)

    genotype_editor = Entry(data_frame_editor, width = 30)
    genotype_editor.grid(row = 3, column = 1, pady = 10, padx = 10)
    g_label_editor = Label(data_frame_editor, text = "Genotype: ")
    g_label_editor.grid(row = 3, column = 0)

    height_editor = Entry(data_frame_editor, width = 30)
    height_editor.grid(row = 4, column = 1, pady = 10, padx = 10)
    h_label_editor = Label(data_frame_editor, text = "Height: ")
    h_label_editor.grid(row = 4, column = 0)

    weight_editor = Entry(data_frame_editor, width = 30)
    weight_editor.grid(row = 5, column = 1, pady = 10, padx = 10)
    w_label_editor = Label(data_frame_editor, text = "Weight: ")
    w_label_editor.grid(row = 5, column = 0)

    #Create Radio Buttons for Gender Selection
    genders = [
                ("Non-binary", "Non-binary"),
                ("Male", "Male"),
                ("Female", "Female")
                ]

    sex_editor = StringVar()

    for a, b in genders:
        Radiobutton(gender_frame_editor, text = a, variable = sex_editor, value = b).pack(anchor = W)

    #Create Radio Buttons for Blood Group Section
    blood_groups = [
                    ("A+", "A+"),
                    ("A-", "A-"),
                    ("B+", "B+"),
                    ("B-", "B-"),
                    ("AB+", "AB+"),
                    ("AB-", "AB-"),
                    ("O+", "O+"),
                    ("O-", "O-"),
                    ]

    bg_editor = StringVar()

    for a, b in blood_groups:
        Radiobutton(bg_frame_editor, text = a, variable = bg_editor, value = b).pack(anchor = W)

    for record in records:
        last_name_editor.insert(0, record[0])
        first_name_editor.insert(0, record[1])
        age_editor.insert(0, record[2])
        genotype_editor.insert(0, record[3])
        height_editor.insert(0, record[4])
        weight_editor.insert(0, record[5])
        sex_editor.set(str(record[6]))
        bg_editor.set(str(record[7]))


    #Create a Save Button
    save_btn = Button(editor, text = "Save", command = save , bg = "#00FF00")
    save_btn.grid(row = 3, column = 0, columnspan = 2, sticky = W+E, padx = 20, pady = 10)


#Define Submit Function
def submit():

    conn = sqlite3.connect("medicaldb.db")

    c = conn.cursor()

    c.execute("INSERT INTO patient_bio VALUES (:last_name, :first_name, :age, :genotype, :height, :weight, :gender, :blood_group)", 
                
                #Create dictionary to assign values
                {
                    "last_name": last_name.get(),
                    "first_name": first_name.get(),
                    "age": age.get(),
                    "genotype": genotype.get(),
                    "height": height.get(),
                    "weight": weight.get(),
                    "gender": sex.get(),
                    "blood_group": bg.get()
                })

    conn.commit()

    conn.close()

    #Clear entry boxes after fields have been entered
    last_name.delete(0, END)
    first_name.delete(0, END)
    age.delete(0, END)
    genotype.delete(0, END)
    height.delete(0, END)
    weight.delete(0, END)
    sex.set("Non-binary")
    bg.set("A+")

#Define Query Function
def query():

    global query_label

    conn = sqlite3.connect("medicaldb.db")

    c = conn.cursor()

    c.execute("SELECT *, oid FROM patient_bio")

    records = c.fetchall()

    query_return = "Patient Records:\n"

    for lastname, firstname, age, geno, height, weight, gender, bloodgroup, record_id in records:
        
        query_return += str(record_id) + " --> " + str(lastname) + " " + str(firstname)  + " - " + "Age: " + str(age) + ", Geno: " + str(geno) + ", Height: " + str(height) + ", Weight: " + str(weight) + ", Gender: " + str(gender) + ", Blood Group: " + str(bloodgroup) + "\n"

    conn.commit()

    conn.close()

    #Update Query Label
    query_label.grid_forget()
    query_label = Label(root, text = query_return, relief = SUNKEN)
    query_label.grid(row = 3, column = 0, columnspan = 2, sticky = W+E, pady = 10)

#Define Delete Function
def delete_record():
    global query
    global sel_entry
    conn = sqlite3.connect("medicaldb.db")

    #Delete a Record
    c = conn.cursor()
    c.execute("DELETE FROM patient_bio WHERE oid = " + sel_entry.get())

    conn.commit()

    conn.close()

    sel_entry.delete(0, END)

    query()


#Create Submit and Query Buttons
submit = Button(data_frame, text = "Submit", command = submit, bg = "#00FF00")
submit.grid(row = 6, column = 0, columnspan = 2, sticky = W+E, padx = 20, pady = 10)

query_btn = Button(root, text = "Query", command = query, bg = "#0000FF")
query_btn.grid(row = 2, column = 0, columnspan = 2, sticky = W+E, padx = 30, pady = 10)

#Create Delete Button
delete_btn = Button(del_frame, text = "Delete", command = delete_record, bg = "#FF0000")
delete_btn.grid(row = 1, column = 0, columnspan = 2, sticky = W+E, padx = 20, pady = 10)

#Create an Update Button
select_btn = Button(del_frame, text = "Update", command = update , bg = "#FFFF00")
select_btn.grid(row = 2, column = 0, columnspan = 2, sticky = W+E, padx = 20, pady = 10)



root.mainloop()