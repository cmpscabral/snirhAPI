from app.client.base import BaseCrawler
from bs4 import BeautifulSoup
from app.utils import format_date


class GetData(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, sites, pars, tmin, tmax):
        tmin = format_date(tmin)
        tmax = format_date(tmax)
        res = self.session.get(
            self.data_url,
            params={
                "sites": sites,
                "pars": pars,
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
                    {
                        "timestamp": cells[0].text.strip(),
                        "value": cells[1].text.strip(),
                    }
                )
        return data
