import rtlsdr


class MyReader(rtlsdr.Reader):

    def act(self, raw):
        print(str(self.create_line(raw)))


connection = rtlsdr.Connection()
reader = MyReader()
reader.attach(connection)
