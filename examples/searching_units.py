from p2000 import Region
from p2000.storage.units import Scraper, Connection

# Fetching the raw data.
scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units(links[0])

# Open the Database.
writer = Connection()
# Write all the units.
writer.write_units(units)

# Search for a single unit, even if multiple exist only one is returned.
unit = writer.find_unit("0300050")
# Search for multiple units, a default can be set as wel, default limit is unlimited.
units = writer.find_units("0300050", limit=10)
