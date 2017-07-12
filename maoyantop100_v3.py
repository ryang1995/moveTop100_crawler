# -*- coding:utf-8 -*-
from multiprocessing import Pool
import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def get_one_page(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException as e:
		return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    movie_data = soup.find_all('dd')
    for item in movie_data:
        yield {
            'index': item.find('i').text,
            'image': item.find('img', {'class':'board-img'})['data-src'],
            'title': item.find('p', {'class':'name'}).text,
            'actor': item.find('p', {'class':'star'}).text.strip()[3:],
            'time': item.find('p', {'class':'releasetime'}).text[5:],
            'score': item.find('p', {'class':'score'}).text
        }

def write_to_file(content):
    with open('result3.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
