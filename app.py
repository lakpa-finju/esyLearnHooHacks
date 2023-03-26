#importing python speech_recognition module
import speech_recognition as sr
#importing flask and required functions
from flask import logging, Flask, render_template, request, flash
#importing openai api
import openai
#importing python text to speech module
import pyttsx3 

app = Flask(__name__)
app.secret_key = "LakpaIgnas"

#open AI reference Key
openai.api_key ="" 
def openai_response(inputPrompt):
    """This function gets inputPromt as an input, sends the input prompt to the openai backend and returns the LLm response
    Args:
        inputPrompt = string
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inputPrompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
    LLMResponse = response.choices[0].text
    return LLMResponse


def textToSpeech(stringFile):
    """TextToSpeech function takes in string file and outputs the audio file equivalent to the given input file.
    Args:
        textFile = file containing contents written in English
    """
    engine = pyttsx3.init()
    voice = engine.getProperty('voice')
    engine.setProperty('voice', voice[1])
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 110)
    engine.say(stringFile)
    engine.runAndWait()

@app.route('/')
def index():
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
            text = r.recognize_google(audio_data, language='en-IN',show_all=False)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error: Could not request results from Google Speech Recognition service")
    LLMResponse = openai_response(text)
    textToSpeech(LLMResponse)
    return str(text+'\n'+LLMResponse)


if __name__ == "__main__":
    app.run(debug=True)
