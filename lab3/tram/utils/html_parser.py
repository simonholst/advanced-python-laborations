import pprint
import re
from urllib import request
import os
from django.conf import settings
from bs4 import BeautifulSoup
from .trams import TramNetwork

STOPS_URL = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
TRAM_STOP_HTML = os.path.join(settings.BASE_DIR,
                              'tram/templates/tram/tram_stops.html')
TRAM_STOP_URL_BASE = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='


def __download_html(url, file_path):
    response = request.urlopen(url)
    web_content = response.read().decode('UTF-8')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(web_content)


def __fetch_html_stop_classes():
    with open(TRAM_STOP_HTML, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    results = soup.find_all(class_='mb-1')
    return str(results).split('</li>, <li class="mb-1">')


def __create_stop_links(stop_classes, network):
    stop_links = dict()
    for stop_class in stop_classes:
        stop_class = stop_class.lower()
        if 'zon a' not in stop_class:
            continue
        for stop in network.all_stops():
            if f'{stop.name},' in stop_class:
                link_digits = re.findall(r'\d{16}', stop_class)[0]
                print(link_digits, stop.name)
                stop_links[stop.name] = f'{TRAM_STOP_URL_BASE}{link_digits}'
                continue
    return stop_links


def get_stop_links(network):
    stop_classes = __fetch_html_stop_classes()
    return __create_stop_links(stop_classes, network)


def main():
    network = TramNetwork.read_tram_network()
    stop_classes = __fetch_html_stop_classes()


if __name__ == '__main__':
    main()
