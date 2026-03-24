import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="karaoke_system"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return None