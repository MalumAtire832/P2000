import rtlsdr


class MyReader(rtlsdr.AbstractReader):

    def act(self, raw):
        line = self.create_line(raw)
        if self.is_line_blacklisted(line):
            print("== LINE IS BLACKLISTED ==")
        else:
            print(str(line))


connection = rtlsdr.Connection()
reader = MyReader()
reader.attach(connection)
