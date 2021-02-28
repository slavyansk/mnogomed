from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('my_db.db')

def populate_list():
	list_patients_text.delete(0,END)
	for row in db.fetch():
		list_patients_text.insert(END, row)
	
def add_report():
	if studydate_text.get() == '' or name_text.get() == '' or birthday_text.get() == '':
		messagebox.showerror('Пустые поля', 'Заполни поля')
		return
	db.insert(studydate_text.get(), name_text.get(), birthday_text.get(), p_sex_text.get(), examination_text.get(), report_entry.get(1.0,END))
	list_patients_text.delete(0,END)
	list_patients_text.insert(END, (studydate_text.get(), name_text.get(), birthday_text.get(), p_sex_text.get(), examination_text.get(), report_entry.get(1.0, END)))
	clear_text()
	populate_list()
	
def select_item(event):
	try:
		global selected_item
		index = list_patients_text.curselection()[0]
		selected_item = list_patients_text.get(index)
		
		studydate_entry.delete(0, END)
		studydate_entry.insert(END, selected_item[1])
		name_entry.delete(0, END)
		name_entry.insert(END, selected_item[2])
		birthday_entry.delete(0, END)
		birthday_entry.insert(END, selected_item[3])
		p_sex_entry.delete(0, END)
		p_sex_entry.insert(END, selected_item[4])
		examination_entry.delete(0, END)
		examination_entry.insert(END, selected_item[5])
		report_entry.delete(1.0, END)
		report_entry.insert(END, selected_item[6])
	except IndexError:
		pass
	
def remove_report():
	db.remove(selected_item[0])
	clear_text()
	populate_list()

def update_item():
	db.update(selected_item[0], studydate_text.get(), name_text.get(), birthday_text.get(), p_sex_text.get(), examination_text.get(), report_entry.get(1.0, END))
	
	populate_list()
	
def clear_text():
	studydate_entry.delete(0, END)
	name_entry.delete(0, END)
	birthday_entry.delete(0, END)
	p_sex_entry.delete(0, END)
	examination_entry.delete(0, END)
	report_entry.delete(1.0, END)
	
def save_doc():
	print(save_doc)
	
	
app = Tk()


#list_patients
list_patients_text = Listbox(app, height=4, width=80, border=0)
list_patients_text.grid(row=0, column=0, columnspan=5, rowspan=1, pady=20, padx=20)
#Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=0,column=5)
#Set scrollbar to report
list_patients_text.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list_patients_text.yview)

#Bind select
list_patients_text.bind('<<ListboxSelect>>', select_item)

#Studydate
studydate_text = StringVar()
studydate_label = Label(app, text='Дата исследования', font=('normal',12))
studydate_label.grid(row=1, column=0, sticky=W)
studydate_entry = Entry(app, width=35, textvariable=studydate_text)
studydate_entry.grid(row=1, column=1, columnspan=3)

#Name
name_text = StringVar()
name_label = Label(app, text='ФИО', font=('normal',12))
name_label.grid(row=2, column=0, sticky=W)
name_entry = Entry(app, width=35, textvariable=name_text)
name_entry.grid(row=2, column=1, columnspan=3)

#Birthday
birthday_text = StringVar()
birthday_label = Label(app, text='Дата рождения', font=('normal',12))
birthday_label.grid(row=3, column=0, sticky=W)
birthday_entry = Entry(app, width=35, textvariable=birthday_text)
birthday_entry.grid(row=3, column=1, columnspan=3)

#Sex
p_sex_text = StringVar()
p_sex_label = Label(app, text='Пол', font=('normal',12))
p_sex_label.grid(row=4, column=0, sticky=W)
p_sex_entry = Entry(app, width=35, textvariable=p_sex_text)
p_sex_entry.grid(row=4, column=1, columnspan=3)

#examination
examination_text = StringVar()
examination_label = Label(app, text='Исследование', font=('normal',12))
examination_label.grid(row=5, column=0, sticky=W)
examination_entry = Entry(app, width=35, textvariable=examination_text)
examination_entry.grid(row=5, column=1, columnspan=3)

#Report
report_entry = Text(height=10, width=80, border=0, wrap=WORD)
report_entry.grid(row=6, column=0, columnspan=5, rowspan=6, pady=20, padx=20)
#Create scrollbar
scroll = Scrollbar(command=report_entry.yview)
scroll.grid(row=6,column=5, rowspan=6)
#Set scrollbar to report
report_entry.configure(yscrollcommand=scroll.set)

#Buttons
add_btn = Button(app, text='Добавить', width=12, command=add_report)
add_btn.grid(row=12, column=0)

remove_btn = Button(app, text='Удалить', width=12, command=remove_report)
remove_btn.grid(row=12, column=1)

update_btn = Button(app, text='Обновить', width=12, command=update_item)
update_btn.grid(row=12, column=2)

clear_btn = Button(app, text='Очистить поля', width=12, command=clear_text)
clear_btn.grid(row=12, column=3)

save_doc_btn = Button(app, text='Save .doc', width=12, command=save_doc)
save_doc_btn.grid(row=12, column=4)

app.title('Report application')
app.geometry('700x550')

populate_list()

app.mainloop()
