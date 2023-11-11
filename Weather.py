import requests # Requests library to make HTTP requests to the Pushover API
import schedule
import time
from datetime import datetime, timedelta
import pytz #Py timezone

# Returns the lowest temperature in °F from tomorrow's date
def getWeather():

    weatherAPI_Key = 'your key here' # After creating an account, from https://home.openweathermap.org/api_keys
    city = "Charlottesville"

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weatherAPI_Key}" #The word 'forecast' here can be replaced with 'weather' for current weather. Format is somewhat different though so errors will occur for this specific code
    response = requests.get(url)
    weatherData = response.json() # Converts the JSON (JavaScript Object Notation) data into python friendly data

    weatherDescribe = 0 # =1 if you want to see all the data from openweather, =0 if you don't
    if weatherDescribe == 1:
        for key, value in weatherData.items():
            print(f"{key}: {value}")

    # Calculate the date for tomorrow
    est_timezone = pytz.timezone('US/Eastern')
    todayDateTime = datetime.now(est_timezone)
    todayDate = todayDateTime.date()

    tomorrow = todayDate + timedelta(days=1)

    # Find the lowest temperature for tomorrow
    # The forecast data is for several days at 3 hour intervals
    # This for loop finds all the data for the next day and the lowest temp_min for the 8 blocks of time
    lowTempTomorrow = None
    for entry in weatherData['list']:
        date_time = datetime.fromtimestamp(entry['dt'])
        date = date_time.date()
        print(date_time)
        if date == tomorrow:
            if lowTempTomorrow is None or entry['main']['temp_min'] < lowTempTomorrow:
                lowTempTomorrow = entry['main']['temp_min']

    if lowTempTomorrow is not None:
        # Convert from Kelvin to Fahrenheit 
        lowTempTomorrow = (lowTempTomorrow - 273.15) * 9/5 + 32
        lowTempTomorrow =  round(lowTempTomorrow, 1) # Round to 1 decimal place

        # print('Low tonight is ' + str(lowTempTomorrow) + '°F')
    else:
        print("No data available for tomorrow's low temperature.")

    return lowTempTomorrow

# This function sends a notification to my phone with the lowTempData from Openweather using the Pushover.net app
def pushoverApp_SendNotification(lowTempTomorrow):
    pushoverToken = 'your token here' # Create a blank application within Pushover.net, and the key associated with this one is what you input here 
    pushoverKey = 'your key here' # Key associated with account, 1 per account, on the main page of https://pushover.net/

    # Setting the message and other parameters
    message = 'Low tonight is ' + str(lowTempTomorrow) + '°F'
    title = 'Freezing Tonight'
    priority = 0  # Priority can be -2, -1, 0, 1, or 2 (0 is the default)
    sound = 'pushover'  # You can change the sound for the notification

    # Pushover API endpoint
    url = 'https://api.pushover.net/1/messages.json'

    # Create a dictionary with the notification data
    data = {
        'token': pushoverToken,
        'user': pushoverKey,
        'message': message,
        'title': title,
        'priority': priority,
        'sound': sound
    }

    # Send the Post request from requests library to Pushover API
    response = requests.post(url, data=data) 

    # Uncomment these lines if you want to report whether the notification was sent sucessfully or not
    
    # if response.status_code == 200:
    #     print('Notification sent successfully!')
    # else:
    #     print(f'Failed to send notification. Status Code: {response.status_code}')
    #     print(response.text)

def checkAndNotify():
    print('Code executed')
    lowTonight = getWeather()
    if lowTonight < 32: #Enter <100 here if you want to see if code is working on days that aren't below freezing the next day
        pushoverApp_SendNotification(lowTonight)
        
# Schedule the script to run at every day
# Anaconda.cloud is running at UTC timezone. I want this to run at 4pm EST -> 9pm UTC

# checkAndNotify() #If you want to just test the code in real time, uncomment this line, and comment out the following lines

schedule.every().day.at("21:00").do(checkAndNotify)  # Schedule the getWeather function
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute