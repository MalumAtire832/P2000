from p2000 import Region, Discipline


class Singleton(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Unit:

    def __init__(self, **kwargs):
        self.capcode = kwargs.get("capcode", "")
        self.region = kwargs.get("region", Region.UNKNOWN)
        self.town = kwargs.get("town", "")
        self.function = kwargs.get("function", "")
        self.discipline = kwargs.get("discipline", Discipline.UNKNOWN)

    def __repr__(self):
        result = "\n  capcode = {0}\n" \
                 "  region = {1}\n" \
                 "  town = {2}\n" \
                 "  function = {3}\n" \
                 "  discipline = {4}\n"
        return "{" + result.format(self.capcode, self.region, self.town, self.function, self.discipline) + "}"
