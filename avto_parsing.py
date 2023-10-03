# Import necessary libraries and modules
from telebot import TeleBot, types
import os
import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from setup import token  # Assuming setup.py contains token variable
import time

# Initialize TeleBot with the provided token
bot = TeleBot(token)

# Define the folder path to store JSON data
folder_path = 'JSON_DATA'

# Initialize dictionaries to store user data and new links
users = {}
users_new_link = []

# Define lists of new links and base URLs for OLX and Otodom
new_links = []
base_url_olx = 'https://olx.pl'
base_url_otodom = 'https://www.otodom.pl'

# Define user-agent header for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

# Function to upload user data from a JSON file
def json_upload():
    file_name = os.path.join(folder_path, 'user_data.json')
    with open(file_name, 'r') as file:
        users = json.load(file)
    return users

# Function to perform initial parsing and retrieve links for OLX and Otodom
def ferst_pars(city, min_price, max_price, r):
    numbers_r = ["one", "two", "three", "four"]
    r_otodom = numbers_r[int(r) - 1]
    link_user_a = []

    # Define URLs for OLX and Otodom based on user input
    urls = [
        f'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{city}/?search%5Bfilter_float_price:from%5D={min_price}&search%5Bfilter_float_price:to%5D={min_price}0&search%5Bfilter_enum_rooms%5D%5B0%5D={r_otodom}',
        f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie,{r_otodom}-pokoje/mazowieckie/{city}/{city}/{city}?distanceRadius=0&limit=36&priceMin={min_price}&priceMax={max_price}&by=DEFAULT&direction=DESC&viewType=listing'
    ]

    for a in range(1):
        response = requests.get(urls[a], headers=headers)
        html_code = response.text
        soup = BeautifulSoup(html_code, "html.parser")
        if a == 0:
            for a_tag in soup.find_all('a', {'class': 'css-rc5s2u'}):
                href_value = a_tag.get('href')
                if href_value.startswith('/d/'):
                    link_user_a.append(urljoin(base_url_olx, href_value))
                else:
                    link_user_a.append(href_value)

                a = 2

            for a in range(5):
                users_new_link.append(link_user_a[a])

            link_user_a = []
            response = requests.get(urls[1], headers=headers)
            html_code = response.text
            soup = BeautifulSoup(html_code, "html.parser")
            for a_tag in soup.find_all('a', {'data-cy': 'listing-item-link'}):
                href_value = a_tag.get('href')
                if href_value.startswith('/pl/'):
                    link_user_a.append(urljoin(base_url_otodom, href_value))
                else:
                    link_user_a.append(href_value)

            for a in range(5):
                users_new_link.append(link_user_a[a])

    return users_new_link

# Function to send messages to users with information about parsed results
def send_message(result_array, user_id):
    for i in range(len(result_array)):
        response = requests.get(result_array[i], headers=headers)
        html_code = response.text
        soup = BeautifulSoup(html_code, "html.parser")

        print(result_array[i])

        # Check if the URL starts with "https://www.olx.pl"
        if i > 1 and i < 5:
            price_elem = soup.find('h3', {'class': 'css-1twl9tf'})
            title_elem = soup.find('h1', {'data-cy': 'ad_title'})
            first_image_elem = soup.find('img', {'class': 'css-1bmvjcs'})

            if first_image_elem is not None:
                first_image = first_image_elem.get('src')
                if first_image is not None:
                    print(first_image)
                else:
                    print("The 'src' attribute is not present in the 'img' tag.")
            else:
                print("No 'img' tag with class 'css-1bmvjcs' was found.")

            print(price_elem)

        else:
            price_elem = soup.find('strong', {'class': 'e1l1avn10'})
            title_elem = soup.find('h1', {'data-cy': 'adPageAdTitle'})
            img_tags = soup.find_all('img')
            first_image = next((img_tag.get('src') for img_tag in img_tags if img_tag.get('src') and img_tag.get('src').startswith("https://ireland.apollo.olxcdn.com")), None)

        price_text = price_elem.get_text(strip=True) if price_elem else ''
        title_text = title_elem.get_text(strip=True) if title_elem else ''

        if price_text and title_text:
            bot.send_photo(user_id, first_image)
            bot.send_message(user_id, f"{title_text} \n\n {price_text} \n\n [link]({result_array[i]})")

# Main function to run the bot continuously
def main():
    while True:
        users = json_upload()

        outer_keys = users.keys()

        for user_key, user_value in users.items():
            urls_users = user_value['avto']
            city = user_value['city']
            min_price = user_value['price_min']
            max_price = user_value['price_max']
            r = user_value['rooms']
            print("1")
            if urls_users == 1:
                result_array = ferst_pars(city, min_price, max_price, r)

                send_message(result_array, user_key)
        time.sleep(1800)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
