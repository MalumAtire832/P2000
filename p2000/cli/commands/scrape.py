from progress.bar import ShadyBar

from p2000.cli.commands.base import Base


class Scrape(Base):
    from p2000.enums import Region
    from p2000.storage.units import Connection, Scraper

    def run(self):
        try:
            self.write_all_units()
        except IOError as error:
            print(error.message)
        except KeyboardInterrupt:
            print ("Interrupt detected, shutting down.")

    def unit_bar(self, total):
        return ShadyBar(
            message='Writing unit %(index)d of %(max)d',
            max=total,
            suffix='%(percent)d%%'
        )

    def scrape_bar(self, total):
        return ShadyBar(
            message="Scraping units from the web",
            max=total,
            suffix='%(percent)d%%'
        )

    def fetch_all_units(self):
        result = []
        regions = Scrape.Region.all()
        bar = self.scrape_bar(len(regions))
        try:
            for region in regions:
                scraper = Scrape.Scraper(region)
                units = scraper.get_units()
                for discipline in units:
                    for unit in discipline:
                        result.append(unit)
                bar.next()
        except IOError as error:
            raise IOError(error.message)
        finally:
            bar.finish()
            return result

    def write_all_units(self):
        units = self.fetch_all_units()
        bar = self.unit_bar(len(units))
        try:
            connection = Scrape.Connection().establish()
            for unit in units:
                connection.write_unit(unit)
                bar.next()
            bar.finish()
        except IOError as error:
            raise IOError(error.message)
        finally:
            bar.finish()
