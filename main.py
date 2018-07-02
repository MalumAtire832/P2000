from p2000.rtlsdr import Connection, AbstractReader
from p2000.tomzulu import Scraper, Region, Database
from pprint import pprint


class MyReader(AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


scraper = Scraper(Region.FRIESLAND)
landing = scraper.get_landing_page()
links = scraper.get_discipline_links(landing)
units = scraper.get_units(links[0])

writer = Database()
writer.write_units(units)
unit = writer.find_unit("0300050")
units = writer.find_units("0300050")

pprint(unit)
pprint(units)
# for discipline in units:
#     pprint("{0} Size = {1}".format(discipline[0].discipline, len(discipline)))


# connection = Connection()
# reader = MyReader()
# reader.attach(connection)
