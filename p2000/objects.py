from p2000.enums import Region, Discipline  # p2000.enums, because just p2000 would create a circular dependency


class Unit:

    def __init__(self, **kwargs):
        self.capcode = kwargs.get("capcode", "")
        self.region = kwargs.get("region", Region.UNKNOWN)
        self.town = kwargs.get("town", "")
        self.function = kwargs.get("function", "")
        self.discipline = kwargs.get("discipline", Discipline.UNKNOWN)
