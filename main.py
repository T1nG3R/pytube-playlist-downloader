from pytube import Playlist
from moviepy.video.io import ffmpeg_tools
import os

playlist_url = input('Enter playlist url:\n')
playlist = Playlist(playlist_url)

for video in playlist.videos:
    video_streams = video.streams.filter()
    best_video = sorted(video_streams, key=lambda x: int(x.resolution[:-1]) if x.resolution else 0, reverse=True)[0]
    print(f"«{video.title}» downloading.")
    video_filename = f"{video.title}.mp4"
    best_video.download(filename=video_filename)
    print(f"«{video.title}» downloaded.")
    if not best_video.includes_audio_track:
        print(f"«{video.title}» has no audio track, downloading")
        audio_filename = f"{video.title}.mp3"
        video.streams.get_audio_only().download(filename=audio_filename)
        print(f"Audio for «{video.title}» downloaded as «{audio_filename}»")
        final_video = f"final {video_filename}"
        ffmpeg_tools.ffmpeg_merge_video_audio(video_filename, audio_filename, final_video)
        os.remove(video_filename)
        os.rename(final_video, video_filename)
        os.remove(audio_filename)
