from flask import Blueprint, render_template, request
import uuid
import os
import subprocess
import wave

user = Blueprint('user', __name__)

ACTIONS = {}

# Ensure sounds directory exists
SOUND_FOLDER = "website/static/sounds"
os.makedirs(SOUND_FOLDER, exist_ok=True)

@user.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'upload' in request.form:
            sound = request.files['new_sound']

            if not sound.filename.endswith(".wav"):
                return "Only WAV files allowed", 400
            with wave.open(sound, 'rb') as w:
                if w.getnchannels() != 2 or w.getframerate() != 48000:
                    return "Only 48kHz stereo WAV files supported", 400
            
            save_path = os.path.join(SOUND_FOLDER, sound.filename)
            sound.save(save_path)

        if 'create_webhook' in request.form:
            sound_file = request.form['sound_file']
            if not sound_file:
                return "No sound file selected", 400
            uid = str(uuid.uuid4())
            full_path = os.path.join(SOUND_FOLDER, sound_file)
            ACTIONS[uid] = full_path
            return f"Webhook created! Send a POST to /webhook/{uid} to trigger <b>{sound_file}</b><br><a href='/'>Back</a>"

    existing_files = os.listdir(SOUND_FOLDER)
    return render_template('index.html', actions=ACTIONS, files=existing_files)

@user.route("/webhook/<uid>", methods=["POST"])
def webhook(uid):
    if uid not in ACTIONS:
        return "Invalid webhook ID", 404
    filename = ACTIONS[uid]
    subprocess.Popen(["aplay", "-D", "plughw:0,0", "-r", "48000", filename])
    return "Audio triggered!", 200
