from src.client.base import BaseCrawler
from bs4 import BeautifulSoup


class GetData(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, sites, pars, tmin, tmax):
        res = self.session.get(
            self.data_url,
            params={
                "sites": sites,
                "pars": pars,
                "tmin": tmin,
                "tmax": tmax,
            },
        )
        soup = BeautifulSoup(res.text, "html.parser")
        data_table = soup.find_all("table")[-1]
        rows = data_table.find_all("tr")

        data = []
        # to add the name
        # name = rows[0].find_all("td")[-1].text
        # data = [name]
        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) == 2:
                data.append(
                    {
                        "timestamp": cells[0].text.strip(),
                        "value": cells[1].text.strip(),
                    }
                )
        return data


# bot = GetData()
# bot.select_network(920123704)
# stations = bot.get_stations()
# print(stations)
# data = bot.get_data(sites=920684954, pars=4237, tmin="01/11/1931", tmax="16/08/2021")
# print(data)
