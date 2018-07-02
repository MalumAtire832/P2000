import p2000.utils as utils
from p2000.rtlsdr import Connection, AbstractReader
from pprint import pprint


class MyReader(AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


connection = Connection()
reader = MyReader()
reader.attach(connection)


