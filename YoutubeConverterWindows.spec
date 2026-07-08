# YoutubeConverterWindows.spec

icon = "icon.ico"

a = Analysis(
    ["main.py"],

    binaries=[
        ("ffmpeg/ffmpeg.exe", "ffmpeg"),
        ("ffmpeg/ffprobe.exe", "ffmpeg"),
    ],

    datas=[
        ("icon.ico", "."),
    ],

    hiddenimports=[
        "customtkinter",
        "PIL",
        "yt_dlp",
    ],
)


pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="YoutubeConverter",
    console=False,
    icon=icon,
)