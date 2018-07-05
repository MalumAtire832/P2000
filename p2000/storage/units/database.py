from pymongo import MongoClient

from p2000 import Unit, Region, Discipline
from p2000.storage.database import AbstractConnection


class Connection(AbstractConnection):
    """
    This class is responsible for writing the database to and from a SQLite database.
    The details of the database are in the config.json.
    """

    def __init__(self):
        """
        Created a new Singleton Database to  write and read from.
        The database is initialized with values from config.json["database"]["collections"]["units"]
        and config.json["database"]["url"]
        """
        super(Connection, self).__init__()

    def init(self):
        self.client = MongoClient(self.mongo_url())
        self.db = self.client[self.db_name()]
        self.collection = self.db[self.collection_name()]

    def mongo_url(self):
        return self.config["database"]["url"]

    def db_name(self):
        return self.config["database"]["name"]

    def collection_name(self):
        return self.config["database"]["collections"]["units"]["name"]

    def object_to_row(self, obj):
        if not isinstance(obj, Unit):
            raise TypeError("Param 'obj' is not of type 'Unit'.")
        return {
            "capcode": obj.capcode,
            "region": obj.region.value["id"],
            "town": obj.town,
            "function": obj.function,
            "discipline": obj.discipline.value["id"]
        }

    def row_to_object(self, row):
        if not isinstance(row, dict):
            raise TypeError("Param 'row' is not of type 'dict'.")
        return Unit(
            capcode=row["capcode"],
            region=Region.match_by_id(
                row["region"]
            ),
            town=row["town"],
            function=row["function"],
            discipline=Discipline.match_by_id(
                row["discipline"]
            )
        )

    def write_units(self, units):
        """
        Write multiple Unit objects to the database.
        :param units: The database to write to the database.
        :return: Nothing
        :raises TypeError: Raised when any of the units is not a Unit object.
        """
        rows = [self.object_to_row(u) for u in units]
        self.collection.insert_many(rows)

    def write_unit(self, unit):
        """
        Write a single Unit object to the database.
        :param unit: The unit to write to the database.
        :return: Nothing
        :raises TypeError: Raised when the unit is not a Unit object.
        """
        row = self.object_to_row(unit)
        self.collection.insert_one(row)

    def find_units(self, capcode, limit=None):
        """
        Search the database for any database matching the given capcode.
        :param capcode: The capcode to search the database for.
        :param limit: The maximum amount of result to fetch, default is unlimited.
        :return: A List of Unit objects, or an empty List if none were found.
        """
        pass
