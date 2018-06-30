from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from enum import Enum


class Unit:

    def __init__(self, **kwargs):
        self.capcode = kwargs.get("capcode", "")
        self.region = kwargs.get("region", Region.UNKNOWN)
        self.town = kwargs.get("town", "")
        self.function = kwargs.get("function", "")
        self.discipline = kwargs.get("discipline", Discipline.UNKNOWN)

    def __repr__(self):
        result = "\n  capcode = {0}\n" \
                 "  region = {1}\n" \
                 "  town = {2}\n" \
                 "  function = {3}\n" \
                 "  discipline = {4}\n"
        return "{" + result.format(self.capcode, self.region, self.town, self.function, self.discipline) + "}"


class Discipline(Enum):
    """
    Represents a discipline in the Dutch national service.
    Each discipline has a dict with a numerical id and a list of keywords that can be
    matched against the titles of sidebar links in the Scraper.
    """
    UNKNOWN =         {"id": 0, "keywords": []}
    FIRE_DEPARTMENT = {"id": 1, "keywords": ["brandweer"]}
    AMBULANCE =       {"id": 2, "keywords": ["ambulance", "ghor", "ovd-g"]}
    POLICE =          {"id": 3, "keywords": ["politie", "copi", "sgbo", "persinfo", "persvoorlichter", "voa", "bhv"]}
    KNRM =            {"id": 4, "keywords": ["knrm", "kwc"]}

    @staticmethod
    def is_match(text, discipline):
        """
        Check to see if the given Discipline is a match for the given text.
        :param text: The text to check for the keywords in the given Discipline.
        :param discipline: The discipline to check the keywords for.
        :return: True if one of the keywords was found in the text, else False.
        :raises TypeError: When the given discipline is not a Discipline object.
        """
        if isinstance(discipline, Discipline):
            keywords = discipline.value["keywords"]
            if len(keywords) > 0:
                for keyword in keywords:
                    if keyword in text.lower():
                        return True
            return False
        else:
            raise TypeError("Parameter 'discipline' is not an instance of Discipline.")

    @staticmethod
    def match(text):
        """
        Check to see what Discipline is matched with the given text.
        This method checks every Discipline for keywords.
        :param text: The text to verify.
        :return: A Discipline object if a match is found, Discipline.UNKNOWN if no match was found.
        """
        for discipline in Discipline:
            if Discipline.is_match(text, discipline):
                return discipline
        return Discipline.UNKNOWN


class Region(Enum):
    # Todo - Maybe move the initial values to the config.json to make them easily editable.
    """
    This enum holds all the regions in the Netherlands covered by the P2000 system.
    Every Region has a dict that has a 2 digit "id" represented as a String, a "url" that should be
    glued onto the end of the Scraper.REGIONS_URL to make a valid page.
    Every Region also has a "name", this name can be used to visually represent the region
    in an eventual application.
    """
    UNKNOWN =              {'id': "00", 'url': "unknown", 'name': "Unknown"}
    GRONINGEN =            {'id': "01", 'url': "01-groningen", 'name': "Groningen"}
    FRIESLAND =            {'id': "02", 'url': "02-friesland", 'name': "Friesland"}
    DRENTHE =              {'id': "03", 'url': "03-drenthe", 'name': "Drenhte"}
    IJSSELLAND =           {'id': "04", 'url': "04-ijsselland", 'name': "IJsselland"}
    TWENTE =               {'id': "05", 'url': "05-twente", 'name': "Twente"}
    GELDERLAND_NEO =       {'id': "06", 'url': "06-noord-en-oost-gelderland", 'name': "Noord en Oost Gelderland"}
    GELDERLAND_MIDDEN =    {'id': "07", 'url': "07-gelderland-midden", 'name': "Gelderland Midden"}
    GELDERLAND_ZUID =      {'id': "08", 'url': "08-gelderland-zuid", 'name': "Gelderland Zuid"}
    UTRECHT =              {'id': "09", 'url': "09-utrecht", 'name': "Utrecht"}
    NOORD_HOLLAND =        {'id': "10", 'url': "10-noord-holland-noord", 'name': "Noord - Holland Noord"}
    ZAANSTREEK_WATERLAND = {'id': "11", 'url': "11", 'name': "Zaanstreek Waterland"}
    KENNERMERLAND =        {'id': "12", 'url': "12-kennermerland1", 'name': "Kennermerland"}
    AMSTERDAM_AMSTELLAND = {'id': "13", 'url': "12-kennermerland", 'name': "Amsterdam - Amstelland"}
    GOOI_EN_VECHTSTREEK =  {'id': "14", 'url': "14-gooi-en-vechstreek", 'name': "Gooi en Vechtstreek"}
    HAAGLANDEN =           {'id': "15", 'url': "15-haaglanden", 'name': "Haaglanden"}
    HOLLANDS_MIDDEN =      {'id': "16", 'url': "16-hollands-midden", 'name': "Hollands Midden"}
    ROTTERDAM_RIJNMOND =   {'id': "17", 'url': "17-rotterdam-rijnmond", 'name': "Rotterdam - Rijnmond"}
    ZUID_HOLLAND =         {'id': "18", 'url': "18-zuid-holland-zuid", 'name': "Zuid - Holland - Zuid"}
    ZEELAND =              {'id': "19", 'url': "19-zeeland", 'name': "Zeeland"}
    BRABANT_MIDWEST =      {'id': "20", 'url': "20-midden-en-west-brabant", 'name': "Midden - en West Brabant"}
    BRABANT_NOORD =        {'id': "21", 'url': "21-brabant-noord", 'name': "Brabant - Noord"}
    BRABANT_ZUIDOOST =     {'id': "22", 'url': "22-brabant-zuidoost", 'name': "Brabant - Zuidoost"}
    LIMBURG_NOORD =        {'id': "23", 'url': "23-limburg-noord", 'name': "Limburg - Noord"}
    LIMBURG_ZUID =         {'id': "24", 'url': "24-zuid-limburg1", 'name': "Zuid - Limburg"}
    FLEVOLAND =            {'id': "25", 'url': "25-flevoland", 'name': "Flevoland"}
    KWC_KNRM =             {'id': "26", 'url': "26-kwc-knrm", 'name': "KWC / KN"}


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

    def get_landing_page(self):
        """
        Fetch the landing page for the current instance.
        The `get_region_url()` method is used in combination with `get_page()` to fetch it.
        :return: The html of the landing page as a String.
        """
        return self.get_page(self.get_region_url())

    def get_discipline_links(self, landing=None):
        """
        Fetch the sidebar links to various disciplines from the given landing page.
        :param landing: The html of the landing page, if no page is given it is fetched using `get_landing_page()`
        :return: A list with discipline link dicts, each with a discipline and a url.
        """
        if landing is None:
            landing = self.get_landing_page()
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

    def get_units(self, discipline_link=None):
        """
        Fetch all the units from the given discipline page.
        See `__get_units__` for detailed info.
        All disciplines are fetched if no discipline_link is given.
        :param discipline_link: The discipline link dict to fetch the units from.
        :return: A list of Unit objects, or a list of lists with Unit objects if no link is given.
        """
        if discipline_link is None:
            return [self.__get_units__(d) for d in self.get_discipline_links()]
        else:
            return self.__get_units__(discipline_link)

    def __get_units__(self, discipline_link):
        """
        Fetch all the units from the given discipline page.
        The units are extracted from the main table and turned into Unit objects.
        The region of the unit is the current instance region, and the Discipline is equal
        to the `discipline` key value in the given `discipline_link` dict.
        :param discipline_link: The link to fetch the page for and extract the units from.
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
