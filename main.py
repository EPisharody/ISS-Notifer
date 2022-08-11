import requests
import datetime as dt
from tkinter import *

# Constants
API_KEY = "81af52dacf4f8979cc374e1588467cce"
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"

# Function gets coordinates and country (latitude and longtitude) of the city entered in the text box
def get_coordinates():
    parameters = {
        "q":city_entry.get(),
        "appid":API_KEY
    }

    geocode_response = requests.get(url=GEOCODE_ENDPOINT, params=parameters)
    geocode_response.raise_for_status()

    data = geocode_response.json()

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    country = data[0]["country"]

    return lat, lon, country

# Function determines if the ISS is currently over the city input by the user
def is_iss_overhead():
    response = requests.get(url=ISS_ENDPOINT)
    response.raise_for_status()

    data = response.json()

    lat, lon, country = get_coordinates()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    city = city_entry.get().title()
    
    # If the ISS is above the inputted city, show the appropriate message
    if (lat-5 <= iss_latitude <= lat+5) and (lon-5 <= iss_longitude <= lon+5):
        
        result.config(text=f"The ISS is currently above {city}!", bg="#213b4a") # display the message
        
        # Modify the GUI elements
        city_label.config(text=f"City: {city}, {country}", font=("arial", 24),bg="#213b4a")
        city_label.grid(column=0, row=1, columnspan=2)
        label2.config(text="Change city: ",bg="#213b4a")
        label2.grid(column=0, row=3, padx=(0, 250), pady=(200, 0))
        city_entry.config(font=("arial", 12))
        city_entry.grid(column=1, row=3, padx=(70, 25), pady=(200, 0))
        button1.grid(column=1, row=3, padx=(320, 0), pady=(200, 0))
        window.config(bg="#213b4a")
        label1.config(bg="#213b4a")

    else:
        result.config(text=f"The ISS is currently not above {city}", font=("arial", 16),bg="#64b4e3") # display the message

        # Modify the GUI elements
        city_label.config(text=f"City: {city}, {country}", font=("arial", 24),bg="#64b4e3")
        city_label.grid(column=0, row=1, columnspan=2)
        label2.config(text="Change city: ",bg="#64b4e3")
        label2.grid(column=0, row=3, padx=(0, 250), pady=(200, 0))
        city_entry.config(font=("arial", 12))
        city_entry.grid(column=1, row=3, padx=(70, 25), pady=(200, 0))
        button1.grid(column=1, row=3, padx=(320, 0), pady=(200, 0))
        window.config(bg="#64b4e3")
        label1.config(bg="#64b4e3")

    result.grid(row=3, column=1, columnspan=2, pady=(0, 150), padx=(0, 80))

# GUI Elements
window = Tk()
window.title("ISS Notifier")
window.minsize(width=700, height=350)
window.config(padx=100)

label1 = Label(text="International Space Station Notifier", font=("arial", 24, "bold"))
label1.grid(column=0, row=0, columnspan=2)

label2 = Label(text="Enter your city:", font=("arial", 16))
label2.grid(column=0, row=1, columnspan=2, pady=(70, 15))

city_entry = Entry(width=25)
city_entry.grid(column=0, row=2, columnspan=2)

button1 = Button(text="Go", command=is_iss_overhead)
button1.grid(column=1, row=2, padx=50)
result = Label()
city_label = Label()


window.mainloop()