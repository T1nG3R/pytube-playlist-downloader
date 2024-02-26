import os

from moviepy.video.io import ffmpeg_tools
from pytube import Playlist, YouTube
from pytube.cli import on_progress


def download_video(video):
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
        print("")
        print(f"Audio for «{yt.title}» downloaded, merging video and audio")
        merged_video = f"merged {video_filename}"
        ffmpeg_tools.ffmpeg_merge_video_audio(video_filename, audio_filename, merged_video, logger=None)
        os.remove(video_filename)
        os.rename(merged_video, video_filename)
        os.remove(audio_filename)
        print(f"{video_filename} merged successfully")


def main():
    url = input('Enter url:\n')
    if 'playlist?list=' in url.lower():
        print("Entered playlist url, downloading videos:\n")
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            download_video(video_url)
    else:
        download_video(url)


if __name__ == "__main__":
    main()
