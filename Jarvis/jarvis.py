import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!, I am Jarvis Sir. Please tell me how can I help you?")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!, I am Jarvis Sir. Please tell me how can I help you?!")

    else:
        speak("Good Evening Sir!, I am Jarvis Sir. Please tell me how can I help you?")


def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sender@gmail.com', 'sender_password')
    server.sendmail('recievert@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif "open my github" in query:
            webbrowser.open("github.com/adityap-codes07")

        elif "open my linkedin" in query:
            webbrowser.open("www.linkedin.com/in/aditya-prakash-1a4534343/")

        elif "play paro" in query:
            music_dir = r"C:\Users\praka\Music\paro.mp3"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "what's the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open pycharm' in query:
            codePath = r"C:\Users\Public\Desktop\PyCharm 2025.2.0.1.lnk"
            os.startfile(codePath)

        elif 'email to aditya' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "bcvsproject@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend aditya bro. I am not able to send this email")