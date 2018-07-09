from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from p2000 import Discipline
from p2000 import Unit


# noinspection PyMethodMayBeStatic
class Scraper:
    BASE_URL = "https://www.tomzulu10capcodes.nl"
    REGIONS_URL = "https://www.tomzulu10capcodes.nl/capcodes-per-regio/"

    def __init__(self, region):
        self.region = region

    def get_page(self, url):
        """
        Try to fetch the page that is at the given url.
        :param url: The url where the page is located.
        :return: The html of the page a String, or None is the response was not valid.
        :raises IOError: When the application encounters an error fetching the page.
        """
        try:
            with closing(get(url, stream=True)) as response:
                if self.__is_valid_response__(response):
                    return response.content.decode("utf-8")
                else:
                    return None
        except RequestException as error:
            raise IOError("Error during request to {0} : {1}".format(url, error))

    def get_region_url(self):
        """
        Format the region url for the current instance.
        The url is based on the REGIONS_URL and the url value of the current instance region.
        :return: The url as a string, ex. "https://www.tomzulu10capcodes.nl/capcodes-per-regio/01-groningen"
        """
        return self.REGIONS_URL + self.region.value["url"]

    def __get_discipline_links__(self):
        """
        Fetch the sidebar links to various disciplines from the given landing page.
        :param landing: The html of the landing page, if no page is given it is fetched using `get_landing_page()`
        :return: A list with discipline link dicts, each with a discipline and a url.
        """
        landing = self.get_page(self.get_region_url())
        html = BeautifulSoup(landing, 'html.parser')
        items = html.find_all("a", {"class": "jw-section-menu-list-item"})
        return [self.__create_dp_link__(item) for item in items]

    def __create_dp_link__(self, item):
        """
        Create a new discipline link dict from the given item.
        The url value is used for fetching the discipline page.
        The correct Discipline is fetched using `Discipline.match()`
        :param item: The item to turn into a discipline link dict.
        :return: A dict with the keys `discipline` and `url`
        """
        return {
            "discipline": Discipline.match(item.getText()),
            "url": item["href"]
        }

    def __create_dp_url__(self, discipline_link):
        """
        Create the url for a discipline page.
        The url is made by combining the `Scraper.BASE_URL` with the url from the given discipline link dict.
        :param discipline_link: The discipline link dict to extract the url from.
        :return: The url as a String,
            ex. "https://www.tomzulu10capcodes.nl/capcodes-per-regio/01-groningen/capcodes-brandweer-roepnummers-1"
        """
        return self.BASE_URL + discipline_link["url"]

    def get_units(self, discipline=None):
        """
        Fetch all the database from the given discipline page.
        See `__get_units__` for detailed info.
        All disciplines are fetched if no discipline_link is given.
        :param discipline: The discipline to fetch the units for, default is all disciplines.
        :return: A list of Unit objects, or a list of lists with Unit objects if no link is given.
        """
        links = self.__get_discipline_links__()
        if discipline is None:
            return [u for u in (self.__get_units__(l) for l in links)]
        else:
            return [self.__get_units__(l) if l["discipline"] == discipline else None for l in links][0]

    def __get_units__(self, discipline_link):
        """
        Fetch all the database from the given discipline page.
        The database are extracted from the main table and turned into Unit objects.
        The region of the unit is the current instance region, and the Discipline is equal
        to the `discipline` key value in the given `discipline_link` dict.
        :param discipline_link: The link to fetch the page for and extract the database from.
        :return: A list of extracted Unit objects.
        """
        page = self.get_page(self.__create_dp_url__(discipline_link))
        html = BeautifulSoup(page, "html.parser")
        table = html.find("table", {"class": "jw-table jw-table--header jw-table--striped"}).find("tbody")
        result = []
        for row in table.find_all("tr"):
            values = [td.getText() for td in row.find_all("td")]
            result.append(
                Unit(
                    capcode=values[0], town=values[1], function=values[2],
                    region=self.region, discipline=discipline_link["discipline"]
                )
            )
        return result

    def __is_valid_response__(self, resp):
        """
        Check to see if the given response is valid, based on a 200 status code and if the content is actual html.
        :param resp: The response to validate.
        :return: True if the response is valid, else False.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)
