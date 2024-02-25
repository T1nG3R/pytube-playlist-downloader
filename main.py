import os

from moviepy.video.io import ffmpeg_tools
from pytube import Playlist, YouTube
from pytube.cli import on_progress

playlist_url = input('Enter playlist url:\n')
playlist = Playlist(playlist_url)

for video in playlist.video_urls:
    yt = YouTube(video, on_progress_callback=on_progress)
    video_streams = yt.streams.filter()
    best_video = sorted(video_streams, key=lambda x: int(x.resolution[:-1]) if x.resolution else 0, reverse=True)[0]
    print(f"«Downloading {yt.title}».")
    video_filename = f"{yt.title}.mp4"
    best_video.download(filename=video_filename)
    print("")
    if not best_video.includes_audio_track:
        print(f"«{yt.title}» has no audio track, downloading")
        audio_filename = f"{yt.title}.mp3"
        yt.streams.get_audio_only().download(filename=audio_filename)
        print(f"Audio for «{yt.title}» downloaded as «{audio_filename}»")
        merged_video = f"merged {video_filename}"
        ffmpeg_tools.ffmpeg_merge_video_audio(video_filename, audio_filename, merged_video, logger=None)
        os.remove(video_filename)
        os.rename(merged_video, video_filename)
        os.remove(audio_filename)
