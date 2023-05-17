import tkinter as tk
import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup
import json

# Fetch phone number details using Truecaller API
def fetch_truecaller_details(phone_number):
    url = "https://www.truecaller.com/search/in/" + phone_number
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script", type="text/javascript")
        for script in scripts:
            if "app\.config" in script.text:
                data = script.text.split("window\.app\.config = ")[1].rsplit(";", 1)[0]
                json_data = json.loads(data)
                return json_data.get("data", {})
    
    return {}

# Fetch phone number details using phonenumbers library
def fetch_phone_details(phone_number):
    details = {}

    try:
        parsed_number = phonenumbers.parse(phone_number, "IN")
        
        if phonenumbers.is_valid_number(parsed_number):
            details["country_code"] = phonenumbers.region_code_for_number(parsed_number)
            details["location"] = geocoder.description_for_number(parsed_number, "en")
            details["carrier"] = carrier.name_for_number(parsed_number, "en")
        else:
            details["error"] = "Invalid phone number."
    
    except phonenumbers.phonenumberutil.NumberParseException as e:
        details["error"] = str(e)
    
    return details

def track_location():
    phone_number = phone_entry.get()

    truecaller_details = fetch_truecaller_details(phone_number)
    phone_details = fetch_phone_details(phone_number)

    location = truecaller_details.get('location') or phone_details.get('location')
    location_label.config(text="Current Location: " + location)

def fetch_social_media_profiles():
    phone_number = phone_entry.get()

    # Implement social media profile fetching here
    # Use appropriate APIs or techniques to retrieve social media profiles based on the phone number
    # Extract relevant information such as names, usernames, profile pictures, etc.
    # Display the profiles in the result_text box

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Social Media Profiles:\n")
    result_text.insert(tk.END, "Profile 1\n")
    result_text.insert(tk.END, "Profile 2\n")
    result_text.insert(tk.END, "Profile 3\n")
    # Add more profiles as needed

# GUI Setup
window = tk.Tk()
window.title("Phone Number Details")
window.geometry("400x400")

phone_label = tk.Label(window, text="Enter Phone Number:")
phone_label.pack()

phone_entry = tk.Entry(window)
phone_entry.pack()

fetch_button = tk.Button(window, text="Fetch Details", command=track_location)
fetch_button.pack()

social_media_button = tk.Button(window, text="Fetch Social Media Profiles", command=fetch_social_media_profiles)
social_media_button.pack()

result_text = tk.Text(window, height=10, width=40)
result_text.pack()

location_label = tk.Label(window, text="Current Location: ")
location_label.pack()

window.mainloop()
