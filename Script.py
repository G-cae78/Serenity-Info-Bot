from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from .env file
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('TARGET_NUMBER')
CITY= os.getenv('CITY')
API_KEY= os.getenv('API_KEY')

print("Environment Variables:")
print(f"TWILIO_ACCOUNT_SID: {ACCOUNT_SID}")
print(f"TWILIO_AUTH_TOKEN: {AUTH_TOKEN}")
print(f"TWILIO_PHONE_NUMBER: {TWILIO_PHONE_NUMBER}")
print(f"RECIPIENT_PHONE_NUMBER: {RECIPIENT_PHONE_NUMBER}")
print(f"CITY: {CITY}")
print(f"API_KEY: {API_KEY}")


# Function to scrape weather data
def get_weather():
    API_KEY = os.getenv("API_KEY")
    CITY = os.getenv("CITY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Today's Weather: Weather: {weather}, Temperature: {round(temperature - 273.15)}C"
    else:
        print(f"Failed to get weather data. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return "Failed to get weather data"

# Function to send SMS
def send_sms(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )
    print(f"Message sent! SID: {message.sid}")

# Main bot logic
def main():
    weather_update = get_weather()
    message = f"Good morning! Today's weather is: {weather_update}"
    send_sms(message)

if __name__ == "__main__":
    main()


# # Schedule the bot to run daily at 8:00 AM
# schedule.every().day.at("08:00").do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

