import mysql.connector
import sys
from tkinter import Tk

if __name__ == '__main__':
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='pre_exam_system'
        )
    except mysql.connector.DatabaseError as error:
        print(error)
        sys.exit()

    else:
        cursor = con.cursor()
        create_query = """
        create table if not exists teachers(
        uid_no varchar(64),
        name varchar(64),
        email varchar(64),
        contactno varchar(64),
        subject varchar(64)
        );
        """
        cursor.execute(create_query)
        root = Tk()
        from pre_exam import *
        obj = Teacher(root)
        root.mainloop()

    finally:
        if "con" in locals():
            cursor.close()
            con.close()
