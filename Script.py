from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import schedule
import time



import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN= os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_NUMBER= os.getenv("TWILIO_NUMBER")
TARGET_NUMBER= os.getenv("TARGET_NUMBER")

def get_weather():
    api_key = os.getenv("API_KEY")  # Replace with your actual API key
    city = os.getenv("CITY")  # Replace with your city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Today's Weather: Weather: {weather}, Temperature: {round(temperature-273.15)}C"
    else:
        print(f"Failed to get weather data. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return "Failed to get weather data"

def send_info(message):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=TARGET_NUMBER
        )
        print(f"Message sent! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def main():
    weather_update = get_weather()
    message = f"Good morning Mate! Let's get it Today's weather is: {weather_update}"
    send_info(message)

if __name__ == "__main__":
    main()

# Schedule the bot to run daily at 8:00 AM
schedule.every().day.at("08:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

