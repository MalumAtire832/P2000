from pprint import pprint

from p2000 import Region, Discipline
from p2000.storage.units import Scraper

# Fetching the raw data.
scraper = Scraper(Region.FRIESLAND)
units = scraper.get_units(Discipline.FIRE_DEPARTMENT)
pprint(units)
