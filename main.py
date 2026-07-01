def main():
    url = get_user_input()

    validate_url(url)

    video = get_video_information(url)

    audio_file = download_audio(video)

    mp3_file = convert_to_mp3(audio_file)

    add_metadata(mp3_file, video)

    print("finished")