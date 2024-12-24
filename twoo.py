import pyttsx3  
import speech_recognition as sr  
import datetime
import wikipedia  
import webbrowser
import os
import smtplib
import pywhatkit as kit  
import pyautogui 
import time
import random  
import requests 
import psutil
import platform
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
# from googletrans import Translator

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
    
    # Function to fetch and speak news headlines
def getNews():
    api_key = "15c83b7ade6c4d07b9a19e0d71e2d097"  # Replace with your NewsAPI key
    base_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + api_key
    response = requests.get(base_url)
    news_data = response.json()
    
    if news_data["status"] == "ok":
        articles = news_data["articles"]
        speak("Here are the top news headlines.")
        for i, article in enumerate(articles[:5], 1):  # Fetch top 5 headlines
            speak(f"Headline {i}: {article['title']}")
            print(f"Headline {i}: {article['title']}")
    else:
        speak("I couldn't fetch the news at the moment. Please try again later.")

expenses = []

def addExpense():
    speak("What is the expense for?")
    category = takeCommand()
    speak("How much is the amount?")
    amount = takeCommand()
    
    if amount.isdigit():
        expenses.append({"category": category, "amount": int(amount)})
        speak(f"Added {amount} to {category}.")
    else:
        speak("Invalid amount. Please try again.")

def viewExpenses():
    if expenses:
        total = sum(expense['amount'] for expense in expenses)
        speak(f"Here is the breakdown of your expenses:")
        for expense in expenses:
            speak(f"{expense['category']}: {expense['amount']} dollars")
        speak(f"Total expenses: {total} dollars")
    else:
        speak("No expenses recorded yet.")
  
def rollDice():
    result = random.randint(1, 6)
    speak(f"The dice rolled a {result}.")

def readPDF(file_path):
    try:
        with open(file_path, 'rb') as file:  # Open the PDF in binary read mode
            reader = PyPDF2.PdfReader(file)  # Initialize the PDF Reader
            text = ''
            # Extract text from all pages
            for page in reader.pages:
                text += page.extract_text()
            
            # Speak and display a snippet of the content
            if text:
                speak("Here is the content of the PDF.")
                print(text[:500])  # Display the first 500 characters
                speak(text[:500])  # Read aloud the first 500 characters
            else:
                speak("Sorry, I couldn't extract any text from the PDF.")
    except Exception as e:
        speak("An error occurred while reading the PDF.")
        print(e)


def create_text_pdf(file_path, text):
    """
    Create a PDF file with the given text.
    
    Parameters:
    file_path (str): The path where the PDF will be saved.
    text (str): The text content to be included in the PDF.
    """
    c = canvas.Canvas(file_path, pagesize=letter)  # Create a PDF canvas
    c.setFont("Helvetica", 12)  # Set the font to Helvetica, size 12

    # Set the starting position for the text (x, y)
    x = 50
    y = 750  # Starting near the top of the page

    # Split text into lines and write them to the PDF
    lines = text.split('\n')  # Split text into multiple lines
    for line in lines:
        c.drawString(x, y, line)  # Add the line to the PDF at position (x, y)
        y -= 14  # Move down for the next line (14 pixels down per line)
    
    c.save()  # Save the PDF file
    print(f"PDF created at: {file_path}")


def setAlarm():
    speak("Please specify the time for the alarm in HH:MM format.")
    alarm_time = takeCommand()
    speak(f"Setting alarm for {alarm_time}.")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Time to wake up!")
            break
        time.sleep(10)  # Check every 10 seconds
        
def batteryStatus():
    battery = psutil.sensors_battery()
    if battery:
        percentage = battery.percent
        speak(f"Battery is at {percentage} percent.")
        if battery.power_plugged:
            speak("The system is plugged in.")
        else:
            speak("The system is running on battery.")
    else:
        speak("Sorry, I couldn't retrieve the battery status.")


# Wishing function
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")
    speak("I meraaki!, your assistant. How can I assist you today?")       

# Function to take commands from the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

# Email sending function
def sendEmail():
    speak("What should I say?")
    mc = takeCommand().lower()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('utkarshwaliaa@gmail.com', 'Bennettgmail2024')  # Replace with your credentials
        server.sendmail('utkarshwaliaa@gmail.com', 'utkarshhwalia@gmail.com', mc)  # Replace with appropriate addresses
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("I am not able to send this email right now.")

# Function to check the weather
def getWeather(city):
    api_key = "7c91fcb7cfdfd4fb2586406ca9a64214"  # Obtain this from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        wind = data["wind"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        wind_speed = wind["speed"]
        
        speak(f"Weather in {city}:")
        speak(f"Description: {weather_desc}")
        speak(f"Temperature: {temp} degrees Celsius")
        speak(f"Humidity: {humidity}%")
        speak(f"Wind Speed: {wind_speed} meter per second")
    else:
        speak(f"City {city} not found!")

# Tell a joke function
def tellJoke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't programmers like nature? It has too many bugs."
    ]
    joke = random.choice(jokes)
    speak(joke)

# Random song from a predefined list
def playRandomSong():
    songs = ["Shape of You by Ed Sheeran", "Blinding Lights by The Weeknd", "Happier by Marshmello"]
    song = random.choice(songs)
    speak(f"Playing {song}")
    kit.playonyt(song)

# Show today's date
def showDate():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {today}")

# Open Twitter
def openTwitter():
    speak("Opening Twitter")
    webbrowser.open("https://twitter.com/")

# Take a Screenshot
def takeScreenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png")
def findMyIP():
    try:
        ip = requests.get('https://api64.ipify.org?format=json').json()["ip"]
        speak(f"Your IP address is {ip}.")
    except Exception as e:
        speak("Sorry, I couldn't fetch your IP address at the moment.")
        
def takeNotes():
    speak("What would you like me to write down?")
    notes = takeCommand()
    if notes != "None":
        file_path = "notes.txt"
        with open(file_path, 'a') as f:
            f.write(f"{datetime.datetime.now()}: {notes}\n")
        speak("Note saved.")
    else:
        speak("I couldn't catch that. Please try again.")


# Initialize the board
board = [' '] * 9  # 9 spaces representing the 3x3 grid

# Function to display the board
def displayBoard():
    print(f"""
     {board[0]} | {board[1]} | {board[2]}
    ---+---+---
     {board[3]} | {board[4]} | {board[5]}
    ---+---+---
     {board[6]} | {board[7]} | {board[8]}
    """)
def playerMove(player):
    while True:
        try:
            pos = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if pos < 0 or pos > 8 or board[pos] != ' ':
                print("Invalid move. Try again.")
            else:
                board[pos] = player
                break
        except ValueError:
            print("Please enter a valid number.")
def checkWin(player):
    # All possible win conditions
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False
def checkTie():
    return all(pos != ' ' for pos in board)
def ticTacToe():
    print("Welcome to Tic-Tac-Toe!")
    displayBoard()

    # Start with Player X
    current_player = 'X'

    for turn in range(9):  # Maximum of 9 moves
        playerMove(current_player)
        displayBoard()

        # Check for a win
        if checkWin(current_player):
            print(f"Player {current_player} wins!")
            break

        # Check for a tie
        if checkTie():
            print("It's a tie!")
            break

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'

# Main assistant loop
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # YouTube search
        elif 'search on youtube' in query:
            speak("What should I search on YouTube?")
            cm = takeCommand().lower()
            kit.playonyt(f"{cm}")

        # Open YouTube
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        # Open Chrome
        elif 'open chrome' in query:
            speak("Opening Chrome")
            codePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(codePath)

        # Search Google
        elif 'search on google' in query:
            speak("What should I search on Google?")
            cm = takeCommand().lower()
            kit.search(f"{cm}")

        # Open Google
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        # Open Facebook
        elif 'open facebook' in query:
            speak("Opening Facebook")
            webbrowser.open("https://facebook.com")

        # Play music
        elif 'play music' in query:
            speak("What song would you like to listen to?")
            cm = takeCommand().lower()
            kit.playonyt(f"{cm}")

        # Current time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # Tell a joke
        elif 'tell me a joke' in query:
            tellJoke()

        # Weather info
        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = takeCommand().lower()
            getWeather(city)

        # Date info
        elif 'date' in query:
            showDate()

        # Open Twitter
        elif 'open twitter' in query:
            openTwitter()

        # Take Screenshot
        elif 'take screenshot' in query:
            takeScreenshot()

        # Random song
        elif 'play  random song' in query:
            playRandomSong()

        # Shutdown the system
        elif 'shut down the system' in query:
            speak("Shutting down the system in 5 seconds")
            os.system("shutdown /s /t 5")

        # Restart the system
        elif 'restart the system' in query:
            speak("Restarting the system in 5 seconds")
            os.system("shutdown /r /t 5")

        # Exit assistant
        elif 'exit' in query:
            speak("Goodbye! Have a nice day!")
            break
        
        elif 'open instagram' in query:
            speak("Opening Instagram sir")
            webbrowser.open("https://www.instagram.com/")
            
       
        elif 'open gmail' in query:
            speak("Opening Gmail sir")
            webbrowser.open("https://mail.google.com/")
            
        elif 'open linkedin' in query:
            speak("Opening LinkedIn sir")
            webbrowser.open("https://www.linkedin.com/")
        elif 'check system specs' in query:
            speak("Checking system specs sir")
            specs = get_system() # type: ignore
            speak(specs)
            print(specs)
            
        # Open any website by name
        elif '.com' in query:
            website = query.replace('open ', '').strip()  # Remove 'open' and extra spaces
            if not website.startswith("http"):
                website = f"http://{website}"  # Ensure proper URL format
            speak(f"Opening {website}")
            webbrowser.open(website)

    
        # News headlines
        elif 'email' in query:
            sendEmail()

        # Greeting responses
        elif 'hello' in query:
            speak("Hello! How can I assist you today?")
        
        elif 'good morning' in query:
            speak("Good morning! Wishing you a great day ahead!")
        
        elif 'good afternoon' in query:
            speak("Good afternoon! Hope you're having a wonderful day!")
        
        elif 'good evening' in query:
            speak("Good evening! How can I assist you this evening?")
        
        elif 'thank you' in query:
            speak("You're welcome! Always happy to help.")
        
        elif 'how are you' in query:
            speak("I'm just a program, but I'm here and ready to assist you!")
        elif 'roll a dice' in query:
            rollDice()
        elif 'read pdf' in query:
            speak("Please type the full path of the PDF file.")
            file_path = input("Enter the full path of the PDF file: ")  # Take input manually
            if os.path.exists(file_path):
                readPDF(file_path)
            else:
                speak("The provided path does not exist. Please check and try again.")
                
        elif 'create pdf' in query:
            speak("Please say the text you want to include in the PDF.")
            text = takeCommand()  # Take the text input from the user (using speech recognition)
    
            if text != "None":
                speak("Please specify the path where you want to save the PDF.")
                file_path = input("Enter the path where you want to save the PDF (e.g., C:\\Users\\YourName\\Documents\\example.pdf): ")
        
            if file_path:
                create_text_pdf(file_path, text)  # Call the create_text_pdf function to generate the PDF
                speak(f"PDF created and saved at {file_path}")
            else:
                speak("You didn't specify a valid path.")
        elif 'set an alarm' in query:
            setAlarm()
        elif 'battery status' in query:
            batteryStatus()

        elif 'find my ip' in query:
            findMyIP()
        elif 'take notes' in query:
            takeNotes()
        
        elif 'add expense' in query:
            addExpense()
        elif 'view expenses' in query:
            viewExpenses()
        # if __name__ == "__main__":
        #     ticTacToe()
            # Main assistant loop addition
        elif 'play tic' in query:
            speak("Starting Tic-Tac-Toe. Player X will go first.")
            ticTacToe()

# thanku