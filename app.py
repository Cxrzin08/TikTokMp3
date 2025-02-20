from flask import Flask, request, render_template, send_file
import requests
import os
from moviepy import VideoFileClip
from pytube import YouTube

app = Flask(__name__)

TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension="mp4").first()
    filename = os.path.join(TEMP_FOLDER, "video.mp4")
    video.download(filename=filename)
    return filename

def remove_watermark(video_path):
    return video_path 

def convert_to_mp3(video_path):
    audio_path = os.path.join(TEMP_FOLDER, "audio.mp3")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("url")
        
        if not video_url:
            return render_template("index.html", error="URL do vídeo é obrigatória")
        
        try:
            video_path = download_video(video_url)
            clean_video_path = remove_watermark(video_path)
            audio_path = convert_to_mp3(clean_video_path)
            return send_file(audio_path, as_attachment=True)
        except Exception as e:
            return render_template("index.html", error=str(e))
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)