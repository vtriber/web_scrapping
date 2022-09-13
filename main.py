import requests
import bs4
from fake_headers import Headers


def scrapping():
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    header = Headers(browser="chrome", os="win, headers=True")
    HEADERS = header.generate()
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'

    response = requests.get(url, headers=HEADERS)
    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all("article")
    articles_dict = {}
    for article in articles:
        previews = article.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        for preview in previews:
            previews = preview.text.strip().lower()

            for keyword in KEYWORDS:
                if previews.find(keyword.lower()) != -1:
                    datetime_ = article.find(class_="tm-article-snippet__datetime-published").contents[0].attrs['title']
                    title = article.find("h2").find("span").text
                    href = base_url + article.find(class_="tm-article-snippet__title-link").attrs['href']
                    dict_ = {href: [title, datetime_]}
                    articles_dict.update(dict_)
    if articles_dict != {}:
        for href, articles in articles_dict.items():
            print(f'<{articles[1]}>-<{articles[0]}>-<{href}>')
    else:
        print('Ключевые слова не встречаются в preview-информации')

if __name__=='__main__':
    scrapping()