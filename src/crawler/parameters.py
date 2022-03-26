from typing import List

from bs4 import BeautifulSoup
from src.crawler.base import BaseCrawler
from src.models import Parameter


class Parameters(BaseCrawler):
    def get(self, station_id: str) -> List[Parameter]:
        res = self.session.get(self.parameters_url, params={"sites": station_id})
        print(res.url)
        soup = BeautifulSoup(res.text, "html.parser")
        return [
            Parameter(id=o["value"], name=o.text.replace("■", "").strip())
            for o in soup.find_all("option")
        ]
