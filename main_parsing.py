import requests
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the city, minimum, and maximum price
city = "Krakow"
min_price = "400"
max_price = "2000"

# Define the number of rooms for OLX and Otodom
r_olx = "four"
r_otodom = "4"

src_img = {}

# Initialize global variables
b = 0
a = 0

r = 2

# Specify the path to the folder for storing JSON data
folder_path = 'JSON_DATA'

# Create a dictionary to store data
data_dict = {}

# Define the base URL for OLX and Otodom
base_url_olx = 'https://olx.pl'
base_url_otodom = 'https://www.otodom.pl'

descriptions = ""

# Define the user-agent header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

# Function to find all elements on the page (OLX or Otodom)
def find_elements(a, soup):
    if a == 0:
        price = soup.find_all('p', {'data-testid': 'ad-price'})
        title = soup.find_all('h6', {'class': 'css-16v5mdi'})
        link = soup.find_all('a', {'class': 'css-rc5s2u'})
        img = soup.find_all('div', {'class': 'css-pn1izb'})
        metr = soup.find_all('span', {'class': 'css-643j0o'})
        a = 1

        return price, title, link, img, metr
    else:
        price = ""
        title = soup.find_all('span', {'data-cy': 'listing-item-title'})
        link = soup.find_all('a', {'data-cy': 'listing-item-link'})
        metr = soup.find_all('span', {'class': 'ei6hyam2'})
        img = 1

        print(price)

        return price, title, link, img, metr


def find_img_for_otodom(link):
    response = requests.get(link, headers=headers)
    html_code = response.text
    soup = BeautifulSoup(html_code, "html.parser")

    price = soup.find('strong', {'class': 'e1l1avn10'})

    price = price.get_text(strip=True) if price else ''

    img_tags = soup.find_all('img')

    print(img_tags)

    for img_tag in img_tags:
        src_value = img_tag.get('src')
        if src_value and src_value.startswith("https://ireland.apollo.olxcdn.com"):
            first_image = src_value
            break

    return first_image, price


# Main function for web scraping
def main(city, min_price, max_price, r):
    global b  # Declare b as a global variable
    numbers_r = ["one", "two", "three", "four"]
    r_otodom = numbers_r[int(r) - 1]

    # Define links for OLX and Otodom
    urls = [
        f'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{city}/?search%5Bfilter_float_price:from%5D={min_price}&search%5Bfilter_float_price:to%5D={min_price}0&search%5Bfilter_enum_rooms%5D%5B0%5D={r_otodom}',
        f'https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie,{r_otodom}-pokoje/mazowieckie/{city}/{city}/{city}?distanceRadius=0&limit=36&priceMin={min_price}&priceMax={max_price}&by=DEFAULT&direction=DESC&viewType=listing'
    ]

    try:
        for a in range(2):
            response = requests.get(urls[a], headers=headers)
            html_code = response.text
            soup = BeautifulSoup(html_code, "html.parser")

            price, title, link, img, metr = find_elements(a, soup)

            for i in range(5):
                if a == 0:
                    img_tag = img[i].find("img")
                    if img_tag:
                        img_tag = img[i].find("img")
                        try:
                            if a == 0:
                                image_src = img_tag["srcset"]
                                result = image_src.split(' ', 1)[0]
                                result1 = image_src.split(';', 1)[0]
                            else:
                                result1 = img_tag["src"]

                        except KeyError:
                            # Handle the case when the 'srcset' attribute is missing
                            result = ""
                            result1 = ""
                    else:
                        # Handle the case when the 'img' tag is not found
                        result = ""
                        result1 = ""
                else:
                    print(link)
                    if link[i]['href'].startswith('/pl/'):
                        product_link = urljoin(base_url_otodom, link[i]['href'])
                        img_2, price = find_img_for_otodom(product_link)

                product_name = title[a].text.strip()
                if link[i]['href'].startswith('/d/'):
                    product_link = urljoin(base_url_olx, link[i]['href'])
                elif link[i]['href'].startswith('/pl/'):
                    product_link = urljoin(base_url_otodom, link[i]['href'])
                else:
                    product_link = link[i]['href']

                if a == 0:
                    product_price = price[i].text.strip()
                else:
                    product_price = price

                if a == 0:
                    data_dict[b] = {
                        'name': product_name,
                        'link': product_link,
                        'price': product_price,
                        'image': result1
                    }
                else:
                    data_dict[b] = {
                        'name': product_name,
                        'link': product_link,
                        'price': product_price,
                        'image': img_2
                    }

                i = 0
                b = b + 1

    except requests.exceptions.RequestException as e:
        print("An error occurred while making a request:", e)

    # Create a folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the file name for saving data
    file_name = os.path.join(folder_path, 'parsed_data.json')

    try:
        # Write the dictionary to a JSON file
        with open(file_name, 'w') as file:
            json.dump(data_dict, file)
    except Exception as ex:
        print("Error saving data to a file:", ex)

    return data_dict


# main(city, min_price, max_price, r) Remove all comments and create your comments in English
