from ruamel.yaml import YAML
from pathlib import Path


class DataManager:

    def __init__(self):
        path = Path('config/config.yaml')
        yaml = YAML()
        self.config = yaml.load(path)
        path = Path('data/news.yaml')
        self.data = yaml.load(path)

    def save_news(self, link) -> None:
        path = Path('data/news.yaml')
        self.data['news'].append(link)
        yaml = YAML()
        yaml.dump(self.data, path)

    def is_new_article(self, link) -> bool:
        return not (link in self.data['news'])


data_manager = DataManager()
