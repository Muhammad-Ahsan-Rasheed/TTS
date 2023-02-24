from flask import Flask, request, jsonify, render_template, send_file
import speech_recognition as sr
import os
from gtts import gTTS


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    bot_text = ""

    # Convert user's speech to text
    if user_text.startswith('audio:'):
        audio_file = user_text[6:]
        bot_text = convert_speech_to_text(audio_file)

    # Process user's text input
    else:
        bot_text = "You said: " + user_text

    # Convert bot's text response to speech
    convert_text_to_speech(bot_text)

    return jsonify(bot_text)


def convert_speech_to_text(audio_file):
    # Load audio file
    audio = sr.AudioFile(audio_file)

    # Initialize recognizer
    r = sr.Recognizer()

    # Convert audio to text
    with audio as source:
        audio_text = r.record(source)
        text = r.recognize_google(audio_text)

    return "You said: " + text


def convert_text_to_speech(text):
    # Convert text to speech
    tts = gTTS(text=text, lang='en')

    # Save speech as mp3 file
    tts.save("response.mp3")


@app.route('/audio')
def send_audio():
    return send_file("response.mp3", mimetype='audio/mp3')


if __name__ == "__main__":
    app.run(debug=True)
