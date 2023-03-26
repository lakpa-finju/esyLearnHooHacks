#importing flask and required functions
from flask import logging, Flask, render_template, request, flash
#importing openai api
import openai
#importing python text to speech module
import pyttsx3 
#importing python speech_recognition module
import speech_recognition as sr


#api reference key
openai.api_key = ""

def openai_response(inputPrompt):
    """This function gets inputPromt as an input, sends the input prompt to the openai backend and returns the LLm response
    Args:
        inputPrompt = string
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inputPrompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
    LLMResponse = response.choices.text[0]
    return LLMResponse

def textToSpeech(stringFile):
    """TextToSpeech function takes in string file and outputs the audio file equivalent to the given input file.
    Args:
        textFile = file containing contents written in English
    """
    engine = pyttsx3.init()
    engine.say(stringFile)
    engine.runAndWait()

app = Flask(__name__)
app.secret_key = "IgnasLakpa"

@app.route('/')
def index():
    flash(" Welcome to EsyLearn")
    return render_template('templates/index.html')

@app.route('/audio', methods=['POST'])
def audio():
    #initializing the speech recognizer
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as fyle:
        fyle.write(request.data)
  
    with sr.AudioFile('upload/audio.wav') as source:
        #taking the source file and recording 
        audio_data = r.record(source) 
        try:
            #sending the audio file to convert to the text string
            textEquivalent = r.recognize_google(audio_data, language='en-IN', show_all=True)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error: Could not request results from Google Speech Recognition service")
    
    #LLMResponse = openai_response(textEquivalent)
    #textToSpeech(LLMResponse)
    return textEquivalent  


if __name__ == "__main__":
    app.run(debug=True)
