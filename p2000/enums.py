from enum import Enum


# noinspection PyTypeChecker
class Region(Enum):
    """
    This enum holds all the regions in the Netherlands covered by the P2000 system.
    Every Region has a dict that has a 2 digit "id" represented as a String, a "url" that should be
    glued onto the end of the Scraper.REGIONS_URL to make a valid page.
    Every Region also has a "name", this name can be used to visually represent the region
    in an eventual application.
    """
    # Todo - Maybe move the initial values to the config.json to make them easily editable.
    __order__ = """
                UNKNOWN GRONINGEN FRIESLAND DRENTHE IJSSELLAND TWENTE
                GELDERLAND_NEO GELDERLAND_MIDDEN GELDERLAND_ZUID UTRECHT
                NOORD_HOLLAND ZAANSTREEK_WATERLAND KENNERMERLAND AMSTERDAM_AMSTELLAND
                GOOI_EN_VECHTSTREEK HAAGLANDEN HOLLANDS_MIDDEN ROTTERDAM_RIJNMOND
                ZUID_HOLLAND ZEELAND BRABANT_MIDWEST BRABANT_NOORD BRABANT_ZUIDOOST
                LIMBURG_NOORD LIMBURG_ZUID FLEVOLAND KWC_KNRM
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
    def all():
        return [r for r in Region][1:]

    @staticmethod
    def match_by_id(val):
        """
        Check to see what Region is matched with the given id.
        This method checks every Region for it's id.
        :param val: The id to verify.
        :return: A Region object if a match is found, Region.UNKNOWN if no match was found.
        """
        for region in Region:
            if region.value["id"] == str(val):
                return region
        return Region.UNKNOWN


# noinspection PyTypeChecker
class Discipline(Enum):
    """
    Represents a discipline in the Dutch national service.
    Each discipline has a dict with a string id and a list of keywords that can be
    matched against the titles of sidebar links in the Scraper.
    """
    # Todo - Maybe move the initial values to the config.json to make them easily editable.
    __order__ = 'UNKNOWN FIRE_DEPARTMENT AMBULANCE POLICE KNRM'

    UNKNOWN =         {"id": "00", "keywords": []}
    FIRE_DEPARTMENT = {"id": "01", "keywords": ["brandweer"]}
    AMBULANCE =       {"id": "02", "keywords": ["ambulance", "ghor", "ovd-g"]}
    POLICE =          {"id": "03", "keywords": ["politie", "copi", "sgbo", "persinfo", "persvoorlichter", "voa", "bhv"]}
    KNRM =            {"id": "04", "keywords": ["knrm", "kwc"]}

    @staticmethod
    def all():
        return [d for d in Discipline][1:]

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
