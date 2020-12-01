from scraper import Article, get_news
from sender import Sender


def main():
    articles = get_news()
    sender = Sender()
    sender.spam_news(articles)


if __name__ == "__main__":
    main()
