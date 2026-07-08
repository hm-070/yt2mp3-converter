# YoutubeConverterWindows.spec

icon = "icon.ico"

from PyInstaller.utils.hooks import collect_all

yt_dlp_datas, yt_dlp_binaries, yt_dlp_hidden = collect_all("yt_dlp")


a = Analysis(
    ["main.py"],

    pathex=[],

    binaries=[
        ("ffmpegWindows/ffmpeg.exe", "ffmpeg"),
        ("ffmpegWindows/ffprobe.exe", "ffmpeg"),
        *yt_dlp_binaries,
    ],

    datas=[
        ("icon.ico", "."),
        *yt_dlp_datas,
    ],

    hiddenimports=[
        "customtkinter",
        "PIL",
        *yt_dlp_hidden,
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
