from progress.bar import ShadyBar

from p2000 import Region, Discipline, Unit
from p2000.storage.units import Connection, Scraper


def row_to_unit(row):
    """
    Convert a row(Tuple) from the database to a Unit object.
    :param row: The row/Tuple to convert.
    :return: A Unit object with the same values as the Tuple, Region and Disciplines are matched as wel.
    """
    if row is None:
        return None
    else:
        return Unit(
            capcode=row[1],
            region=Region.match_by_id(row[2]),
            town=row[3],
            function=row[4],
            discipline=Discipline.match_by_id(row[5]),
        )


def unit_to_params(unit):
    """
    Creates a tuple from the given Unit object's values.
    This tuple can be used as parameters for a Unit insert query.
    :param unit: The unit to convert.
    :return: A tuple of strings in the following format: (capcode, region[id], town, function, discipline[id])
    """
    return (
        unit.capcode,
        unit.region.value["id"],
        unit.town,
        unit.function,
        unit.discipline.value["id"]
    )


def drop_units_table(connection):
    """
    Drop the database table.
    :param connection:
    :return: Nothing
    """
    connection.execute("DROP TABLE IF EXISTS database;")
    connection.commit()


def create_units_table(connection, drop=False):
    """
    Create the database table.
    :param connection:
    :param drop: True if the table should be dropped before this operation, default is False.
    :return: Nothing
    """
    if drop:
        drop_units_table(connection)
    connection.execute(
        "CREATE TABLE database("
            "id          INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,"
            "capcode     TEXT NOT NULL,"
            "region      TEXT,"
            "town      TEXT,"
            "function    TEXT,"
            "discipline  TEXT"
        ");")
    connection.commit()


def unit_bar(total):
    return ShadyBar(
        message='Writing unit %(index)d of %(max)d',
        max=total,
        suffix='%(percent)d%%'
    )


def scrape_bar(total):
    return ShadyBar(
        message="Scraping database from the web",
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
    writer = Connection()
    bar = unit_bar(len(units))
    for unit in units:
        writer.write_unit(unit)
        bar.next()
    bar.finish()
