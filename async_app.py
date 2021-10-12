import datetime
from bs4 import BeautifulSoup
import asyncio
import aiohttp

list_sites = []
with open("sites.txt", "r") as file1:
    for line in file1:
        list_sites.append(line.strip())


async def get_html(url_site):
    try:
        url = f"https://{url_site}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as newurl:
                newurl.raise_for_status()
                return await newurl.text()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        print(url_site + ' - неверный сайт/запрещенный сайт')


def get_title(html):
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title
    if not title:
        return 'Нет заголовка'
    return title.text.strip()


async def get_name():
    task = []
    for url_name in list_sites:
        task.append(asyncio.get_event_loop().create_task(get_html(url_name)))
    for url_name in task:
        html = await url_name
        title = get_title(html)
        if not title:
            continue
        print(title)



def main():
    t0 = datetime.datetime.now()
    asyncio.run(get_name())
    dt = datetime.datetime.now() - t0
    print(f'Async done is {dt.total_seconds():.2f} sec.')


if __name__ == '__main__':
    main()
