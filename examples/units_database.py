from p2000 import Region
from p2000.storage.units import Scraper, Connection

# Fetching the raw data.
scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units(links[0])

# Open the Database.
connection = Connection().establish()
# Write a single unit.
connection.write_unit(units[0])
# Or write all the units.
connection.write_units(units)
# Search for multiple units, a limit can be set as wel, default limit is unlimited.
units = connection.find_units("0300050", limit=10)
