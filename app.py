from flask import Flask, request, render_template, send_file
from moviepy.editor import ImageClip, AudioFileClip
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        audio = request.files['audio']

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
        image.save(image_path)
        audio.save(audio_path)

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
        video = image_clip.set_audio(audio_clip)

        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(OUTPUT_FOLDER, video_filename)
        video.write_videofile(video_path, fps=24)

        return send_file(video_path, as_attachment=True)

    return render_template('index.html')
