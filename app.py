import speech_recognition as sr
from flask import logging, Flask, render_template, request, flash


app = Flask(__name__)
app.secret_key = "IgnasLakpa"

@app.route('/')
def index():
    flash(" Welcome to EsyLearn")
    return render_template('index.html')

@app.route('/audio_to_text/')
def audio_to_text():
    flash(" Press Start to start recording audio and press Stop to end recording audio")
    return render_template('audio_to_text.html')

@app.route('/audio', methods=['POST'])
def audio():
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)
  
    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        
        try:
            text = r.recognize_google(audio_data, language='en-IN', show_all=True)
        
        except sr.UnknownValueError:    
            print("Could not read the audio file")
        except sr.RequestError:
            print("Unknown request from the user")

        
        
    return str(return_text)


if __name__ == "__main__":
    app.run(debug=True)
