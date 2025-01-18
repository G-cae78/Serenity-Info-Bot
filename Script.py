from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from .env file
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

# Function to scrape weather data
def get_weather():
    driver = webdriver.Chrome()  # Make sure to set the correct path to chromedriver if needed
    driver.get("https://www.weather.com/")  # Change URL if needed

    try:
        # Wait for the weather element to be visible before accessing it
        weather_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "CurrentConditions--tempValue--3KcTQ"))
        )
        weather = weather_element.text
    except Exception as e:
        print(f"Error finding weather element: {e}")
        weather = "Could not retrieve weather"

    driver.quit()
    return weather

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

