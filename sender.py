from typing import List
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from scraper import Article
import time
from data_manager import data_manager


class Sender:

    def __init__(self):
        self.updater = Updater(self.__get_token())

    def spam_news(self, articles: List[Article]) -> None:
        for article in articles:
            self.updater.bot.send_photo(self.__get_chatid(), article.img_src, self.__generate_news(
                article), parse_mode=telegram.ParseMode.MARKDOWN, timeout=10)
            data_manager.save_news(article.link)
            time.sleep(4)

    def __generate_news(self, article: Article) -> str:
        news = '*[' + article.category + ']*\n'
        news += '🔗 ' + article.link + '\n\n'
        news += '*' + article.title + '*\n'
        news += article.content + '\n\n'
        news += '🕔 ' + article.date + '  👤 ' + article.author + '\n'
        news += '*Clicca il link in cima al post per visualizzare la notizia*'
        return news

    def __get_token(self) -> str:
        return data_manager.config['token']

    def __get_chatid(self) -> str:
        return data_manager.config['chat_id']
