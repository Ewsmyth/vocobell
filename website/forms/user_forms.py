from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class FirstLoginForm(FlaskForm):
    changeFirstLogin = SubmitField('Finish')

class SoundFileForm(FlaskForm):
    soundName = StringField('Sound Name', validators=[DataRequired()])
    soundFileInput = FileField('Select .wav file.', validators=[
        FileRequired(),
        FileAllowed(['wav'], 'Only WAV files are allowed!')
    ])
    submitSoundFile = SubmitField('Upload')

class CreateWebhookForm(FlaskForm):
    webhookName = StringField('Webhook Name', validators=[DataRequired()])
    soundFileSelect = SelectField('Select Sound File', choices=[], coerce=int)
    submit = SubmitField('Create Webhook')
