from p2000 import Region
from p2000.storage.units import Scraper, Connection

# Fetching the raw data.
scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units(links[0])

# Open the Database.
writer = Connection()
# Write a single unit.
writer.write_unit(units[0])
# Or write all the units.
writer.write_units(units)
