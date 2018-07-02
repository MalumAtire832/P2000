import sqlite3

from p2000 import utils
from p2000.storage.units import helpers
from p2000.objects import Unit, Singleton


class Connection(metaclass=Singleton):
    """
    This class is responsible for writing the database to and from a SQLite database.
    The details of the database are in the config.json.
    """

    INSERT_STATEMENT = 'INSERT INTO units (capcode, region, town, function, discipline) VALUES (?, ?, ?, ?, ?)'

    def __init__(self):
        """
        Created a new Singleton Database to  write and read from.
        The database is initialized with the path given in `config.json["database"]["database"]["path"]`.
        The tables are dropped each time the application is started by default, this can be changed by
        setting `config.json["database"]["database"]["refresh_on_start"]` to `False`
        """
        refresh = utils.load_config()["database"]["units"]["refresh_on_start"]
        db_path = utils.load_config()["database"]["units"]["path"]
        self.connection = sqlite3.connect(db_path)
        helpers.create_units_table(self.connection, drop=refresh)

    def write_units(self, units):
        """
        Write multiple Unit objects to the database.
        :param units: The database to write to the database.
        :return: Nothing
        :raises TypeError: Raised when any of the database is not a Unit object.
        """
        cursor = self.connection.cursor()
        for unit in units:
            if not isinstance(unit, Unit):
                raise TypeError("Parameter unit is not of type Unit.")
            params = helpers.unit_to_params(unit)
            cursor.execute(self.INSERT_STATEMENT, params)
        self.connection.commit()

    def write_unit(self, unit):
        """
        Write a single Unit object to the database.
        :param unit: The unit to write to the database.
        :return: Nothing
        :raises TypeError: Raised when the unit is not a Unit object.
        """
        if not isinstance(unit, Unit):
            raise TypeError("Parameter unit is not of type Unit.")
        params = helpers.unit_to_params(unit)
        self.connection.execute(self.INSERT_STATEMENT, params)
        self.connection.commit()

    def find_units(self, capcode, limit=None):
        """
        Search the database for any database matching the given capcode.
        :param capcode: The capcode to search the database for.
        :param limit: The maximum amount of result to fetch, default is unlimited.
        :return: A List of Unit objects, or an empty List if none were found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM units WHERE capcode =?", [capcode])
        rows = cursor.fetchall() if limit is None else cursor.fetchmany(limit)
        return [helpers.row_to_unit(row) for row in rows]

    def find_unit(self, capcode):
        """
        Search the database for any database matching the given capcode.
        Only one Unit is returned at all times, even if multiple are found, the first is returned.
        :param capcode: The capcode to search the database for.
        :return: A Unit object, or None if none were found.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM units WHERE capcode =?", [capcode])
        row = cursor.fetchone()
        return helpers.row_to_unit(row)
