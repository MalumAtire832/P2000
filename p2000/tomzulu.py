import sqlite3
from p2000 import utils
from p2000.singleton import Singleton
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
    Each discipline has a dict with a string id and a list of keywords that can be
    matched against the titles of sidebar links in the Scraper.
    """
    UNKNOWN =         {"id": "00", "keywords": []}
    FIRE_DEPARTMENT = {"id": "01", "keywords": ["brandweer"]}
    AMBULANCE =       {"id": "02", "keywords": ["ambulance", "ghor", "ovd-g"]}
    POLICE =          {"id": "03", "keywords": ["politie", "copi", "sgbo", "persinfo", "persvoorlichter", "voa", "bhv"]}
    KNRM =            {"id": "04", "keywords": ["knrm", "kwc"]}

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

    @staticmethod
    def match_by_id(val):
        """
        Check to see what Discipline is matched with the given id.
        This method checks every Discipline for it's id.
        :param val: The id to verify.
        :return: A Discipline object if a match is found, Discipline.UNKNOWN if no match was found.
        """
        for discipline in Discipline:
            if discipline.value["id"] == val:
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

    @staticmethod
    def match_by_id(val):
        """
        Check to see what Region is matched with the given id.
        This method checks every Region for it's id.
        :param val: The id to verify.
        :return: A Region object if a match is found, Region.UNKNOWN if no match was found.
        """
        for region in Region:
            if region.value["id"] == val:
                return region
        return Region.UNKNOWN


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


class Database(metaclass=Singleton):
    """
    This class is responsible for writing the units to and from a SQLite database.
    The details of the database are in the config.json.
    """

    INSERT_STATEMENT = 'INSERT INTO units (capcode, region, town, function, discipline) VALUES (?, ?, ?, ?, ?)'

    def __init__(self):
        """
        Created a new Singleton Database to  write and read from.
        The database is initialized with the path given in `config.json["tomzulu"]["database"]["path"]`.
        The tables are dropped each time the application is started by default, this can be changed by
        setting `config.json["tomzulu"]["database"]["refresh_on_start"]` to `False`
        """
        refresh = utils.load_config()["tomzulu"]["database"]["refresh_on_start"]
        db_path = utils.load_config()["tomzulu"]["database"]["path"]
        self.connection = sqlite3.connect(db_path)
        self.__create_units_table__(drop=refresh)

    def __drop_units_table(self):
        """
        Drop the units table.
        :return: Nothing
        """
        self.connection.execute("DROP TABLE IF EXISTS units;")
        self.connection.commit()

    def __create_units_table__(self, drop=False):
        """
        Create the units table.
        :param drop: True if the table should be dropped before this operation, default is False.
        :return: Nothing
        """
        if drop:
            self.__drop_units_table()
        self.connection.execute(
            "CREATE TABLE units("
                "id          INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,"
                "capcode     TEXT NOT NULL,"
                "region      TEXT,"
                "town      TEXT,"
                "function    TEXT,"
                "discipline  TEXT"
            ");")
        self.connection.commit()

    def write_units(self, units):
        """
        Write multiple Unit objects to the database.
        :param units: The units to write to the database.
        :return: Nothing
        :raises TypeError: Raised when any of the units is not a Unit object.
        """
        cursor = self.connection.cursor()
        for unit in units:
            if not isinstance(unit, Unit):
                raise TypeError("Parameter unit is not of type tomzulu.Unit")
            params = self.__unit_to_params__(unit)
            cursor.execute(self.INSERT_STATEMENT, params)
        self.connection.commit()

    def write_unit(self, unit):
        """
        Write a single Unit object to the database.
        :param unit: The unit to write to the database.
        :return: Nothing
        :raises TypeError: Raised when the unit is not a Unit object.
        """
        if not isinstance(unit, Unit):
            raise TypeError("Parameter unit is not of type tomzulu.Unit")
        params = self.__unit_to_params__(unit)
        self.connection.execute(self.INSERT_STATEMENT, params)
        self.connection.commit()

    # noinspection PyMethodMayBeStatic
    def __unit_to_params__(self, unit: Unit):
        """
        Creates a tuple from the given Unit object's values.
        This tuple can be used as parameters for a Unit insert query.
        :param unit: The unit to convert.
        :return: A tuple of strings in the following format: (capcode, region[id], town, function, discipline[id])
        """
        return (
            unit.capcode,
            unit.region.value["id"],
            unit.town,
            unit.function,
            unit.discipline.value["id"]
        )

    def find_units(self, capcode, limit=None):
        """
        Search the database for any units matching the given capcode.
        :param capcode: The capcode to search the database for.
        :param limit: The maximum amount of result to fetch, default is unlimited.
        :return: A List of Unit objects, or an empty List if none were found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM units WHERE capcode =?", [capcode])
        rows = cursor.fetchall() if limit is None else cursor.fetchmany(limit)
        return [self.__row_to_unit__(row) for row in rows]

    def find_unit(self, capcode):
        """
        Search the database for any units matching the given capcode.
        Only one Unit is returned at all times, even if multiple are found, the first is returned.
        :param capcode: The capcode to search the database for.
        :return: A Unit object, or None if none were found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM units WHERE capcode =?", [capcode])
        row = cursor.fetchone()
        return self.__row_to_unit__(row)

    # noinspection PyMethodMayBeStatic
    def __row_to_unit__(self, row):
        """
        Convert a row(Tuple) from the database to a Unit object.
        :param row: The row/Tuple to convert.
        :return: A Unit object with the same values as the Tuple, Region and Disciplines are matched as wel.
        """
        if row is None:
            return None
        else:
            return Unit(
                capcode=row[1],
                region=Region.match_by_id(row[2]),
                town=row[3],
                function=row[4],
                discipline=Discipline.match_by_id(row[5]),
            )
