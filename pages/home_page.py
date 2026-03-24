import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
import vlc, os
import service

from db import create_connection
from utils import hash_password


class HomeKaraokePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#CCEEFF")
        self.controller = controller

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

        main_container = tk.Frame(self, bg="#CCEEFF")
        main_container.pack(expand=True, fill="both", padx=15, pady=15)

        service.init_backend()

        # ------------------------------------------------
        #               MAIN KARAOKE SECTION
        # ------------------------------------------------
        left_frame = tk.Frame(main_container, bg="#CCEEFF")
        left_frame.pack(side="left", expand=True, fill="both")

        # VIDEO
        video_box = tk.Frame(
            left_frame, bg="black", highlightbackground="#448AFF", highlightthickness=2
        )
        video_box.pack(pady=(10, 10), fill="both", expand=True)

        self.video_panel = tk.Frame(video_box, bg="black")
        self.video_panel.pack(fill="both", expand=True)

        # VLC
        vlc_path = r"C:\Program Files\VideoLAN\VLC"
        os.environ["PATH"] = vlc_path + ";" + os.environ["PATH"]
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        events = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_song_end)

        # BUTTONS
        controls = tk.Frame(video_box, bg="#222")
        controls.pack(fill="x")
        tk.Button(controls, text="▶ Play", command=self.safe_play).pack(
            side="left", padx=5
        )
        tk.Button(controls, text="⏸ Pause", command=self.player.pause).pack(
            side="left", padx=5
        )
        tk.Button(controls, text="⏹ Stop", command=self.player.stop).pack(
            side="left", padx=5
        )
        tk.Button(controls, text="⏭ Skip", command=self.skip_song).pack(
            side="left", padx=5
        )
        tk.Button(controls, text="🔉", command=self.volume_down).pack(
            side="left", padx=5
        )
        tk.Button(controls, text="🔊", command=self.volume_up).pack(side="left", padx=5)
        tk.Button(controls, text="🔇", command=self.toggle_mute).pack(
            side="left", padx=5
        )

        self.overlay_text = tk.Label(
            video_box,
            text="No song playing",
            fg="yellow",
            bg="black",
            font=("Courier", 14, "bold"),
        )
        self.overlay_text.place(relx=0.5, rely=0.9, anchor="center")

        # QUEUE
        self.current_video_id = None
        self.queue_frame = tk.Frame(left_frame, bg="white", bd=1, relief="solid")
        self.queue_frame.pack(fill="x", pady=10)
        self.queue_label = tk.Label(
            self.queue_frame,
            text="",
            bg="white",
            fg="#283593",
            font=("Courier", 10),
            pady=15,
        )
        self.queue_label.pack()

        self.update_queue_display()
        self.update_current_song_display()
        self.play_video_for_current_song()

        # REMOTE
        right_frame = tk.Frame(
            main_container, bg="white", width=320, bd=1, relief="solid"
        )
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        self.entry_var = tk.StringVar(value="")
        input_entry = tk.Entry(
            right_frame,
            textvariable=self.entry_var,
            font=("Courier", 14),
            fg="#283593",
            bd=1,
            relief="solid",
            justify="center",
        )
        input_entry.pack(pady=30, padx=25, fill="x")

        keypad_frame = tk.Frame(right_frame, bg="white")
        keypad_frame.pack()
        buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "DEL", "0", "RES"]
        r, c = 0, 0
        for b in buttons:
            color = "#E1F5FE"
            if b == "DEL":
                color = "#FFCDD2"
            if b == "RES":
                color = "#DCEDC8"
            btn = tk.Button(
                keypad_frame,
                text=b,
                width=7,
                height=2,
                bg=color,
                font=("Courier", 10, "bold"),
                command=lambda x=b: self.press(x),
            )
            btn.grid(row=r, column=c, padx=4, pady=4)
            c += 1
            if c > 2:
                c = 0
                r += 1

    # ------------------------------------------------
    #               VIDEO STUFF OPTIONS
    # ------------------------------------------------

    def get_video_path(self, song_id: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, f"videos/{song_id}.mp4")

    def play_video_for_current_song(self):
        if (
            not hasattr(self.controller, "current_user")
            or not self.controller.current_user
        ):
            self.player.stop()
            self.overlay_text.config(text="Use the remote to add songs to queue...")
            self.current_video_id = None
            return

        current = service.current_song()
        if not current:
            self.player.stop()
            self.overlay_text.config(text="No song playing")
            self.current_video_id = None
            return

        song_id = current["id"]

        if self.current_video_id == song_id:
            return

        self.current_video_id = song_id
        video_path = self.get_video_path(song_id)

        if os.path.exists(video_path):
            media = self.instance.media_new(video_path)
            self.player.set_media(media)

            if os.name == "nt":
                self.player.set_hwnd(self.video_panel.winfo_id())
            else:
                self.player.set_xwindow(self.video_panel.winfo_id())

            self.player.play()
        else:
            self.player.stop()
            self.overlay_text.config(text=f"❌ No video for {song_id}")

    def safe_play(self):
        if (
            not hasattr(self.controller, "current_user")
            or not self.controller.current_user
        ):
            self.overlay_text.config(text="Please log in to play songs")
            return
        self.player.play()

    def press(self, key):
        if key == "DEL":
            self.entry_var.set(self.entry_var.get()[:-1])
        elif key == "RES":
            song_id = self.entry_var.get()
            try:
                service.reserve_song(song_id)
                self.update_queue_display()
                self.update_current_song_display()
                self.play_video_for_current_song()
            except ValueError as e:
                print("Error:", e)
            self.entry_var.set("")
        else:
            self.entry_var.set(self.entry_var.get() + key)

    def update_queue_display(self):
        q = service.get_queue()
        self.queue_label.config(
            text="Song Queue: " + ", ".join(q) if q else "Song Queue: (empty)"
        )

    def update_current_song_display(self):
        current = service.current_song()
        if current:
            self.overlay_text.config(
                text=f"{current['id']} | {current['title']} | {current['artist']}"
            )
        else:
            self.overlay_text.config(text="No song playing")

    def skip_song(self):
        service.skip_current()
        self.current_video_id = None 
        self.update_queue_display()
        self.update_current_song_display()
        self.play_video_for_current_song()

    def on_song_end(self, event):
        service.skip_current()
        self.current_video_id = None
        self.update_queue_display()
        self.update_current_song_display()
        self.play_video_for_current_song()

    def volume_up(self):
        current = self.player.audio_get_volume()
        if current < 100:
            self.player.audio_set_volume(min(100, current + 10))

    def volume_down(self):
        current = self.player.audio_get_volume()
        if current > 0:
            self.player.audio_set_volume(max(0, current - 10))

    def toggle_mute(self):
        self.player.audio_toggle_mute()