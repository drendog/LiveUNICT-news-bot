from typing import List
import requests
from bs4 import BeautifulSoup
from data_manager import data_manager


class Article:
    def __init__(self, soup_article):
        self.category = self.__get_article_text_element(
            soup_article, 'span', class_='meta-category')
        self.title = self.__get_article_text_element(
            soup_article, 'h2', class_='entry-title h3')
        self.content = self.__sanitize_content(
            self.__get_article_text_element(soup_article, 'div', class_='entry-content'))
        self.date = self.__get_article_text_element(
            soup_article, 'div', class_='herald-date')
        self.author = self.__get_article_text_element(
            soup_article, 'span', class_='author')
        self.link = self.get_article_link(soup_article)
        self.img_src = self.__get_img_src(soup_article)

    def __get_img_src(self, soup_article) -> str:
        src: str = soup_article.find('img', class_='wp-post-image')['src']
        index_resize = src.find('?resize')
        if index_resize != -1:
            return src[:index_resize]
        return src

    @staticmethod
    def get_article_link(soup_article) -> str:
        entry_title = soup_article.find('h2', class_='entry-title')
        return entry_title.find('a', href=True)['href']

    def __sanitize_content(self, content: str) -> str:
        content = content.replace('\n', '')
        if content.endswith('300'):
            return content[:(len(content) - 3)]
        return content

    def __get_article_text_element(self, soup_article, tag, **kwargs) -> str:
        element = soup_article.find(tag, **kwargs)
        if element is None:
            return None
        return element.get_text()


def scan_today_news() -> List[Article]:
    articles: List[Article] = []
    for page_link in data_manager.config['pages']:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_articles = soup.find_all('article', class_='herald-lay-b')
        for soup_article in soup_articles:
            link = Article.get_article_link(soup_article)
            if data_manager.is_new_article(link):
                articles.append(Article(soup_article))
    return articles


def get_news() -> List[Article]:
    articles = scan_today_news()
    articles.reverse()
    return articles
