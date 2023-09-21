import requests
from bs4 import BeautifulSoup

url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/#680671531"  # Замените это на URL вашего сайта
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_code = response.text
        # Используйте BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html_code, "html.parser")
        
        # Найти все элементы
        p_elements = soup.find_all('p', {'data-testid': 'ad-price'})
        h6_elements = soup.find_all('h6', {'class': 'css-16v5mdi'})
        a_elements = soup.find_all('a', {'class': 'css-rc5s2u'})
        img_elements = soup.find_all('img', {'class': 'css-8wsg1m'} or {'class': 'css-gwhqbt'})
        
        # Создать словарь для хранения данных
        data_dict = {}
        
        # Заполнить словарь данными
        for i in range(len(h6_elements)):
            product_name = h6_elements[i].text.strip()
            product_link = a_elements[i]['href']
            product_price = p_elements[i].text.strip()
            product_image = img_elements[i]['src']
            data_dict[product_name] = {
                'link': product_link,
                'price': product_price,
                'image': product_image
            }
        
        # Вывести содержимое словаря
        for product_name, product_data in data_dict.items():
            print(f"Изделие: {product_name}")
            print(f"Ссылка: {product_data['link']}")
            print(f"Цена: {product_data['price']}")
            print(f"Фотография: {product_data['image']}\n")
    else:
        print("Ошибка при запросе:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Произошла ошибка при выполнении запроса:", e)
