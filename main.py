import rtlsdr
from tomzulu import Scraper, Region
from pprint import pprint


class MyReader(rtlsdr.AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


# scraper = Scraper(Region.FRIESLAND)
# landing = scraper.get_landing_page()
# links = scraper.get_discipline_links(landing)
# units = scraper.get_units()
#
# for discipline in units:
#     pprint("{0} Size = {1}".format(discipline[0].discipline, len(discipline)))


connection = rtlsdr.Connection()
reader = MyReader()
reader.attach(connection)
