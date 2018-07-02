from p2000 import Region
from p2000.storage.units import Scraper, helpers


# Scraping for a single Region.
scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units()

for discipline in units:
    print("{0} Size = {1}".format(
        discipline[0].discipline,
        len(discipline)
    ))

# Fetch everything.
helpers.fetch_all_units()
