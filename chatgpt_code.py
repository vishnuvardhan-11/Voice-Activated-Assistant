import speech_recognition as sr  # type: ignore
import pyttsx3  # type: ignore
import pywhatkit  # type: ignore
import wikipedia  # type: ignore
from datetime import datetime
import pyjokes  # type: ignore
import requests  # type: ignore
import webbrowser  # type: ignore
from googlesearch import search  # type: ignore

def talk(answer):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(answer)
    engine.runAndWait()

def processQuestion(question):
    question = question.lower()  # Convert the question to lower case for uniformity
    if "what are you doing" in question:
        print("I am waiting for your queries.")
        talk("I am waiting for your queries.")
        return True
    elif "how are you" in question:
        print("I am good, what about you? And thanks for asking.")
        talk("I am good, what about you? And thanks for asking.")
        return True
    elif "play" in question:
        question = question.replace("play", "")
        pywhatkit.playonyt(question)
        return True
    elif "who is" in question or "about" in question:
        question = question.replace("who is", "").replace("about", "")
        try:
            summary = wikipedia.summary(question, sentences=1)
            print(summary)
            talk(summary)
        except wikipedia.exceptions.PageError:
            print("Sorry, I could not find any information on that topic.")
            talk("Sorry, I could not find any information on that topic.")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"That query is too ambiguous. Did you mean one of these: {e.options}")
            talk(f"That query is too ambiguous. Did you mean one of these: {e.options}")
        return True
    elif "time" in question:
        current_time = datetime.now().strftime("%I:%M %p")
        date = datetime.now().strftime("%Y-%m-%d")
        day = datetime.now().strftime("%A")
        print(f"Current time: {current_time}")
        print(f"Current date: {date}")
        print(f"Day: {day}")
        talk(f"Current time is {current_time}")
        talk(f"Today's date is {date}")
        talk(f"And it's {day} today.")
        return True
    elif "funny jokes" in question or "tell me a joke" in question:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
        return True
    elif "love you" in question:
        talk("Sorry, I have a boyfriend. His name is Vishnu.")
        return True
    elif "weather" in question:
        api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = "your_city"  # Replace with the desired city
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        weather_data = response.json()
        if weather_data["cod"] != "404":
            main = weather_data.get("main", {})
            weather = weather_data.get("weather", [{}])[0]
            temp = main.get("temp")
            description = weather.get("description", "no description available")
            if temp:
                weather_report = f"The temperature is {temp - 273.15:.2f} degrees Celsius with {description}."
            else:
                weather_report = "Sorry, I couldn't get the temperature information."
            print(weather_report)
            talk(weather_report)
        else:
            talk("City not found.")
        return True
    elif "search for" in question:
        query = question.replace("search for", "").strip()
        for url in search(query, num_results=1):
            print(f"Opening {url}")
            talk(f"Opening {url}")
            webbrowser.open(url)
        return True
    elif "bye" in question or "goodnight" in question:
        talk("Okay, bye. Please take care. We will meet again later.")
        return False
    else:
        print("Sorry, I didn't recognize your query. Thanks for asking.")
        talk("Sorry, I didn't recognize your query. Thanks for asking.")
        return True

def getQuestion():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please ask your question.")
        talk("Please ask your question.")
        audio = r.listen(source)
    try:
        question = r.recognize_google(audio)
        print(f"You said: {question}")
        if "alexa" in question.lower():
            question = question.replace("Alexa", "").strip()
            return question
        else:
            print("Sorry, I'm unable to detect your query.")
            talk("Sorry, I'm unable to detect your query.")
            return "i am unable get your queries"
    except sr.UnknownValueError:
        print("Sorry, I can't get your question.")
        talk("Sorry, I can't get your question.")
        return "i am unable get your queries"

canAskQuestion = True
while canAskQuestion:
    question = getQuestion()
    if question == "i am unable get your queries":
        talk("If you have any queries, please feel free to ask me.")
        canAskQuestion = False
    else:
        canAskQuestion = processQuestion(question)
