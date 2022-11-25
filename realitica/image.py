from datetime import *
from bs4 import BeautifulSoup
import requests, json, re, threading


url = 'https://www.realitica.com/en/listing/1777587'

req = requests.get(url)

if req.status_code == 200:

    soup = BeautifulSoup(req.text, 'lxml')
    image_elements = soup.find_all('img', attrs={'style':"margin-bottom:15px;"})

    for el in image_elements:
        with open(el.get('alt'), 'wb') as f:
            f.write(requests.get(el.get('src')).content)