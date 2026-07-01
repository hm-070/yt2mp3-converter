import re
from yt_dlp import YoutubeDL


def main():
    url = get_vidID_from_user_inp()

def get_vidID_from_user_inp():
    inp = input("Enter a Youtube URL: ")
    match = re.search(r'youtube\.com\/watch\?v=', inp)
    if match:
        print("Video ID: ", inp[match.end():])
        downloadAs_m4a(inp)
    else:
        print("No match")
        get_vidID_from_user_inp()
    return inp

def yt_dlpTest(inp):
    print("URL:", inp)
    options = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",
    }
    print("Creating YoutubeDL...")
    with YoutubeDL(options) as ydl:
        print("Starting download...")
        ydl.download([inp])
    print("Finished!")

def downloadAs_m4a(inp):
    print("URL:", inp)
    options = {
        "format": "m4a/bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    print("Creating YoutubeDL...")
    with YoutubeDL(options) as ydl:
        print("Starting download...")
        error_code = ydl.download([inp])
        print(error_code)
    print("Finished!")