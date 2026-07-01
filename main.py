import re
from yt_dlp import YoutubeDL
import customtkinter as ctk
import threading

#download progress global value
progress_value = 0

def start_download():
    threading.Thread(target=downloadAs_m4a, daemon=True).start()

def downloadAs_m4a():
    global progress_value
    progress_value = 0
    inp = urlEntry.get()
    options = {
        "format": "m4a/bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    statusLabel.configure(text="Downloading...")
    with YoutubeDL(options) as ydl:
        error_code = ydl.download([inp])
        print(error_code)
    statusLabel.configure(text="Finished Downloading")

def progress_hook(d):
    global progress_value

    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        if total:
            progress_value = downloaded/total

def update_progBar():
    progressbar.set(progress_value)
    app.after(100, update_progBar)

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(2, weight=1)
app.geometry("400x400")
title = ctk.CTkLabel(app, text="YouTube to MP3 Downloader")
button = ctk.CTkButton(app, text="Download", command=start_download)
urlEntry = ctk.CTkEntry(app, placeholder_text="Paste YouTube URL Here", width=400)
progressbar = ctk.CTkProgressBar(app, width=350)
statusLabel = ctk.CTkLabel(app ,text="Idle")
progressbar.set(0)
statusLabel.grid(row=3, column=1, padx=20, pady=20)
progressbar.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
title.grid(row=0, column=1, padx=20, pady=20)
urlEntry.grid(row=1 ,column=0, padx=20, pady=20, sticky="ew", columnspan=3)
button.grid(row=2, column=1, padx=20, pady=20)
update_progBar()
app.mainloop()