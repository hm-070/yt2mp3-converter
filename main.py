from yt_dlp import YoutubeDL
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from PIL import Image
import math
import threading

# Stage one gui done

downloadLoc = ""
url = ""
wrappableToWinSize = []

def changeDownloadLocation():
    global downloadLoc
    downloadLoc = Path(filedialog.askdirectory())
    app.stageList[stageOne_Start].downloadPath.configure(text=f"Download Location {downloadLoc}")
    print(downloadLoc)

def startDownload():
    print("Download Started")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x720")

        # TODO - In future make sure to just have title of "Youtube Converter" rendered here seperate of any frame

        self.stageList = {}

        for FrameClass in (stageOne_Start, stageTwo_Confirm):
            frame = FrameClass(self)
            self.stageList[FrameClass] = frame

        self.showFrame(stageOne_Start)

    def showFrame(self, frame_class):
        for frame in self.stageList.values():
            frame.pack_forget()
        
        self.stageList[frame_class].pack(fill="both", expand=True)


class stageOne_Start(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        global downloadLoc

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Youtube Converter - Stage 1").grid(row=0, column=1, padx=20, pady=20)
        self.urlEntry = ctk.CTkEntry(self, placeholder_text="Paste a Youtube or Youtube Music URL Here", width=400)
        self.urlEntry.grid(row=1 ,column=0, padx=20, pady=20, sticky="ew", columnspan=3)
        self.downloadPath = ctk.CTkLabel(self, text=f"Download Location: {downloadLoc}")
        self.downloadPath.grid(row=2, column=1, padx=20, pady=20)
        ctk.CTkButton(self, text="Change Download Location", command=changeDownloadLocation).grid(row=3, column=1, padx=20, pady=20)
        ctk.CTkButton(self, text="Load Video", command=lambda: self.saveURL(parent)).grid(row=4, column=1, padx=20, pady=20)
    
    def saveURL(self, parent):
        global url
        url = self.urlEntry.get()
        app.stageList[stageTwo_Confirm].getMetadata()
        parent.showFrame(stageTwo_Confirm)


class stageTwo_Confirm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Youtube Converter - Stage 2").grid(row=0, column=1, padx=20, pady=20)
        # TODO - Thumbnail displayed here need to write script to find the thumbnail that was downloaded (should just be title.png or title.webp in same dir)
        # self.loadThumbnailImage(path goes here)
        self.btns = self.buttonFrame(master=self)
        self.btns.grid(row=99, column=0, padx=20, pady=20, sticky="ew", columnspan=3)

    class buttonFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

            ctk.CTkButton(self, text="Back", command=lambda: master.parent.showFrame(stageOne_Start)).grid(row=0, column=0, padx=20, pady=20)
            ctk.CTkButton(self, text="Download", command=startDownload).grid(row=0, column=1, padx=20, pady=20)


    #called in saveURL in stage one
    def getMetadata(self):
        with YoutubeDL() as ydl:
            self.info = ydl.extract_info(url, download=False)

        global wrappableToWinSize

        self.update_width()
        print(f"\n\n\nWidth: {self.width}\n\n\n")

        titleLabel = ctk.CTkLabel(self, text=f"Title: {self.info['title']}", wraplength=self.width)
        titleLabel.grid(row=2, column=1, padx=20, pady=20)
        wrappableToWinSize.append(titleLabel)

        channelLabel = ctk.CTkLabel(self, text=f"Channel: {self.info['channel']}", wraplength=self.width)
        channelLabel.grid(row=3, column=1, padx=20, pady=20)
        wrappableToWinSize.append(channelLabel)

        dur = self.getDur(self.info['duration'])
        durationLabel = ctk.CTkLabel(self, text=f"Duration: {dur}", wraplength=self.width)
        durationLabel.grid(row=5, column=1, padx=20, pady=20)
        wrappableToWinSize.append(durationLabel)

    def update_width(self):
        global wrappableToWinSize
        self.width = app.winfo_width()-40
        for item in wrappableToWinSize:
            item.configure(wraplength=self.width)
        app.after(100, self.update_width)

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
        print(f"\n\n\n--------------------------------------\nRTN:{rtn}\n\n\n")
        return rtn


    def loadThumbnailImage(self, path, max_size=(400,400)):
        img = Image.open(path)
        img.thumbnail(max_size)
        ctk.CTkImage(self, light_image=Image.open(path), size=(400, 400))

app = App()
app.mainloop()