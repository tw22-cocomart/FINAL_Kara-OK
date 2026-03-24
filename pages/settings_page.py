import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk

from db import create_connection
from utils import hash_password


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        primary_blue = "#4A61E1"
        button_bg = "#E6FFC1"
        nav_blue = "#2c3e8c"
        font_style = ("Courier New", 11, "bold")
        header_font = ("Courier New", 18, "bold")

        # ------------------------------------------------
        #               NAVIGATION BAR
        # ------------------------------------------------
        nav_frame = tk.Frame(self, bg=nav_blue, height=45)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        self.nav_targets = {
            "Karaoke": "HomeKaraokePage",
            "SongBook": "SongbookPage",
            "Settings": "SettingsPage",
        }

        tabs = ["Karaoke", "SongBook", "Settings"]
        targets = ["HomeKaraokePage", "SongbookPage", "SettingsPage"]

        for tab, target in zip(tabs, targets):
            btn = tk.Button(
                nav_frame,
                text=tab,
                bg=nav_blue,
                fg="white",
                font=font_style,
                bd=0,
                padx=20,
                activebackground="#3d51b3",
                activeforeground="white",
                cursor="hand2",
                command=lambda t=target: controller.show_frame(t),
            )
            btn.pack(side="left", fill="y")
            self.nav_buttons[tab] = btn

        # ------------------------------------------------
        #                   USER PROFILE
        # ------------------------------------------------
        content_area = tk.Frame(self, bg="white")
        content_area.pack(fill="both", expand=True)

        # ------------------------------------------------
        #                     PROFILE
        # ------------------------------------------------
        sidebar = tk.Frame(content_area, bg="#f2f2f2")
        sidebar.place(relx=0, rely=0, relwidth=0.28, relheight=1)

        profile_box = tk.Frame(
            sidebar,
            bg="#448AFF",
            width=160,
            height=160,
            highlightthickness=3,
            highlightbackground="#448AFF",
        )
        profile_box.pack(pady=(60, 15))
        profile_box.pack_propagate(False)

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
            print("FILES:", os.listdir(base_dir))

            img_path = os.path.join(base_dir, "pfp.jpg")
            print("LOOKING FOR:", img_path)

            img = Image.open(img_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            self.profile_img = ImageTk.PhotoImage(img)

            img_label = tk.Label(profile_box, image=self.profile_img, bg="#7f8c8d")
            img_label.pack(expand=True)

        except Exception as e:
            print("ERROR:", e)
            tk.Label(
                profile_box,
                text="No Image",
                bg="#7f8c8d",
                fg="white"
            ).pack(expand=True)

        self.name_label = tk.Label(
            sidebar, text="", bg="#f2f2f2", font=("Courier New", 14, "bold")
        )
        self.name_label.pack(pady=(80, 5))

        self.username_label = tk.Label(
            sidebar, text="", bg="#f2f2f2", fg="grey", font=("Courier New", 11)
        )
        self.username_label.pack()

        tk.Button(
            sidebar,
            text="logout",
            fg=primary_blue,
            bg="#f2f2f2",
            bd=0,
            font=("Courier New", 11, "underline"),
            cursor="hand2",
            command=lambda: controller.show_frame("LoginPage"),
        ).pack(side="bottom", pady=40)

        # ------------------------------------------------
        #                       INFO
        # ------------------------------------------------
        self.form_frame = tk.Frame(content_area, bg="white", padx=50)
        self.form_frame.place(relx=0.28, rely=0, relwidth=0.72, relheight=1)

        def create_input(label_text, default_val):
            row = tk.Frame(self.form_frame, bg="white")
            row.pack(fill="x", pady=12, padx=(0, 50))

            tk.Label(
                row,
                text=label_text,
                font=font_style,
                fg=primary_blue,
                bg="white",
                width=12,
                anchor="e",
            ).pack(side="left", padx=15)

            entry = tk.Entry(
                row,
                font=("Courier New", 12),
                bd=0,
                highlightthickness=1,
                highlightbackground=primary_blue,
                highlightcolor=primary_blue,
            )
            entry.insert(0, default_val)
            entry.pack(side="left", fill="x", expand=True, ipady=8)

            return entry

        self.create_input = create_input

    def show_profile(self, user):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        primary_blue = "#4A61E1"
        button_bg = "#E6FFC1"
        font_style = ("Courier New", 11, "bold")
        header_font = ("Courier New", 18, "bold")

        self.name_label.config(text=user["username"])
        self.username_label.config(text=f"@{user['username']}")

        tk.Label(
            self.form_frame,
            text="USER PROFILE",
            font=header_font,
            fg=primary_blue,
            bg="white",
        ).pack(pady=(60, 40))

        username_entry = self.create_input("Username", user["username"])
        email_entry = self.create_input("Email", user["email"])
        password_entry = self.create_input("Password", "")
        password_entry.config(show="*")

        show_password = tk.BooleanVar(value=False)

        def toggle_password():
            if show_password.get():
                password_entry.config(show="")
            else:
                password_entry.config(show="*")

        tk.Checkbutton(
            self.form_frame,
            text="Show Password",
            variable=show_password,
            command=toggle_password,
            bg="white",
        ).pack()

        def save_changes():
            conn = create_connection()
            if not conn:
                return

            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                    (
                        username_entry.get(),
                        email_entry.get(),
                        hash_password(password_entry.get()),
                        user["id"],
                    ),
                )
                conn.commit()
                messagebox.showinfo("Success", "Profile updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                cursor.close()
                conn.close()

        tk.Button(
            self.form_frame,
            text="Save Changes",
            font=font_style,
            fg=primary_blue,
            bg=button_bg,
            relief="groove",
            bd=1,
            padx=50,
            pady=10,
            cursor="hand2",
            command=save_changes,
        ).pack(pady=30)
