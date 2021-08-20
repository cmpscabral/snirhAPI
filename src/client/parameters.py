from client.base import BaseCrawler
from bs4 import BeautifulSoup

# from client.exceptions import NetworkSelectionError


class Parameters(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, station):
        res = self.session.get(self.parameters_url, params={"sites": station})
        print(res.url)
        soup = BeautifulSoup(res.text, "html.parser")
        return [
            {"id": o["value"], "name": o.text.replace("■", "").strip()}
            for o in soup.find_all("option")
        ]


if __name__ == "__main__":
    bot = Parameters()
    bot.select_network(920123704)
    bot.get_parameters(920685726)
