import abc
import json
from subprocess import Popen, PIPE, run
from sys import exc_info


class Line:

    def __init__(self, line, **kwargs):
        r"""
        Create a new FLEX Line object with data from the given line.
        :param line: The line to extract the data from.
        :keyword timestamp: The timestamp to set to the object.
        :keyword monitorcode: The monitorcode to set to the object.
        :keyword message: The message to set to the object.
        """
        words = line.split()
        self.line = line
        self.timestamp = kwargs.get('timestamp', " ".join(words[1:2]))
        self.monitorcode = kwargs.get('monitorcode', words[5].strip("[]"))
        self.message = kwargs.get('message', " ".join(words[6:-1]))

    def __str__(self):
        """
        Create a string representation for a FLEX Line object, primarily used for debugging or logging purposes.
        :return: A String in the format:
            "@line = {0}\n" \
            "\t@message = {1}\n" \
            "\t@timestamp = {2}\n" \
            "\t@monitorcode = {3}"
        """
        return "@line = {0}\n" \
               "\t@message = {1}\n" \
               "\t@timestamp = {2}\n" \
               "\t@monitorcode = {3}".format(self.line, self.message, self.timestamp, self.monitorcode)


class Connection:
    
    COMMAND_RTLFM = ["rtl_fm", "-f", "169.65M", "-M", "fm", "-s", "22050", "-p", "83", "-g", "30"]
    COMMAND_MULTI = ["multimon-ng", "-q", "-a", "FLEX", "-t", "raw", "/dev/stdin"]
    COMMAND_KILL = ["killall", "-9", "rtl_fm"]

    def __init__(self):
        self.rtlfm_process = None
        self.multi_process = None
        self.stdout = None

    def open(self, **kwargs):
        """
        Open a new connection with the RTLSDR antenna.
        Spawns 2 processes:
            * rtl_fm - A process that runs an instance of rtl_fm that connects to the antenna.
            * multimon-ng - A process that runs an instance of multimon_ng that decodes the FLEX protocol messages.
        :keyword kill: To kill or not kill any current running processes, default is True.
        :return: Nothing
        """
        if kwargs.get("kill", False):
            self.kill()
        self.rtlfm_process = Popen(self.COMMAND_RTLFM, stdout=PIPE)
        self.multi_process = Popen(self.COMMAND_MULTI, stdin=self.rtlfm_process.stdout, stdout=PIPE)
        self.stdout = self.multi_process.stdout

    def kill(self):
        """
        Kill the connection with COMMAND_KILL.
        :return: Nothing
        """
        run(self.COMMAND_KILL)


class Reader:

    def __init__(self, **kwargs):
        self.blacklist_messages = self.load_config()["rtlsdr"]["blacklist"]["messages"]
        self.blacklist_monitorcodes = self.load_config()["rtlsdr"]["blacklist"]["monitorcodes"]
        self.encoding = kwargs.get("encoding", "utf-8")
        self.connection = None

    def attach(self, connection, kill=True):
        """
        Attach the given connection to the reader, calls the setup method and sets the instance variables.
        :param connection: The connection to attach.
        :param kill: To kill or not kill any current running processes, default is True.
        :return: Nothing
        :raises ConnectionError: Raised when a connection is already active or existent.
        """
        if self.connection is None:
            self.__setup_connection__(connection, kill)
        elif self.connection.stdout is None:
            self.__setup_connection__(connection, kill)
        else:
            raise ConnectionError("Connection is already active.").with_traceback(exc_info()[2])

    def detach(self):
        """
        Detach the current connection from the reader.
        Kills the connection and sets self.connection to None.
        :return: Nothing.
        """
        if self.connection is not None:
            self.connection.kill()
            self.connection = None

    def __setup_connection__(self, connection, kill):
        """
        Set the connection to the instance and open it.
        :param connection: The connection to set up.
        :param kill: To kill or not kill any current running processes.
        :return: Nothing
        """
        try:
            self.connection = connection
            connection.open(kill=kill)
            for line in self.connection.stdout:
                self.act(line)
        finally:
            self.detach()

    @abc.abstractmethod
    def act(self, line):
        """
        Act on the given line.
        :param line: The line to operate on.
        :return: Up to the user.
        """

    def decode_line(self, line, strip=True):
        """
        Decode the line from a byte-format to the format determined by self.encoding, default is "utf-8".
        :param line: The line to decode.
        :param strip: If the newlines should be striped from the line or not, default is True.
        :return: The decoded line in the given format.
        """
        decoded = line.decode(self.encoding)
        return decoded.rstrip() if strip else decoded

    def create_line(self, line, decode=True, strip=True):
        return Line(
            self.decode_line(line, strip=strip) if decode else line
        )

    def is_line_blacklisted(self, line):
        """
        Check to see if the given line is in the blacklist.
        The blacklist is checked for monitorcodes and messages.
        :param line: The line to check against the blacklist.
        :return: True if the line is blacklisted.
        """
        return self.is_monitorcode_blacklisted(line) or self.is_message_blacklisted(line)

    def is_monitorcode_blacklisted(self, line):
        """
        Check to see if the given line is in the blacklist.
        The blacklist is checked for monitorcodes.
        :param line: The line to check against the blacklist.
        :return: True if the line is blacklisted.
        """
        return Line(line).monitorcode in self.blacklist_monitorcodes

    def is_message_blacklisted(self, line):
        """
        Check to see if the given line is in the blacklist.
        The blacklist is checked for messages.
        :param line: The line to check against the blacklist.
        :return: True if the line is blacklisted.
        """
        return Line(line).message in self.blacklist_messages

    # noinspection PyMethodMayBeStatic
    def load_config(self):
        """
        Load the config file as JSON.
        :return: The config file as JSON.
        """
        with open('config.json') as file:
            return json.load(file)
