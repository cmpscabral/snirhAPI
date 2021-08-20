from src.client.base import BaseCrawler
from bs4 import BeautifulSoup

# from client.exceptions import NetworkSelectionError


class Networks(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        res = self.session.get(self.home_url)
        soup = BeautifulSoup(res.text, "html.parser")
        networks = soup.find("select", {"name": "f_redes_todas[]"})
        return [{"id": n["value"], "name": n.text} for n in networks.find_all("option")]


if __name__ == "__main__":
    bot = Networks()
    data = bot.get_networks()
    print(data)
