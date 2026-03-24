import tkinter as tk
import service


class SongbookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        primary_blue = "#4A61E1"
        nav_dark_blue = "#2c3e8c"
        font_mono = ("Courier New", 11, "bold")
        song_font = ("Courier New", 12)
        nav_blue = "#283593"
        font_style = ("Courier New", 11, "bold")

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

        # --- Filter Bar ---
        filter_frame = tk.Frame(self, bg="white", pady=25)
        filter_frame.pack(fill="x", padx=50)

        # SEARCH FUNCTION
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            font=("Courier New", 11),
            fg="grey",
            highlightthickness=1,
            highlightbackground=primary_blue,
            bd=0,
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(15, 0), ipady=8)

        search_entry.bind("<KeyRelease>", self.update_song_list)
        search_entry.bind("<Return>", self.update_song_list)
        
        search_entry.insert(0, "Search...")

        def on_focus_in(event):
            if search_entry.get() == "Search...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Search...")
                search_entry.config(fg="grey")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        # ------------------------------------------------
        #                  SONG SECTION
        # ------------------------------------------------
        self.table_container = tk.Frame(self, bg="white", padx=50)
        self.table_container.pack(fill="both", expand=True)

        service.init_backend()
        self.all_songs = service.get_all_songs()
        self.draw_song_list(self.all_songs)

    def draw_song_list(self, songs):
        """Clear and redraw the song list based on the given songs."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        def draw_gradient(event, start_color, end_color):
            canvas = event.widget
            canvas.delete("grad")
            w, h = event.width, event.height
            r1, g1, b1 = self.winfo_rgb(start_color)
            r2, g2, b2 = self.winfo_rgb(end_color)
            r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
            r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
            for i in range(h):
                nr = int(r1 + (r2 - r1) * (i / h))
                ng = int(g1 + (g2 - g1) * (i / h))
                nb = int(b1 + (r2 - b1) * (i / h))
                color = f"#{nr:02x}{ng:02x}{nb:02x}"
                canvas.create_line(0, i, w, i, fill=color, tags="grad")
            canvas.tag_lower("grad")

        if songs:
            featured = songs[0]
            feat_canvas = tk.Canvas(
                self.table_container,
                height=85,
                highlightthickness=1,
                highlightbackground="#4A61E1",
                bd=0,
            )
            feat_canvas.pack(fill="x", pady=(0, 10))
            feat_canvas.bind(
                "<Configure>", lambda e: draw_gradient(e, "#e1f0ff", "#FFFFFF")
            )

            tk.Label(
                feat_canvas,
                text="✦ FEATURED SONG",
                font=("Courier New", 11, "bold"),
                fg="#4A61E1",
                bg="#e1f0ff",
            ).place(x=20, y=10)
            tk.Label(
                feat_canvas,
                text=featured["id"],
                font=("Courier New", 12),
                bg="#f0f8ff",
                width=12,
                anchor="w",
            ).place(x=20, y=48)
            tk.Label(
                feat_canvas,
                text=featured["title"],
                font=("Courier New", 12),
                bg="#f0f8ff",
                width=35,
                anchor="w",
            ).place(x=150, y=48)
            tk.Label(
                feat_canvas,
                text=featured["artist"],
                font=("Courier New", 12),
                bg="#f0f8ff",
                anchor="w",
            ).place(relx=0.7, y=48)


        for song in songs[1:]:
            code = song["id"]
            title = song["title"]
            artist = song["artist"]
            is_highlighted = code == "03297"

            if is_highlighted:
                row_canvas = tk.Canvas(
                    self.table_container, height=50, highlightthickness=0, bd=0
                )
                row_canvas.pack(fill="x")
                row_canvas.bind(
                    "<Configure>", lambda e: draw_gradient(e, "#E6FFC1", "#FFFFFF")
                )
                tk.Label(
                    row_canvas,
                    text=code,
                    font=("Courier New", 12),
                    bg="#f1ffd9",
                    fg="#2c3e8c",
                    width=12,
                    anchor="w",
                ).place(x=20, y=12)
                tk.Label(
                    row_canvas,
                    text=title,
                    font=("Courier New", 12),
                    bg="#f1ffd9",
                    fg="#2c3e8c",
                    width=35,
                    anchor="w",
                ).place(x=150, y=12)
                tk.Label(
                    row_canvas,
                    text=artist,
                    font=("Courier New", 12),
                    bg="#f1ffd9",
                    fg="#2c3e8c",
                    anchor="w",
                ).place(relx=0.7, y=12)
            else:
                row_frame = tk.Frame(self.table_container, bg="white", bd=0)
                row_frame.pack(fill="x")
                tk.Label(
                    row_frame,
                    text=code,
                    font=("Courier New", 12),
                    bg="white",
                    fg="#2c3e8c",
                    width=12,
                    anchor="w",
                ).pack(side="left", padx=(20, 0), pady=12)
                tk.Label(
                    row_frame,
                    text=title,
                    font=("Courier New", 12),
                    bg="white",
                    fg="#2c3e8c",
                    width=35,
                    anchor="w",
                ).pack(side="left", pady=12)
                artist_lbl = tk.Label(
                    row_frame,
                    text=artist,
                    font=("Courier New", 12),
                    bg="white",
                    fg="#2c3e8c",
                    anchor="w",
                )
                artist_lbl.place(relx=0.7, rely=0.5, anchor="w")

            tk.Frame(self.table_container, bg="#4A61E1", height=1).pack(fill="x")

    def update_song_list(self, event=None):
        """Filter songs based on search bar input."""
        query = self.search_var.get().strip()
        if query:
            filtered = service.search_songs(query)
            self.draw_song_list(filtered)
        else:
            self.draw_song_list(self.all_songs)
