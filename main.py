import p2000.rtlsdr as rtlsdr
from p2000.rtlsdr import AbstractReader
from p2000 import Region
from pprint import pprint


regions = Region.all()
# print(regions[0])
# print(regions[-0])


# class MyReader(AbstractReader):
#
#     def act(self, raw):
#         line = self.create_line(raw)
#         if self.is_line_blacklisted(line):
#             print("== LINE IS BLACKLISTED ==")
#         else:
#             print(str(line))
#
#
# connection = rtlsdr.Connection()
# reader = MyReader()
# reader.attach(connection)
