import re
from yt_dlp import YoutubeDL

def main():
    url = get_vidID_from_user_inp()

def get_vidID_from_user_inp():
    inp = input("Enter a Youtube URL: ")
    match = re.search(r'youtube\.com\/watch\?v=', inp)
    if match:
        print("Video ID: ", inp[match.end():])
        yt_dlpTest(inp)
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

main()