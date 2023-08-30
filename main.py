import time

import psutil
import pyautogui
from PyDictionary import PyDictionary
import pyttsx3
from bs4 import BeautifulSoup
from decouple import config
from datetime import datetime
import speech_recognition as sr
import webbrowser
import sys
from random import choice
from utils import opening_text
import requests
import subprocess
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, \
    get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_nfs, open_pycharm
from pprint import pprint

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-GH')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if 21 <= hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open need for speed' in query:
            open_nfs()

        elif 'open pycharm' in query:
            open_pycharm()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            print(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            api_key = '9bb9b456bf124f80aba6a0e09cc2f811'
            URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + api_key

            resp = requests.get(URL)
            if resp.status_code == 200:
                data = resp.json()
                news = data['articles'][0]
                speak(news['title'])
                speak(news['description'])
            else:
                speak("Cannot find a news at this moment")

        elif "current info" in query or "latest info" in query:
            url = "https://www.ghanaweb.com/GhanaHomePage/NewsArchive/"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find all the headlines on the page
            headlines = soup.find_all("h2")
            for headline in headlines[:4]:
                print(headline.text)
                speak(headline.text)

        elif 'weather' in query:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What is the name of the city?")
            city_name = take_user_input().lower()

            print(f"{city_name} whether conditions : ")

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"] - 273.15
                current_temperature = float('%.2f' % current_temperature)
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in Celsius unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidity) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in Celsius unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidity) +
                      "\n description = " +
                      str(weather_description))
            else:
                speak("Can't find details about this city")


        elif 'search flight' in query:
            speak("What is the source of the Flight Sir!!")
            source = take_user_input().lower()
            speak("What is the Destination of the Flight Sir!!")
            destination = take_user_input().lower()
            # speak("What is the Travel date sir Please speak in numeric format")
            # traveldate = takeCommand()
            # webbrowser.open(f"https://www.google.com/search?q={search_go}")
            # webbrowser.open(f"https://www.makemytrip.com/flight/search?itinerary={source}-{destination}-25/01/2023-&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E")
            webbrowser.open(
                f"https://www.makemytrip.com/flight/search?itinerary={source}-{destination}-26/01/2023&tripType=O&paxType=A-2_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng")

        elif 'shut up' in query or 'sleep' in query:
            speak('Alright Sir! Ping me up when you need me again')
            sys.exit(0)

        elif 'thank you' in query or 'appreciate' in query:
            speak("It's my duty to assist you anytime sir")

        elif "log off" in query or "sign out" in query:
            speak(
                "Ok , your pc will log off in 10 seconds! make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f'{USERNAME} our System still has {percentage} percent battery')
            if percentage >= 75:
                print("\U0001F601")
                speak(f'{USERNAME} we have enough power to continue our work!')
            elif 40 <= percentage < 75:
                speak(
                    f'{USERNAME} we should think of connecting our system to the battery supply!')
            elif 40 >= percentage >= 15:
                speak(
                    f"{USERNAME} we don't have enough power to work through!... Connect now sir!")
            elif percentage < 15:
                speak(
                    f'{USERNAME} we have very low power!... Our System may Shutdown anytime soon!...')

        elif "switch the window" in query or "switch window" in query:
            speak(f"Okay {USERNAME}, Switching the window")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")
        elif 'screenshot' in query:
            speak("Taking screenshot")
            times = time.time()
            name_img = r"{}.png".format(str(times))
            img = pyautogui.screenshot(name_img)
            speak("Done!")
            img.show()
