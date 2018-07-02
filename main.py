from p2000.rtlsdr import Connection, AbstractReader
from p2000.tomzulu import Scraper, Region, Database
from progress.bar import Bar
from pprint import pprint


class MyReader(AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


def fetch_all_units():
    result = []
    regions = Region.all()
    bar = Bar("Scraping units from the web", max=len(regions), fill="■", suffix='%(percent)d%%')
    for region in regions:
        scraper = Scraper(region)
        units = scraper.get_units()
        for discipline in units:
            for unit in discipline:
                result.append(unit)
        bar.next()
    bar.finish()
    return result


def write_all_units():
    units = fetch_all_units()
    writer = Database()
    bar = Bar(message='Writing unit %(index)d of %(max)d', max=len(units), fill="■", suffix='%(percent)d%%')
    for unit in units:
        writer.write_unit(unit)
        bar.next()
    bar.finish()


# write_all_units()

# scraper = Scraper(Region.FRIESLAND)
# landing = scraper.get_landing_page()
# links = scraper.get_discipline_links(landing)
# units = scraper.get_units(links[0])
#
# writer = Database()
# writer.write_units(units)
# unit = writer.find_unit("0300050")
# units = writer.find_units("0300050")
#
# pprint(unit)
# pprint(units)

# for discipline in units:
#     pprint("{0} Size = {1}".format(discipline[0].discipline, len(discipline)))


# connection = Connection()
# reader = MyReader()
# reader.attach(connection)


