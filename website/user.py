from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
import uuid
import os
import subprocess
import werkzeug
from werkzeug.utils import secure_filename
from website.forms.user_forms import FirstLoginForm, SoundFileForm, CreateWebhookForm
from .models import db, User, SoundFile, Webhook
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import wave
from website import csrf

user = Blueprint('user', __name__)

ACTIONS = {}
SOUND_FOLDER = "website/static/sounds"
os.makedirs(SOUND_FOLDER, exist_ok=True)

# Utility function to validate user access to their own resources
def verify_user(username):
    if current_user.username != username:
        abort(403, "Unauthorized access.")

def is_valid_wav(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            return True
    except wave.Error:
        return False

@user.route("/<username>/user-welcome/")
@login_required
def userFirstLogin(username):
    form = FirstLoginForm()

    return render_template('user-first-login.html', username=username, form=form)

@user.route("/<username>/user-welcome/complete", methods=['POST'])
@login_required
def userFirstLoginComplete(username):
    verify_user(username)

    userToChange = User.query.filter_by(username=username).first_or_404()

    if userToChange.first_login:
        userToChange.first_login = False
        db.session.commit()

    return redirect(url_for('user.userDashboard', username=username))

@user.route("/<username>/dashboard/")
@login_required
def userDashboard(username):
    verify_user(username)
    sound_files = SoundFile.query.filter_by(owner=current_user.user_id).all()
    webhooks = Webhook.query.join(SoundFile).filter(SoundFile.owner == current_user.user_id).all()

    webhook_form = CreateWebhookForm()
    webhook_form.soundFileSelect.choices = [(sf.sound_id, sf.filename) for sf in sound_files]
    sound_file_form = SoundFileForm()

    return render_template('user-dashboard.html', username=username,
                            webhook_form=webhook_form, sound_file_form=sound_file_form,
                            sound_files=sound_files, webhooks=webhooks)

@user.route("/<username>/dashboard/webhook/")
@login_required
def userWebhookPage(username):
    verify_user(username)
    form = CreateWebhookForm()

    soundFiles = SoundFile.query.filter_by(owner=current_user.user_id).all()

    form.soundFileSelect.choices = [(sf.sound_id, sf.sound_name) for sf in soundFiles]

    # Get webhooks for this user
    webhooks = Webhook.query.filter_by(owner=current_user.user_id).all()

    return render_template('user-webhook-page.html', username=username, form=form, webhooks=webhooks)

@user.route("/<username>/webhook/create/", methods=['POST'])
@login_required
def userCreateWebhook(username):
    verify_user(username)
    form = CreateWebhookForm()
    form.soundFileSelect.choices = [
        (sf.sound_id, sf.filename)
        for sf in SoundFile.query.filter_by(owner=current_user.user_id).all()
    ]

    if form.validate_on_submit():
        sound_file_id = form.soundFileSelect.data
        webhook_name = form.webhookName.data  # <-- Get webhook name from form

        # Verify the sound file belongs to current user
        sound_file = SoundFile.query.filter_by(sound_id=sound_file_id, owner=current_user.user_id).first()
        if not sound_file:
            flash("Invalid sound file selected.", "danger")
            return redirect(url_for('user.userDashboard', username=username))

        try:
            uid = str(uuid.uuid4())
            newWebhook = Webhook(
                uid=uid,
                sound_file_id=sound_file_id,
                webhook_name=webhook_name, 
                owner=current_user.user_id
            )
            db.session.add(newWebhook)
            db.session.commit()
            flash("Webhook created successfully!", "success")
        except SQLAlchemyError:
            db.session.rollback()
            flash("Database error while creating webhook.", "danger")
    else:
        flash("Invalid webhook submission.", "danger")

    return redirect(url_for('user.userDashboard', username=username))

@user.route("/webhook/<uid>", methods=["POST"])
@csrf.exempt
def webhook(uid):
    try:
        webhook_entry = Webhook.query.filter_by(uid=uid).first()
        if not webhook_entry:
            return "Invalid webhook ID", 404

        sound_file = SoundFile.query.filter_by(sound_id=webhook_entry.sound_file_id).first()
        if not sound_file:
            return "Sound file not found", 404

        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], sound_file.filename)

        if not os.path.exists(filepath):
            return f"File not found: {filepath}", 404

        subprocess.Popen(["/usr/bin/aplay", filepath])
        return "Audio triggered!", 200

    except Exception as e:
        return f"Internal error: {str(e)}", 500

@user.route("/<username>/dashboard/sounds/")
@login_required
def userSounds(username):
    verify_user(username)
    form = SoundFileForm()
    sound_files = SoundFile.query.filter_by(owner=current_user.user_id).all()
    return render_template('user-sounds.html', username=username, form=form, sound_files=sound_files)

@user.route("/<username>/sound-file/submit/", methods=['POST'])
@login_required
def userSoundFileSubmit(username):
    verify_user(username)
    form = SoundFileForm()

    if form.validate_on_submit():
        soundName = form.soundName.data
        sound = form.soundFileInput.data
        filename = secure_filename(sound.filename)

        if not filename.lower().endswith(".wav"):
            flash("Only WAV files allowed.", "danger")
            return redirect(url_for('user.userDashboard', username=username))

        # Prevent filename collisions:
        unique_filename = f"{uuid.uuid4()}_{filename}"
        savePath = os.path.join(SOUND_FOLDER, unique_filename)
        sound.save(savePath)

        if not is_valid_wav(savePath):
            os.remove(savePath)
            flash("Invalid WAV file!", "danger")
            return redirect(url_for('user.userDashboard', username=username))

        try:
            newSound = SoundFile(
                sound_name=soundName,
                filename=unique_filename, 
                owner=current_user.user_id
            )
            db.session.add(newSound)
            db.session.commit()
            flash("Sound file uploaded successfully!", "success")
        except SQLAlchemyError:
            db.session.rollback()
            flash("Database error while saving sound file.", "danger")

    else:
        flash("Invalid sound file submission.", "danger")

    return redirect(url_for('user.userDashboard', username=username))
