import customtkinter as ct
import sqlite3
from CTkMenuBar import *
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable
import webbrowser as wb
import mysql.connector
import pandas as pd

conn = sqlite3.connect("exam.db")
curs = conn.cursor()

connDB = mysql.connector.connect(host="sql.freedb.tech", username="freedb_isouopadmin", password="*a@SHRB@m6#7mK4")
cursDB = connDB.cursor()

cursDB.execute("USE freedb_isouop")
cursDB.execute("SELECT schoolName FROM schools")

schoolsfromsql = cursDB.fetchall()
schools = []

for school in schoolsfromsql:
    schools.append(school[0])

cursDB.execute("SELECT organName from organs")
organsfromsql = cursDB.fetchall()
organs = []

for organ in organsfromsql:
    organs.append(organ[0])

connDB.close()
exists = False

curs.execute("""
        CREATE TABLE IF NOT EXISTS students(
                studentName TEXT
             )
""")
conn.commit()

curs.execute("""
        CREATE TABLE IF NOT EXISTS examTypes(
                typeName TEXT
             )
""")
conn.commit()

curs.execute("""
        CREATE TABLE IF NOT EXISTS journal(
                studentName TEXT,
                mark INTEGER,
                type TEXT
             )
""")
conn.commit()

curs.execute("""
        CREATE TABLE IF NOT EXISTS ktp(
                type TEXT,
                topic TEXT
             )
""")
conn.commit()

curs.execute("SELECT * FROM students ORDER BY studentName ASC")
studentsSql = curs.fetchall()
students = []
for student in studentsSql:
    students.append(student[0])

curs.execute("SELECT * FROM examTypes ORDER BY typeName ASC")
typesSql = curs.fetchall()

types = []
for type_ in typesSql:
    types.append(type_[0])

root = ct.CTk()
root.title(f"ИС «УВО»")

support = lambda : wb.open("https://vk.com/iso_uop")
close = lambda : root.destroy()

def studentsManager():
    sm = ct.CTk()
    sm.title("Управление учениками")

    def addStudent():
        global students
        try:
            curs.execute("INSERT INTO students(studentName) VALUES (?)", (studentName.get(),))
            conn.commit()
        except Exception as e:
            studentError = CTkMessagebox(sm, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
            if studentError.get() == "Сообщить разработчику":
                support()
        else:
            students.append(studentName.get())
    
    def delStudent():
        global students
        try:
            curs.execute("DELETE FROM students WHERE studentName = ?", (studentName.get(),))
            conn.commit()
        except Exception as e:
            studentError = CTkMessagebox(sm, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
            if studentError.get() == "Сообщить разработчику":
                support()
        else:
            students.remove(studentName.get())
        
    def students():
        stm = ct.CTk()
        stm.title("Ученики")

        curs.execute("SELECT * FROM students ORDER BY studentName ASC")

        studentsTable = CTkTable(stm, values=curs.fetchall(), column=1, hover_color="black")
        studentsTable.pack()

        stm.mainloop()

    studentName = ct.CTkEntry(sm, placeholder_text="Имя ученика")
    studentName.pack()

    smMenu = CTkMenuBar(sm)
    smMenu.add_cascade(text="Добавить", postcommand=addStudent)
    smMenu.add_cascade(text="Удалить", postcommand=delStudent)
    smMenu.add_cascade(text="Ученики", postcommand=students)

    sm.mainloop()

def typesManager():
    if exists:
        tm = ct.CTk()
        tm.title("Управление типами")

        def types():
            ttm = ct.CTk()
            ttm.title("Ученики")

            curs.execute("SELECT * FROM examTypes ORDER BY typeName ASC")

            studentsTable = CTkTable(ttm, values=curs.fetchall(), column=1, hover_color="black")
            studentsTable.pack()

            ttm.mainloop()

        def addType():
            global types
            try:
                curs.execute("INSERT INTO examTypes(typeName) VALUES (?)", (typeName.get(),))
                conn.commit()
            except Exception as e:
                studentError = CTkMessagebox(tm, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
                if studentError.get() == "Сообщить разработчику":
                    support()
            else:
                types.append(typeName.get())

        def delType():
            global types
            try:
                curs.execute("DELETE FROM examTypes WHERE typeName = ?", (typeName.get(),))
                conn.commit()
            except Exception as e:
                studentError = CTkMessagebox(tm, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
                if studentError.get() == "Сообщить разработчику":
                    support()
            else:
                types.remove(typeName.get())

        typeName = ct.CTkEntry(tm, placeholder_text="Введите тип")
        typeName.pack()

        tmMenu = CTkMenuBar(tm)
        tmMenu.add_cascade("Добавить", postcommand=addType)
        tmMenu.add_cascade("Удалить", postcommand=delType)
        tmMenu.add_cascade("Просмотреть", postcommand=types)

        tm.mainloop()
    else:
        orgnotex = CTkMessagebox(root, title="Ошибка", message="Организации несуществует! Запросите программу у органа или у нас напрямую", option_1="Запросить")
        if orgnotex.get() == "Запросить":
            wb.open("https://isouop.site/organs")

def journalManager():
    jrnalmng = ct.CTk()
    jrnalmng.title("Журнал")
    jrnalmng.geometry("420x84")

    def addMark():
        try:
            curs.execute("INSERT INTO journal(studentName, mark, type) VALUES (?, ?, ?)", (studentCb.get(), int(markEntry.get()), typeCb.get()))
            conn.commit()
        except Exception as e:
            studentError = CTkMessagebox(jrnalmng, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
            if studentError.get() == "Сообщить разработчику":
                support()
        else:
            CTkMessagebox(jrnalmng, title="Добавлено", message="Добавлено", icon="check")

    def delMark():
        try:
            curs.execute("DELETE FROM journal WHERE studentName = ? AND mark = ? AND type = ?", (studentCb.get(), int(markEntry.get()), typeCb.get()))
            conn.commit()
        except Exception as e:
            studentError = CTkMessagebox(jrnalmng, title="Ошибка", message=f"Произошла ошибка! Сообщите о ней разработчику\n{e}", option_1="Сообщить разработчику", option_2="Отмена", cancel_button="None", icon="cancel")
            if studentError.get() == "Сообщить разработчику":
                support()
        else:
            CTkMessagebox(jrnalmng, title="Удалено", message="Удалено", icon="check")

    studentCb = ct.CTkComboBox(jrnalmng, values=students)
    studentCb.place(x=0, y=0)
    studentCb.set("Ученик")

    typeCb = ct.CTkComboBox(jrnalmng, values=types)
    typeCb.place(x=140, y=0)
    typeCb.set("Тип работы")

    markEntry = ct.CTkEntry(jrnalmng, placeholder_text="Оценка")
    markEntry.place(x=280, y=0)

    checkKtp = ct.CTkButton(jrnalmng, text="КТП", command=viewWorks)
    checkKtp.place(x=0, y=28)

    jrnalmngMenu = CTkMenuBar(jrnalmng)
    jrnalmngMenu.place(x=0, y=56)
    jrnalmngMenu.add_cascade("Добавить оценку", postcommand=addMark)
    jrnalmngMenu.add_cascade("Удалить оценку", postcommand=delMark)

    jrnalmng.mainloop()

def journalViewManager():
    jrnlvm = ct.CTk()
    jrnlvm.title("Просмотр журнала")

    def marksByType():
        jtm = ct.CTk()
        jtm.title("Просмотр по типу")

        curs.execute("SELECT studentName, mark FROM journal WHERE type = ? ORDER BY studentName ASC", (typesCb.get(),))

        marksTable = CTkTable(jtm, values=curs.fetchall(), column=2, hover_color="black")
        marksTable.pack()

        df = pd.DataFrame(marksTable.get())

        exportToExcel = ct.CTkButton(jtm, text="Экспорт в Excel", command = lambda : df.to_excel(f"{typesCb.get()}.xlsx"))
        exportToExcel.pack()

        jtm.mainloop()
    
    def marksByStudent():
        jtm = ct.CTk()
        jtm.title("Просмотр по ученику")

        curs.execute("SELECT type, mark FROM journal WHERE studentName = ? ORDER BY studentName ASC", (studentCb.get(),))

        marksTable = CTkTable(jtm, values=curs.fetchall(), column=2, hover_color="black")
        marksTable.pack()

        df = pd.DataFrame(marksTable.get())

        exportToExcel = ct.CTkButton(jtm, text="Экспорт в Excel", command = lambda : df.to_excel(f"{studentCb.get()}.xlsx"))
        exportToExcel.pack()

        jtm.mainloop()

    studentCb = ct.CTkComboBox(jrnlvm, values=students)
    studentCb.pack()
    studentCb.set("Ученики")

    typesCb = ct.CTkComboBox(jrnlvm, values=types)
    typesCb.pack()
    typesCb.set("Типы")

    jrnlvmMenu = CTkMenuBar(jrnlvm)
    jrnlvmMenu.add_cascade("Просмотр по ученику", postcommand=marksByStudent)
    jrnlvmMenu.add_cascade("Просмотр по типу", postcommand=marksByType)

    jrnlvm.mainloop()

def viewWorks():
    vwr = ct.CTk()
    vwr.title("КТП работ")

    curs.execute("SELECT * FROM ktp")
    ktptbl = CTkTable(vwr, values=curs.fetchall())
    ktptbl.pack()
    
    df = pd.DataFrame(ktptbl.get())
    exportToExcel = ct.CTkButton(vwr, text="Экспорт в Excel", command = lambda : df.to_excel("график работ.xlsx"))
    exportToExcel.pack()

    vwr.mainloop()
        
def ktp():
    ktpr = ct.CTk()
    ktpr.title("Модуль КТП")
    ktpr.geometry("300x56")

    def addWork():
        try:
            curs.execute("INSERT INTO ktp(type, topic) VALUES (?, ?)", (ktpType.get(), ktpTopic.get()))
            conn.commit()
        except Exception as e:
            errormessage = CTkMessagebox(ktpr, title="Ошибка", message=f"Сообщите об ошибке разработчику!\n{e}", option_1="Сообщить")
            if errormessage.get() == "Сообщить":
                support()
        else:
            CTkMessagebox(ktpr, title="Готово!", message="Работа была успешно добавлена!")
    
    def delWork():
        try:
            curs.execute("DELETE FROM ktp WHERE topic = ?", (ktpTopic.get(),))
            conn.commit()
        except Exception as e:
            errormessage = CTkMessagebox(ktpr, title="Ошибка", message=f"Сообщите об ошибке разработчику!\n{e}", option_1="Сообщить")
            if errormessage.get() == "Сообщить":
                support()
        else:
            CTkMessagebox(ktpr, title="Готово!", message="Работа была успешно добавлена!")
    
    ktpType = ct.CTkComboBox(ktpr, values=types, width=150)
    ktpType.place(x=0, y=0)
    ktpType.set("Тип работы")

    ktpTopic = ct.CTkEntry(ktpr, placeholder_text="Тема работы", width=150)
    ktpTopic.place(x=155, y=0)

    ktprMenu = CTkMenuBar(ktpr)
    ktprMenu.add_cascade("Добавить", postcommand=addWork)
    ktprMenu.add_cascade("Удалить", postcommand=delWork)
    ktprMenu.add_cascade("Просмотр", postcommand=viewWorks)
    ktprMenu.place(x=0, y=28)

    ktpr.mainloop()
    

def modules():
    modr = ct.CTk()
    modr.title("Модули")

    ktpBtn = ct.CTkButton(modr, text="КТП работ", width=150, command=ktp)
    ktpBtn.grid(row=0, column=0)

    modr.mainloop()

menu = CTkMenuBar(root)
menu.add_cascade(text="Ученики", postcommand=studentsManager)
menu.add_cascade(text="Виды экзаменов", postcommand=typesManager)
menu.add_cascade(text="Журнал", postcommand=journalManager)
menu.add_cascade(text="Просмотр журнала", postcommand=journalViewManager)
menu.add_cascade(text="Доп. модули", postcommand=modules)

root.mainloop()
