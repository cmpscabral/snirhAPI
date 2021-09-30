from app.crawler.base import BaseCrawler
from bs4 import BeautifulSoup


class Stations(BaseCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_stations_ids(self):
        """return a dict with station code and id: {'22E/01UG': '920686062', ... ,'18B/04UG': '920685966'}"""
        res = self.session.get(self.stations_url)
        soup = BeautifulSoup(res.text, "html.parser")
        data = {}
        for station in soup.find_all("marker"):
            code = station["estacao"].split("(")[-1].split(")")[0]
            data[code] = station["site"]
        return data

    def get_stations_details(self):
        res = self.session.get(self.stations_details_url)
        soup = BeautifulSoup(res.text, "html.parser")
        headers_dom = soup.find("thead").find("tr")
        headers = [h.text for h in headers_dom.find_all("td")]

        data = []
        for row in soup.find("tbody").find_all("tr"):
            row_data = {}
            for index, cell in enumerate(row.find_all("td")):
                row_data[headers[index]] = cell.text
            data.append(row_data)
        return data

    def get(self):
        ids = self.get_stations_ids()
        stations = self.get_stations_details()
        for station in stations[:]:
            try:
                station["ID"] = ids[station["CÓDIGO"]]
            except KeyError:
                stations.remove(station)
        return stations
