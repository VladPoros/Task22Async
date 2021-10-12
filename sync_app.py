import datetime
import requests
from bs4 import BeautifulSoup

list_sites = []
with open("sites.txt", "r") as file1:
    for line in file1:
        list_sites.append(line.strip())


def get_html(url_site):
    try:
        url = requests.get(f"https://{url_site}", timeout=1)
        url.raise_for_status()
        return url.text
    except requests.exceptions.RequestException as err:
        print(url_site + ' - неверный сайт/запрещенный сайт')



def get_title(html):
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title
    if not title:
        return 'Нет заголовка'
    return title.text.strip()



def get_name():
    for url_name in list_sites:
        html = get_html(url_name)
        title = get_title(html)
        if not title:
            continue
        print(url_name + ' - ' + title)


def main():
    t0 = datetime.datetime.now()
    get_name()
    dt = datetime.datetime.now() - t0
    print(f'Done is {dt.total_seconds():.2f} sec.')


if __name__ == '__main__':
    main()
