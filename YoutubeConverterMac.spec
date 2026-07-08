import sys

icon = "icon.icns"

a = Analysis(
    ["main.py"],

    binaries=[
        ("ffmpeg/ffmpeg", "ffmpeg"),
        ("ffmpeg/ffprobe", "ffmpeg"),
    ],

    datas=[
        ("icon.icns", "."),
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
    [],
    exclude_binaries=True,
    name="YoutubeConverter",
    console=False,
    icon=icon,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="YoutubeConverter",
)


app = BUNDLE(
    coll,
    name="YoutubeConverter.app",
    icon=icon,
    bundle_identifier="com.harry.youtubeconverter",
)