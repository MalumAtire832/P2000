from p2000 import Region, Discipline
from p2000.storage.units import Scraper


# Scraping for a single Region.
scraper = Scraper(Region.FRIESLAND)
units = scraper.get_units(Discipline.FIRE_DEPARTMENT)

for discipline in units:
    print("{0} Size = {1}".format(
        discipline[0].discipline,
        len(discipline)
    ))
