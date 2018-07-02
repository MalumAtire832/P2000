import json
from p2000.tomzulu import Scraper, Region, Database
from progress.bar import ShadyBar


def load_config():
    """
    Load the config file as JSON.
    :return: The config file as JSON.
    """
    with open('./resources/config.json') as file:
        return json.load(file)


def unit_bar(total):
    return ShadyBar(
        message='Writing unit %(index)d of %(max)d',
        max=total,
        suffix='%(percent)d%%'
    )


def scrape_bar(total):
    return ShadyBar(
        message="Scraping units from the web",
        max=total,
        suffix='%(percent)d%%'
    )


def fetch_all_units():
    result = []
    regions = Region.all()
    bar = scrape_bar(len(regions))
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
    bar = unit_bar(len(units))
    for unit in units:
        writer.write_unit(unit)
        bar.next()
    bar.finish()
