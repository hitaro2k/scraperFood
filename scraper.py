import requests
from bs4 import BeautifulSoup
import json

user_input = input("Set product: ")


def connection(food):
    url = f"https://klopotenko.com/{food}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.bbc.com/news',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'DNT': '1',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    blockSearch = soup.findAll("div", class_="item-content rtin-content rtin-content-block vertical-style")

    searchear(blockSearch)


def searchear(block):
    titleList = []
    timeList = []
    diffList = []
    arr = []
    for titles in block:
        titles = titles.findAll("h3", class_="item-title")
        for links in titles:
            linkArr = links.findAll("a")
            for link in linkArr:
                link = link
                titleList.append(link.text)


    for timeBlocks in block:
        timeBlock = timeBlocks.findAll("div", class_="media-body space-sm")
        for timeTitles in timeBlock:
            timeTitle = timeTitles.findAll("div" , class_='feature-sub-title')
            for title in timeTitle:
                arr.append(title.text)

    n = 3
    sublists = [arr[i:i + n] for i in range(0, len(arr), n)]
    modified_sublists = [[item for index, item in enumerate(sublist) if index != 1] for sublist in sublists]
    flattened_list = [item for sublist in modified_sublists for item in sublist]

    for index, value in enumerate(flattened_list):
        if index % 2 != 0:
            diffList.append(value)
        else:
            timeList.append(value)

    obj = [{"name": name, "time": time, "difficulty": diff , "link" : f"https://klopotenko.com/{transliterate(name)}"} for name, time, diff in zip(titleList, timeList, diffList)]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def transliterate(text):
    special_cases = {
        'рецепт': 'reczept',
        'найважливіших': 'najvazhlivishih'
    }


    translit_dict_uk = {
        'А': 'a', 'а': 'a', 'Б': 'b', 'б': 'b', 'В': 'v', 'в': 'v',
        'Г': 'h', 'г': 'g', 'Ґ': 'g', 'ґ': 'g', 'Д': 'd', 'д': 'd',
        'Е': 'e', 'е': 'e', 'Є': 'ye', 'є': 'ye', 'Ж': 'zh', 'ж': 'zh',
        'З': 'z', 'з': 'z', 'И': 'y', 'и': 'y', 'І': 'i', 'і': 'i',
        'Ї': 'yi', 'ї': 'i', 'Й': 'y', 'й': 'j', 'К': 'k', 'к': 'k',
        'Л': 'l', 'л': 'l', 'М': 'm', 'м': 'm', 'Н': 'n', 'н': 'n',
        'О': 'o', 'о': 'o', 'П': 'p', 'п': 'p', 'Р': 'r', 'р': 'r',
        'С': 's', 'с': 's', 'Т': 't', 'т': 't', 'У': 'u', 'у': 'u',
        'Ф': 'f', 'ф': 'f', 'Х': 'h', 'х': 'h', 'Ц': 'cz', 'ц': 'cz',
        'Ч': 'ch', 'ч': 'ch', 'Ш': 'sh', 'ш': 'sh', 'Щ': 'shch', 'щ': 'shch',
        'Ь': '', 'ь': '', 'Ю': 'yu', 'ю': 'iu', 'Я': 'ya', 'я': 'ia',
        ' ': '-', '.': '', ',': '', '!': '', '?': '', ':': '', ';': '',
        '"': '', "'": '', '(': '', ')': '', '[': '', ']': '', '{': '', '}': ''
    }

    for key, value in special_cases.items():
        text = text.replace(key, value)

    transliterated_text = ''.join([translit_dict_uk.get(char, char) for char in text.lower()])

    transliterated_text = transliterated_text.replace('--', '-')
    if not transliterated_text.endswith('/'):
        transliterated_text += '/'

    return transliterated_text


connection(user_input)