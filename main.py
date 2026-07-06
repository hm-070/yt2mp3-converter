import re
from yt_dlp import YoutubeDL
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import threading

#download progress global value
progress_value = 0

#download location global value
downloadLoc = ""

def start_download():
    want_m4a = app.optionsFrame.m4acheckBox.get()
    want_mp4 = app.optionsFrame.mp4checkBox.get()
    if want_m4a == 1:
        threading.Thread(target=downloadAs_m4a, daemon=True).start()
    elif want_mp4 == 1:
        threading.Thread(target=downloadAs_MP4, daemon=True).start()

def downloadAs_MP4():
    global progress_value
    progress_value = 0
    inp = app.downloadFrame.urlEntry.get()
    options = {
        "format": "best",
        "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "embedthumbnail": True,
        "progress_hooks": [progress_hook],
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(inp, download=False)
        title = info["title"]
        app.statusFrame.statusLabel.configure(text=f"Downloading {title}")
    with YoutubeDL(options) as ydl:
        error_code = ydl.download([inp])
        print(error_code)
    app.statusFrame.statusLabel.configure(text="Finished Downloading")

def downloadAs_m4a():
    global progress_value
    progress_value = 0
    inp = app.downloadFrame.urlEntry.get()
    options = {
        "format": "m4a/bestaudio/best",
        "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "embedthumbnail": True,
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    app.statusFrame.statusLabel.configure(text="Downloading...")
    with YoutubeDL(options) as ydl:
        error_code = ydl.download([inp])
        print(error_code)
    app.statusFrame.statusLabel.configure(text="Finished Downloading")

def progress_hook(d):
    global progress_value

    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        if total:
            progress_value = downloaded/total

def update_progBar():
    app.statusFrame.progressbar.set(progress_value)
    app.after(100, update_progBar)

def updateDownloadLabel():
    global downloadLoc
    app.downloadFrame.downloadPath.configure(text=f"Download Location: {str(downloadLoc)}")

def changeDownloadLocation():
    global downloadLoc
    downloadLoc = Path(filedialog.askdirectory())
    updateDownloadLabel()
    print(downloadLoc)

class top_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title = ctk.CTkLabel(self, text="YouTube to MP3 Downloader")
        self.title.pack(padx=20)

class downloadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        global downloadLoc
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.urlEntry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL Here", width=400)
        self.button = ctk.CTkButton(self, text="Download", command=start_download)
        self.downloadPath = ctk.CTkLabel(self, text=f"Download Location: {str(downloadLoc)}")
        self.changeDownloadLocButton = ctk.CTkButton(self, text="Change Download Location", command=changeDownloadLocation)
        self.urlEntry.grid(row=0 ,column=0, padx=20, pady=20, sticky="ew", columnspan=3)
        self.button.grid(row=1, column=1, padx=20, pady=20)
        self.downloadPath.grid(row=2, column=1, padx=20, pady=20)
        self.changeDownloadLocButton.grid(row=3, column=1, padx=20, pady=20)

class statusFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.progressbar = ctk.CTkProgressBar(self, width=350)
        self.progressbar.set(0)
        self.statusLabel = ctk.CTkLabel(self ,text="Idle")
        self.statusLabel.pack(padx=20, pady=20)
        self.progressbar.pack(padx=20, pady=20)

class optionsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.m4acheckBox = ctk.CTkCheckBox(self, text="m4a")
        self.mp4checkBox = ctk.CTkCheckBox(self, text="MP4")
        self.warningLabel = ctk.CTkLabel(self, text="Tick only ONE option: ")

        self.warningLabel.grid(row=0, column=1, padx=20, pady=20)
        self.mp4checkBox.grid(row=1, column=2, padx=20, pady=20)
        self.m4acheckBox.grid(row=1, column=0, padx=20, pady=20)



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.geometry("600x720")

        self.top_frame = top_frame(master=self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", columnspan=4)

        self.downloadFrame = downloadFrame(master=self)
        self.downloadFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=4)

        self.statusFrame = statusFrame(master=self)
        self.statusFrame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew", columnspan=4)

        self.optionsFrame = optionsFrame(master=self)
        self.optionsFrame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan=4)

app = App()
update_progBar()
app.mainloop()