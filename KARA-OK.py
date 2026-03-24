import tkinter as tk
import ctypes
import service

from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.home_page import HomeKaraokePage
from pages.songbook_page import SongbookPage
from pages.settings_page import SettingsPage

DWMWA_CAPTION_COLOR = 35


class KaraOKApp(tk.Tk):
    def __init__(self):
        super().__init__()

        service.clear_queue()

        self.title("Kara-OK!")
        self.geometry("1150x750")
        self.configure(bg="white")

        self.state("zoomed")

        try:
            self.update()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            title_color = 0xE1614A
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
            )
        except Exception as e:
            print(f"Title bar color not supported: {e}")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (
            RegisterPage,
            LoginPage,
            HomeKaraokePage,
            SongbookPage,
            SettingsPage,
        ):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if page_name == "ScorePage":
            frame.refresh_score()

        for f in self.frames.values():
            if hasattr(f, "nav_buttons"):
                for btn_text, btn_obj in f.nav_buttons.items():
                    if f.nav_targets.get(btn_text) == page_name:
                        btn_obj.configure(font=("Courier New", 11, "bold", "underline"))
                    else:
                        btn_obj.configure(font=("Courier New", 11, "bold"))

        frame.tkraise()


if __name__ == "__main__":
    app = KaraOKApp()
    app.mainloop()
