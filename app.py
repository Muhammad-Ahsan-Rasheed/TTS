from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import openai
import markdown


app = Flask(__name__)

# Replace YOUR_API_KEY with your actual API key for the OpenAI GPT-3 API
openai.api_key = 'YOUR_API_KEY'

# Home page
@app.route('/')
def home():
    return render_template('home.html')


# Endpoint for text-based chat
@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the form
    message = request.form['message']

    # Send the message to the ChatGPT API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.9,
    )

    response_text = response['choices'][0]['text']
    markdown_text = markdown.markdown(response_text)
    # Return the response to the user
    return markdown_text


# Endpoint for voice-based chat
@app.route('/voice', methods=['POST'])
def audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=10, phrase_time_limit=20)
    # save audio file
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())
    try:
        text = r.recognize_google(audio, language='en-US', show_all=False)
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)

    # Send the text message to the ChatGPT API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.9,
    )

    response_text = response['choices'][0]['text']

    # Return the response to the user
    return response_text


if __name__ == '__main__':
    app.run(debug=True)
