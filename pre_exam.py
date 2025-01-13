import smtplib
import ssl
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import mysql.connector


class Teacher:
    def __init__(self, root):
        self.root = root
        self.root.title("PRE-EXAMINATION SYSTEM")
        self.root.geometry("1350x700")
        self.root.maxsize(width=1350, height=700)
        title = Label(self.root, text="PreExamination System", bd=10,
                      relief=GROOVE,
                      font=("times new roman", 30, "bold"),
                      bg="yellow", fg="red")
        title.pack(side=TOP, fill=X)

        # variables
        self.UID_no_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.contact_no_var = StringVar()
        self.subject_var = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()

        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        Manage_Frame.place(x=10, y=90, width=480, height=580)
        m_title = Label(Manage_Frame, text="Manage Teacher", bg="crimson", fg="white",
                        font=("times new roman", 30, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)
        lbl_uidno = Label(Manage_Frame, text="UID No.", bg="crimson", fg="white",
                          font=("times new roman", 20, "bold"))
        lbl_uidno.grid(row=1, column=0, pady=10, sticky="w")
        txt_uidno = Entry(Manage_Frame, textvariable=self.UID_no_var,
                          font=("times new roman", 20, "bold"), bd=5, relief=GROOVE)
        txt_uidno.grid(row=1, column=1, pady=10, padx=4, sticky="w")

        lbl_name = Label(Manage_Frame, text="Name.", bg="crimson", fg="white",
                         font=("times new roman", 20, "bold"))
        lbl_name.grid(row=2, column=0, pady=10, sticky="w")

        txt_name = Entry(Manage_Frame, textvariable=self.name_var,
                         font=("times new roman", 20, "bold"), bd=5, relief=GROOVE)
        txt_name.grid(row=2, column=1, pady=10, padx=4, sticky="w")

        lbl_email = Label(Manage_Frame, text="Email.", bg="crimson", fg="white",
                          font=("times new roman", 20, "bold"))
        lbl_email.grid(row=3, column=0, pady=10, sticky="w")

        txt_email = Entry(Manage_Frame, textvariable=self.email_var,
                          font=("times new roman", 20, "bold"), bd=5, relief=GROOVE)
        txt_email.grid(row=3, column=1, pady=20, padx=5, sticky="w")

        lbl_contactno = Label(Manage_Frame, text="Contact No.",
                              bg="crimson", fg="white",
                              font=("times new roman", 20, "bold"))
        lbl_contactno.grid(row=4, column=0, pady=10, sticky="w")

        txt_contactno = Entry(Manage_Frame, textvariable=self.contact_no_var,
                              font=("times new roman", 20, "bold"), bd=5, relief=GROOVE)
        txt_contactno.grid(row=4, column=1, pady=10, padx=4, sticky="w")

        lbl_subject = Label(Manage_Frame, text="Subject", bg="crimson", fg="white",
                            font=("times new roman", 20, "bold"))
        lbl_subject.grid(row=5, column=0, pady=10, padx=4, sticky="w")

        combo_subject = ttk.Combobox(Manage_Frame, textvariable=self.subject_var,
                                     font=("times new roman", 20, "bold"), state="readonly")
        combo_subject['values'] = ("PHP Programming", "Python Programming", "Computer Network",
                                   "Operating System", "Cloud Computing", "Data Science")
        combo_subject.grid(row=5, column=1, pady=5, padx=1, sticky="w")

        # button frame
        btn_Frame = Frame(Manage_Frame, bd=4, relief=RIDGE, bg='crimson')
        btn_Frame.place(x=15, y=450, width=450)

        # add button
        Addbtn = Button(btn_Frame, text="Add", width=10, command=self.add_teachers)
        Addbtn.grid(row=0, column=0, padx=10, pady=10)

        updatebtn = Button(btn_Frame, text="Update", width=10, command=self.update_data)
        updatebtn.grid(row=0, column=2, padx=10, pady=10)

        deletebtn = Button(btn_Frame, text="Delete", width=10, command=self.delete_data)
        deletebtn.grid(row=0, column=3, padx=10, pady=10)

        clearbtn = Button(btn_Frame, text="Clear", width=10, command=self.clear)
        clearbtn.grid(row=0, column=4, padx=10, pady=10)

        # email send
        email_Frame = Frame(Manage_Frame, bd=4, relief=RIDGE, bg="crimson")
        email_Frame.place(x=150, y=510, width=150)
        sendmailbtn = Button(email_Frame, text="send mail", width=10, command=self.send_email)
        sendmailbtn.grid(row=0, column=0, padx=10, pady=10)
        Detail_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        Detail_Frame.place(x=500, y=90, width=950, height=580)

        lbl_search = Label(Detail_Frame, text="Search By.", bg="crimson",
                           fg="white", font=("times new roman", 20, "bold"))
        lbl_search.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        combo_search = ttk.Combobox(Detail_Frame, textvariable=self.search_by,
                                    font=("times new roman", 13, "bold"), width=10, state="readonly")
        combo_search['values'] = ("UID_no", "Name")
        combo_search.grid(row=0, column=1, pady=10, padx=20)

        txt_search = Entry(Detail_Frame, textvariable=self.search_txt,
                           font=("times new roman", 10, "bold"), width=20, bd=5, relief=GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")

        searchbtn = Button(Detail_Frame, text="Search", width=10, pady=5, command=self.search_data)
        searchbtn.grid(row=0, column=3, padx=20, pady=10)

        showallbtn = Button(Detail_Frame, text="Show all", width=10, pady=5, command=self.fetch_data)
        showallbtn.grid(row=0, column=4, padx=10, pady=10)

        # table frame
        Table_Frame = Frame(Detail_Frame, bd=4, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=830, height=500)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)

        self.Teacher_table = ttk.Treeview(Table_Frame, columns=("UID_no", "name", "email", "contactno", "subject"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.Teacher_table.xview)
        scroll_y.config(command=self.Teacher_table.yview)

        self.Teacher_table.heading("UID_no", text="Uid_no.")
        self.Teacher_table.heading("name", text="Name.")
        self.Teacher_table.heading("email", text="email.")
        self.Teacher_table.heading("contactno", text="contact_no.")
        self.Teacher_table.heading("subject", text="subject.")
        self.Teacher_table['show'] = 'headings'
        self.Teacher_table.column("UID_no", width=100)
        self.Teacher_table.column("name", width=100)
        self.Teacher_table.column("email", width=100)
        self.Teacher_table.column("contactno", width=100)
        self.Teacher_table.column("subject", width=100)
        self.Teacher_table.pack(fill=BOTH, expand=1)
        self.Teacher_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def add_teachers(self):
        if self.UID_no_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("error", "all fields required")
            return
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="pre_exam_system"
            )

            cur = con.cursor()
            cur.execute(
                """insert into teachers values(%s,%s,%s,%s,%s)""",
                (self.UID_no_var.get(), self.name_var.get(), self.email_var.get(),
                 self.contact_no_var.get(), self.subject_var.get())
            )
            con.commit()
            self.fetch_data()
            self.clear()
            con.close()
            messagebox.showinfo("success", "Teacher information is added successfully", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"due to {str(es)}", parent=self.root)

    def send_email(self):
        user_email = self.email_var.get()
        smpt_server = "smpt.gmail.com"
        port = 587
        sender_email = "kamleshnizare12345@gmail.com"
        password = " "
        context = ssl.create_default_context()
        server = smtplib.SMTP(smpt_server, port)
        server.ehlo()
        try:
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, user_email, "subject:{}\n{}".format('PreExam', 'Thanks for Your Support'))
        except Exception as e:
            # print any error message to stdout
            messagebox.showerror("Error", f"due to {str(e)}", parent=self.root)
        finally:
            server.quit()

    def fetch_data(self):
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='pre_exam_system'
        )
        cur = con.cursor()
        cur.execute("select * from teachers")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Teacher_table.delete(*self.Teacher_table.get_children())
            for row in rows:
                self.Teacher_table.insert("", END, values=row)
            con.commit()
        con.close()

    def clear(self):
        self.UID_no_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.contact_no_var.set("")
        self.subject_var.set("")

    def get_cursor(self, ev):
        cursor_row = self.Teacher_table.focus()
        contents = self.Teacher_table.item(cursor_row)
        row = contents['values']
        self.UID_no_var.set(row[0])
        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.contact_no_var.set(row[3])
        self.subject_var.set(row[4])

    def update_data(self):
        if self.UID_no_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("error", "all fields required")
        else:
            try:
                update = messagebox.askyesno("Update", "Are you sure update data", parent=self.root)
                if update > 0:
                    con = mysql.connector.connect(host='localhost', user='root', password='root',
                                                  database='pre_exam_system')
                    cur = con.cursor()
                    cur.execute("update teachers set name=%s,email=%s,contactno=%s,subject=%s where uid_no=%s",
                                (self.name_var.get(), self.email_var.get(),
                                 self.contact_no_var.get(), self.subject_var.get(), self.UID_no_var.get()))
                    con.commit()
                    self.fetch_data()
                    con.close()
                    messagebox.showinfo("success", "teachers data update successfully", parent=self.root)
                else:
                    if not update:
                        return

            except Exception as e:
                messagebox.showerror("Error", f"due to {str(e)}", parent=self.root)

    def delete_data(self):
        if self.UID_no_var.get() == "":
            messagebox.showerror("Error", "all fields are required", parent=self.root)
        else:
            try:
                Delete = messagebox.askyesno("Delete", "Are you sure the delete this data")

                if Delete > 0:
                    con = mysql.connector.connect(host='localhost', user='root', password='root',
                                                  database='pre_exam_system')
                    cur = con.cursor()
                    sql = "delete from teachers where uid_no=%s"
                    value = (self.UID_no_var.get(),)
                    cur.execute(sql, value)
                    con.commit()
                    self.fetch_data()
                    self.clear()
                    con.close()
                    messagebox.showinfo("Delete", "your data has been deleted", parent=self.root)
                else:
                    if not Delete:
                        return
            except Exception as e:
                messagebox.showerror("Error", f"due to {str(e)}", parent=self.root)

    def search_data(self):
        if self.search_txt.get() == "":
            messagebox.showerror("Error", "please select option", parent=self.root)
        else:
            try:
                con = mysql.connector.connect(host='localhost', user='root', password='root',
                                              database='pre_exam_system')
                cur = con.cursor()
                cur.execute("select * from teachers where uid_no = {}".format(self.search_txt.get()))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.Teacher_table.delete(*self.Teacher_table.get_children())
                    for row in rows:
                        self.Teacher_table.insert("", END, values=row)
                    con.commit()
                con.close()
            except Exception as e:
                messagebox.showerror("Error", f"due to {str(e)}", parent=self.root)
