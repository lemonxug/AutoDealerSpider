from bs4 import BeautifulSoup

with open('brand-data', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        if len(line) > 5:
            soup = BeautifulSoup(line, 'lxml')
            # print(soup)
            brand = soup.input.get('value')
            print(brand)

