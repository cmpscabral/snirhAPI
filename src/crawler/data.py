from typing import List

from bs4 import BeautifulSoup
from src.crawler.base import BaseCrawler
from src.models import DataEntry
from src.utils import format_date


class GetData(BaseCrawler):
    def get_data(
        self, station_id: str, parameter_id: str, tmin: str, tmax: str
    ) -> List[DataEntry]:
        tmin = format_date(tmin)
        tmax = format_date(tmax)
        res = self.session.get(
            self.data_url,
            params={
                "sites": station_id,
                "pars": parameter_id,
                "tmin": tmin,
                "tmax": tmax,
            },
        )
        print(res.status_code)
        print(res.url)
        soup = BeautifulSoup(res.text, "html.parser")
        data_table = soup.find_all("table")[-1]
        rows = data_table.find_all("tr")

        data = []
        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) == 2:
                data.append(
                    DataEntry(
                        timestamp=cells[0].text.strip(),
                        value=cells[1].text.strip(),
                    )
                )
        return data
