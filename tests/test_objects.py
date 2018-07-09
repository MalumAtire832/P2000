import unittest

from p2000 import Unit, Discipline, Region


# noinspection SpellCheckingInspection
class TestObjectUnit(unittest.TestCase):

    def setUp(self):
        pass

    def test_unit_custom(self):
        unit1 = Unit(
            capcode="1234",
            region=Region.GRONINGEN,
            town="mTown",
            function="testcase",
            discipline=Discipline.FIRE_DEPARTMENT
        )
        self.assertEqual(unit1.capcode, "1234")
        self.assertEqual(unit1.region, Region.GRONINGEN)
        self.assertEqual(unit1.town, "mTown")
        self.assertEqual(unit1.function, "testcase")
        self.assertEqual(unit1.discipline, Discipline.FIRE_DEPARTMENT)

    def test_unit_normal(self):
        unit2 = Unit()
        self.assertEqual(unit2.capcode, "")
        self.assertEqual(unit2.region, Region.UNKNOWN)
        self.assertEqual(unit2.town, "")
        self.assertEqual(unit2.function, "")
        self.assertEqual(unit2.discipline, Discipline.UNKNOWN)


if __name__ == '__main__':
    unittest.main()
