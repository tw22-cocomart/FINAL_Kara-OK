import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

from db import create_connection
from utils import hash_password

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        primary_blue = "#4A61E1"
        button_lime = "#E6FFC1"
        font_mono = ("Courier New", 12, "bold")
        header_font = ("Courier New", 18, "bold")

        main_frame = tk.Frame(self, bg="white", padx=40)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            main_frame,
            text="LOG IN",
            font=header_font,
            fg=primary_blue,
            bg="white"
        ).pack(pady=(0, 30))

        # ------------------------------------------------
        #                   LOGIN
        # ------------------------------------------------
        tk.Label(main_frame, text="Email", font=font_mono, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        email = tk.Entry(main_frame, font=("Courier New", 12), bd=0,
                         highlightthickness=1, highlightbackground=primary_blue)
        email.pack(fill="x", ipady=10, ipadx=10)

        tk.Label(main_frame, text="Password", font=font_mono, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
        password = tk.Entry(main_frame, font=("Courier New", 12), bd=0,
                            highlightthickness=1, highlightbackground=primary_blue, show="*")
        password.pack(fill="x", ipady=10, ipadx=10)

        def login_user():
            conn = create_connection()
            if not conn:
                return

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email.get(),))
            user = cursor.fetchone()

            if user and user['password'] == hash_password(password.get()):
                messagebox.showinfo("Success", "Login successful")
                controller.show_frame("HomeKaraokePage")
                controller.current_user = user
                controller.frames["SettingsPage"].show_profile(user)
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(
            main_frame,
            text="Log In",
            font=font_mono,
            fg=primary_blue,
            bg=button_lime,
            relief="groove",
            bd=1,
            padx=50,
            pady=5,
            command=login_user
        ).pack(pady=40)

        tk.Button(
            main_frame,
            text="Go to Signup",
            font=font_mono,
            fg=primary_blue,
            bg="white",
            bd=0,
            command=lambda: controller.show_frame("RegisterPage")
        ).pack()
        