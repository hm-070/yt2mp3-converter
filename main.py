from yt_dlp import YoutubeDL
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import math
import threading
import sys
import os


# Stage 3 gui done APART FROM ETA & CANCEL BUTTON
# Havent even started on stage 4

#Build Command is (MacOS):  

downloadLoc = ""
url = ""
wrappableToWinSize = []
options = {}
progress_value = 0



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x720")
        #self.giveMeDimensions()

        # TODO - In future make sure to just have title of "Youtube Converter" rendered here seperate of any frame

        self.stageList = {}

        for FrameClass in (stageOne_Start, stageTwo_Confirm, stageThree_Dowload, stageFour_End):
            frame = FrameClass(self)
            self.stageList[FrameClass] = frame

        #TODO - Change back to stageOne_Start for any builds
        self.showFrame(stageOne_Start)

    def showFrame(self, frame_class):
        for frame in self.stageList.values():
            frame.pack_forget()
        
        self.stageList[frame_class].pack(fill="both", expand=True)

    def giveMeDimensions(self):
        w = self.winfo_width()
        h = self.winfo_height()
        print(f"\nWidth: {w} || Height: {h}\n")
        self.after(100, self.giveMeDimensions)

    def update_width(self):
        global wrappableToWinSize
        width = self.winfo_width()-40
        for item in wrappableToWinSize:
            item.configure(wraplength=width)
        self.after(100, self.update_width)



class stageOne_Start(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global downloadLoc

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(self, text="TEMP TEST BUTTON", command=testRun).grid(row=99, column=1, padx=20, pady=20)

        ctk.CTkLabel(self, text="Youtube Converter - Stage 1").grid(row=0, column=1, padx=20, pady=20)
        self.urlEntry = ctk.CTkEntry(self, placeholder_text="Paste a Youtube or Youtube Music URL Here", width=400)
        self.urlEntry.grid(row=1 ,column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        self.chkBoxes = self.checkBoxFrame(master=self)
        self.chkBoxes.grid(row=2, column=0, padx=20, pady=20, columnspan=3)

        self.downloadPath = ctk.CTkLabel(self, text=f"Download Location: {downloadLoc}")
        self.downloadPath.grid(row=3, column=1, padx=20, pady=20)
        ctk.CTkButton(self, text="Change Download Location", command=changeDownloadLocation).grid(row=4, column=1, padx=20, pady=20)
        ctk.CTkButton(self, text="Load Video", command=lambda: self.saveURL(parent)).grid(row=5, column=1, padx=20, pady=20)
    
    class checkBoxFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, *kwargs)
            self.m4acheckBox = ctk.CTkCheckBox(self, text="m4a")
            self.mp4checkBox = ctk.CTkCheckBox(self, text="MP4")
            self.mp4checkBox.grid(row=1, column=1, padx=20, pady=20)
            self.m4acheckBox.grid(row=1, column=0, padx=20, pady=20)

    def saveURL(self, parent):
        global url
        url = self.urlEntry.get()
        app.stageList[stageTwo_Confirm].getMetadata()
        parent.showFrame(stageTwo_Confirm)



class stageTwo_Confirm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global wrappableToWinSize

        wrappableToWinSize.clear()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Youtube Converter - Stage 2")
        self.title.grid(row=0, column=1, padx=20, pady=20)
        wrappableToWinSize.append(self.title)

        self.btns = self.buttonFrame(master=self)
        self.btns.grid(row=99, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

        parent.update_width()

    class buttonFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            ctk.CTkButton(self, text="Back", command=lambda: master.master.showFrame(stageOne_Start)).grid(row=0, column=0, padx=20, pady=20)
            ctk.CTkButton(self, text="Download", command=startDownload).grid(row=0, column=1, padx=20, pady=20)

    #called in saveURL in stage one
    def getMetadata(self):
        with YoutubeDL() as ydl:
            self.info = ydl.extract_info(url, download=False)

        global wrappableToWinSize

        titleLabel = ctk.CTkLabel(self, text=f"Title: {self.info['title']}")
        titleLabel.grid(row=2, column=1, padx=20, pady=20)
        wrappableToWinSize.append(titleLabel)

        channelLabel = ctk.CTkLabel(self, text=f"Channel: {self.info['channel']}")
        channelLabel.grid(row=3, column=1, padx=20, pady=20)
        wrappableToWinSize.append(channelLabel)

        dur = self.getDur(self.info['duration'])
        durationLabel = ctk.CTkLabel(self, text=f"Duration: {dur}")
        durationLabel.grid(row=5, column=1, padx=20, pady=20)
        wrappableToWinSize.append(durationLabel)

        self.loadThumbnailImage(self.info['thumbnail'])

    def getDur(self, rawDur):
        rtn = ""
        if rawDur > 60:
            min = math.floor(rawDur/ 60)
            if min > 60:
                hr = math.floor(min / 60)
                rtn += f"{hr}hrs "
            rtn += f"{min}mins "
        sec = rawDur % 60
        rtn += f"{sec}secs "
        return rtn

    def loadThumbnailImage(self, urlLoc, max_size=(400,400)):
        response = requests.get(urlLoc)

        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size)

        self.thumbnail = ctk.CTkImage(light_image=img,  size=img.size)
        self.thumbnailLabel = ctk.CTkLabel(self, image=self.thumbnail, text="")
        self.thumbnailLabel.grid(row=1, column=1, padx=20, pady=20)
        wrappableToWinSize.append(self.thumbnailLabel)



class stageThree_Dowload(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global wrappableToWinSize
        wrappableToWinSize.clear()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Youtube Converter - Stage 3")
        self.title.pack(pady=20)
        wrappableToWinSize.append(self.title)

        self.tempButtons = self.tempButtonFrame(master=self)
        self.tempButtons.pack(pady=20)

        self.statusLabel = ctk.CTkLabel(self, text="Idle")
        self.statusLabel.pack(pady=20)
        wrappableToWinSize.append(self.statusLabel)

        self.progPanel = self.progressPanel(master=self)
        self.progPanel.pack(pady=20)

        self.ETALabel = ctk.CTkLabel(self, text="ETA: 11mths 30days 23hr 59min 59sec")
        self.ETALabel.pack(pady=20)
        wrappableToWinSize.append(self.ETALabel)

        parent.update_width()

    class tempButtonFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            ctk.CTkButton(self, text="TEMP NEXT BUTTON", command=lambda: master.master.showFrame(stageFour_End)).grid(row=1, column=1, padx=20)
            ctk.CTkButton(self, text="TEMP BACK", command=lambda: master.master.showFrame(stageTwo_Confirm)).grid(row=1, column=0, padx=20)

    class progressPanel(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            
            self.progressbar = ctk.CTkProgressBar(self, width=350)
            self.progressbar.set(0)
            self.progressbar.grid(row=0, column=0, padx=20)
            self.percentProgress = ctk.CTkLabel(self, text="100%")
            self.percentProgress.grid(row=0, column=1, padx=20)

            self.update_progBar()

        def update_progBar(self):
            global progress_value
            self.progressbar.set(progress_value)
            percenProg = math.floor(progress_value*100)
            self.percentProgress.configure(text=f"{percenProg}%")
            self.after(100, self.update_progBar)



class stageFour_End(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Youtube Converter - Stage 4").grid(row=0, column=1, padx=20, pady=20)
        ctk.CTkButton(self, text="TEMP BACK", command=lambda: parent.showFrame(stageThree_Dowload)).grid(row=1, column=0, padx=20, pady=20)





def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def testRun():
    url="https://www.youtube.com/watch?v=isGNQILKM0A"
    app.stageList[stageOne_Start].chkBoxes.mp4checkBox.select()
    app.stageList[stageOne_Start].urlEntry.insert(0, url)
    global downloadLoc
    downloadLoc = Path("/Users/harrym/Desktop/test downloads")
    app.stageList[stageOne_Start].downloadPath.configure(text=f"Download Location {downloadLoc}")

def changeDownloadLocation():
    global downloadLoc
    downloadLoc = Path(filedialog.askdirectory())
    app.stageList[stageOne_Start].downloadPath.configure(text=f"Download Location {downloadLoc}")
    print(downloadLoc)

def startDownload():
    global options, downloadLoc, progress_value
    progress_value = 0
    app.showFrame(stageThree_Dowload)
    checkBoxes = app.stageList[stageOne_Start].chkBoxes
    m4aCheck = checkBoxes.m4acheckBox.get()
    mp4Check = checkBoxes.mp4checkBox.get()
    if sys.platform.startswith("win"):
        if m4aCheck == 1:
            options = {
                "format": "m4a/bestaudio/best",
                "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
                "ffmpeg_location": resource_path("ffmpegWindows"),
                "writethumbnail": True,
                "embedthumbnail": True,
                "progress_hooks": [progress_hook],
                "postprocessors": [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                },
                {
                    "key": "EmbedThumbnail",
                },]
            }
        elif mp4Check == 1:
            options = {
                "format": "bestvideo[height>=1080]+bestaudio/bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
                "ffmpeg_location": resource_path("ffmpegWindows"),
                "writethumbnail": True,
                "embedthumbnail": True,
                "progress_hooks": [progress_hook],
                "postprocessors": [
                {
                    "key": "EmbedThumbnail",
                },],
            }
    elif sys.platform == "darwin":
        if m4aCheck == 1:
            options = {
                "format": "m4a/bestaudio/best",
                "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
                "ffmpeg_location": resource_path("ffmpegMac"),
                "writethumbnail": True,
                "embedthumbnail": True,
                "progress_hooks": [progress_hook],
                "postprocessors": [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                },
                {
                    "key": "EmbedThumbnail",
                },]
            }
        elif mp4Check == 1:
            options = {
                "format": "bestvideo[height>=1080]+bestaudio/bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": str(downloadLoc / "%(title)s.%(ext)s"),
                "ffmpeg_location": resource_path("ffmpegMac"),
                "writethumbnail": True,
                "embedthumbnail": True,
                "progress_hooks": [progress_hook],
                "postprocessors": [
                {
                    "key": "EmbedThumbnail",
                },],
            }

    threading.Thread(target=mainDownload, daemon=True).start()

def mainDownload():
    try:
        inp = app.stageList[stageOne_Start].urlEntry.get()
        stg3 = app.stageList[stageThree_Dowload]
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(inp, download=False)
            if "entries" in info:
                for video in info["entries"]:
                    app.after(0, lambda title=video["title"]: stg3.statusLabel.configure(text=f"Downloading {title}"))
                    ydl.download([video["webpage_url"]])
            else:
                app.after(0, lambda: stg3.statusLabel.configure(text=f"Downloading {info['title']}"))
                ydl.download([inp])
    except Exception as e:
        print("Download failed:", e)
        import traceback
        traceback.print_exc()
    app.after(0, lambda: stg3.statusLabel.configure(text="Finished Downloading"))

def progress_hook(d):
    global progress_value

    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        if total:
            progress_value = downloaded/total



app = App()
app.mainloop()