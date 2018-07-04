import unittest

from p2000 import Region, Discipline


class TestEnumRegion(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        self.assertEqual(len(Region.all()), 26)
        self.assertEqual(Region.all()[0], Region.GRONINGEN)
        self.assertEqual(Region.all()[5], Region.GELDERLAND_NEO)
        self.assertEqual(Region.all()[10], Region.ZAANSTREEK_WATERLAND)
        self.assertEqual(Region.all()[15], Region.HOLLANDS_MIDDEN)
        self.assertEqual(Region.all()[20], Region.BRABANT_NOORD)
        self.assertEqual(Region.all()[-1], Region.KWC_KNRM)

    def test_match_by_id(self):
        self.assertEqual(Region.match_by_id("00"), Region.UNKNOWN)
        self.assertEqual(Region.match_by_id("05"), Region.TWENTE)
        self.assertEqual(Region.match_by_id("10"), Region.NOORD_HOLLAND)
        self.assertEqual(Region.match_by_id("15"), Region.HAAGLANDEN)
        self.assertEqual(Region.match_by_id("20"), Region.BRABANT_MIDWEST)
        self.assertEqual(Region.match_by_id("25"), Region.FLEVOLAND)
        self.assertEqual(Region.match_by_id("120"), Region.UNKNOWN)
        self.assertEqual(Region.match_by_id("@3fs"), Region.UNKNOWN)
        self.assertEqual(Region.match_by_id(1234), Region.UNKNOWN)
        self.assertEqual(Region.match_by_id([1, "2", (1, 2, 3)]), Region.UNKNOWN)


# noinspection SpellCheckingInspection
class TestEnumDiscipline(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        disciplines = Discipline.all()
        self.assertEqual(len(disciplines), 4)
        self.assertEqual(disciplines[0], Discipline.FIRE_DEPARTMENT)
        self.assertEqual(disciplines[1], Discipline.AMBULANCE)
        self.assertEqual(disciplines[2], Discipline.POLICE)
        self.assertEqual(disciplines[3], Discipline.KNRM)
        self.assertEqual(disciplines[-1], Discipline.KNRM)

    def test_match_by_id(self):
        self.assertEqual(Discipline.match_by_id("00"), Discipline.UNKNOWN)
        self.assertEqual(Discipline.match_by_id("01"), Discipline.FIRE_DEPARTMENT)
        self.assertEqual(Discipline.match_by_id("02"), Discipline.AMBULANCE)
        self.assertEqual(Discipline.match_by_id("03"), Discipline.POLICE)
        self.assertEqual(Discipline.match_by_id("04"), Discipline.KNRM)
        self.assertEqual(Discipline.match_by_id("120"), Discipline.UNKNOWN)
        self.assertEqual(Discipline.match_by_id("@3fs"), Discipline.UNKNOWN)
        self.assertEqual(Discipline.match_by_id(1234), Discipline.UNKNOWN)
        self.assertEqual(Discipline.match_by_id([1, "2", (1, 2, 3)]), Discipline.UNKNOWN)

    def test_is_match(self):
        self.assertEqual(Discipline.is_match("brandweer", Discipline.FIRE_DEPARTMENT), True)
        self.assertEqual(Discipline.is_match("alsdebrandweer", Discipline.FIRE_DEPARTMENT), True)
        self.assertEqual(Discipline.is_match("het brand weer", Discipline.FIRE_DEPARTMENT), False)

        self.assertEqual(Discipline.is_match("test ambulance test", Discipline.AMBULANCE), True)
        self.assertEqual(Discipline.is_match("test ghor+ test", Discipline.AMBULANCE), True)
        self.assertEqual(Discipline.is_match("test +ovd-g test", Discipline.AMBULANCE), True)
        self.assertEqual(Discipline.is_match("am bu lance", Discipline.AMBULANCE), False)

        self.assertEqual(Discipline.is_match("test politie test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test copi test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test sgbo test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test persinfo test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test persvoorlichter test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test voa test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("test bhv test", Discipline.POLICE), True)
        self.assertEqual(Discipline.is_match("po litie", Discipline.POLICE), False)
        self.assertEqual(Discipline.is_match("pers", Discipline.POLICE), False)
        self.assertEqual(Discipline.is_match("info", Discipline.POLICE), False)

        self.assertEqual(Discipline.is_match("test knrm test", Discipline.KNRM), True)
        self.assertEqual(Discipline.is_match("test kwc test", Discipline.KNRM), True)
        self.assertEqual(Discipline.is_match("test wc test", Discipline.KNRM), False)
        self.assertEqual(Discipline.is_match("test knmi test", Discipline.KNRM), False)

    def test_match(self):
        self.assertEqual(Discipline.match("Capcodes Brandweer"), Discipline.FIRE_DEPARTMENT)
        self.assertEqual(Discipline.match("Capcodes Brandweer+Roepnummers"), Discipline.FIRE_DEPARTMENT)
        self.assertEqual(Discipline.match("Capcodes Brandweer + Brugbediening"), Discipline.FIRE_DEPARTMENT)

        self.assertEqual(Discipline.match("Capcodes GHOR + OvD-G"), Discipline.AMBULANCE)
        self.assertEqual(Discipline.match("Capcodes Ambulance + GHOR"), Discipline.AMBULANCE)
        self.assertEqual(Discipline.match("Capcodes GHOR+OvD-G +Lifeguards"), Discipline.AMBULANCE)
        self.assertEqual(Discipline.match("Capcodes Ambulance + OvD-G + GHOR"), Discipline.AMBULANCE)

        self.assertEqual(Discipline.match("Capcodes Politie"), Discipline.POLICE)
        self.assertEqual(Discipline.match("Capcodes VOA + BHV"), Discipline.POLICE)
        self.assertEqual(Discipline.match("Capcodes Persvoorlichter + Persinfo"), Discipline.POLICE)
        self.assertEqual(Discipline.match("Capcodes Functionris COPI+SGBO + Persinfo"), Discipline.POLICE)

        self.assertEqual(Discipline.match("Capcodes KNRM"), Discipline.KNRM)
        self.assertEqual(Discipline.match("Capcodes KWC - KNRM"), Discipline.KNRM)
        self.assertEqual(Discipline.match("Capcodes Brugbediening + KNRM"), Discipline.KNRM)


if __name__ == '__main__':
    unittest.main()
