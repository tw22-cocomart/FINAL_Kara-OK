import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

from db import create_connection
from utils import hash_password

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        primary_blue = "#4A61E1"
        button_bg = "#E6FFC1"
        font_style = ("Courier New", 12, "bold")
        header_font = ("Courier New", 18, "bold")

        main_frame = tk.Frame(self, bg="white", padx=50, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            main_frame,
            text="CREATE AN ACCOUNT",
            font=header_font,
            fg=primary_blue,
            bg="white"
        ).pack(pady=(0, 20))

        # ------------------------------------------------
        #                     SIGNUP
        # ------------------------------------------------
        tk.Label(main_frame, text="Email", font=font_style, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        email = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1,
                         highlightbackground=primary_blue)
        email.pack(fill="x", ipady=8)

        tk.Label(main_frame, text="Username", font=font_style, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        username = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1,
                            highlightbackground=primary_blue)
        username.pack(fill="x", ipady=8)

        tk.Label(main_frame, text="Password", font=font_style, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        password = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1,
                            highlightbackground=primary_blue, show="*")
        password.pack(fill="x", ipady=8)

        tk.Label(main_frame, text="Confirm Password", font=font_style, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        confirm_password = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1,
                                   highlightbackground=primary_blue, show="*")
        confirm_password.pack(fill="x", ipady=8)

        def register():
            conn = create_connection()
            if not conn:
                return

            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username.get(), email.get(), hash_password(password.get()))
                )
                conn.commit()
                messagebox.showinfo("Success", "Account created!")
                controller.show_frame("LoginPage")
            except Error as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            main_frame,
            text="Register",
            font=font_style,
            fg=primary_blue,
            bg=button_bg,
            relief="groove",
            bd=1,
            padx=40,
            pady=5,
            command=register
        ).pack(pady=30)

        tk.Button(
            main_frame,
            text="Go to Login",
            font=font_style,
            fg=primary_blue,
            bg="white",
            bd=0,
            command=lambda: controller.show_frame("LoginPage")
        ).pack()