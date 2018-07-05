import abc

import p2000.utils


class AbstractConnection:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractConnection, self).__init__()
        self.client = None
        self.db = None
        self.collection = None
        self.init()

    @abc.abstractmethod
    def init(self):
        """
        Initialize the database.
        :return: None
        """
        pass

    @abc.abstractproperty
    def mongo_url(self):
        """
        The path to the database.
        :return: Returns a string with the path to the database.
        """
        pass

    @abc.abstractproperty
    def db_name(self):
        """
        The name of the database.
        :return: Returns a string with the name of the database.
        """
        pass

    @abc.abstractproperty
    def collection_name(self):
        """
        The name of the database.
        :return: Returns a string with the name of the database.
        """
        pass

    @property
    def config(self):
        """
        The config file in json/dict format.
        :return: A Dict with all the config settings.
        """
        return p2000.utils.load_config()

    @abc.abstractmethod
    def object_to_row(self, obj):
        """
        Convert the given object to a correct row dictionary.
        :param obj: The object to convert.
        :return: A Dict with the values of the given object.
        :raises TypeError: If the parm is not of type object
        """
        pass

    @abc.abstractmethod
    def row_to_object(self, row):
        """
        Convert the given row to a correct object.
        :param row: The row to convert.
        :return: A object with the values of the given dict.
        :raises TypeError: If the parm is not of type Dict.
        """
        pass

    def drop_collection(self):
        """
        **WARNING, DATA CANNOT BE RECOVERED**
        Destroy/ Drop the current database.
        :return: None
        """
        self.client[self.collection_name].drop()
