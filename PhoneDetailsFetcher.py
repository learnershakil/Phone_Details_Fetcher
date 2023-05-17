import phonenumbers
import requests
from bs4 import BeautifulSoup
from tkinter import *

def fetch_details():
    # get phone number from input field
    phone_number = phone_number_input.get()

    # validate phone number
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            result_text.delete('1.0', END)
            result_text.insert(END, "Invalid phone number.")
            return
    except phonenumbers.phonenumberutil.NumberParseException:
        result_text.delete('1.0', END)
        result_text.insert(END, "Invalid phone number.")
        return

    # fetch carrier details
    url = f'https://www.carrierlookup.com/index.php/api/lookup?api_key=YOUR_API_KEY&number={phone_number}'
    response = requests.get(url)
    carrier_details = response.json()

    # fetch location details
    url = f'https://www.numberlookup.com/{phone_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    location_details = soup.find_all('div', {'class': 'detail-row'})[0].find('p').text

    # fetch social media profiles
    # replace the following code with your actual implementation to fetch social media profiles
    social_media_profiles = [
        {
            'name': 'John Doe',
            'platform': 'Twitter',
            'link': 'https://twitter.com/johndoe'
        },
        {
            'name': 'John Doe',
            'platform': 'Facebook',
            'link': 'https://facebook.com/johndoe'
        },
        {
            'name': 'John Doe',
            'platform': 'Instagram',
            'link': 'https://instagram.com/johndoe'
        }
    ]

    # display the results
    result_text.delete('1.0', END)
    result_text.insert(END, f"Phone number: {phone_number}\n\n")
    result_text.insert(END, f"Carrier: {carrier_details['carrier']}\n")
    result_text.insert(END, f"Line type: {carrier_details['linetype']}\n\n")
    result_text.insert(END, f"Location: {location_details}\n\n")
    result_text.insert(END, "Social media profiles:\n")
    for profile in social_media_profiles:
        result_text.insert(END, f"{profile['name']} - {profile['platform']}: {profile['link']}\n")
