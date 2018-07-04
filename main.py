# import p2000.rtlsdr as rtlsdr
# from p2000.rtlsdr import AbstractReader
#
#
# class MyReader(AbstractReader):
#
#     def act(self, raw):
#         line = self.create_line(raw)
#         if self.is_line_blacklisted(line):
#             print("== LINE IS BLACKLISTED ==")
#         else:
#             print(str(line))
#
#
# connection = rtlsdr.Connection()
# reader = MyReader()
# reader.attach(connection)

from p2000 import Region
from p2000.storage.units import Scraper, Connection as UConnection


scraper = Scraper(Region.GRONINGEN)
uc = UConnection()
units = scraper.get_units(scraper.get_discipline_links()[0])
for unit in units:
    uc.write_unit(unit)
