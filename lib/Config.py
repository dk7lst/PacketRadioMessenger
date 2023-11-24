import configparser # https://docs.python.org/3/library/configparser.html

# Class for handling configuration (ini) file.
class Config(configparser.ConfigParser):
  def __init__(self, filename):
    super().__init__()
    self.read(filename)

  def getString(self, section, key, default=None):
    return self.get(section, key, fallback=default)

  def getInt(self, section, key, default=0):
    return self.getint(section, key, fallback=default)

  def getFloat(self, section, key, default=0.0):
    return self.getfloat(section, key, fallback=default)

  def getBool(self, section, key, default = False):
    return self.getboolean(section, key, fallback=default)

  def getCallsign(self):
    return self.getString("general", "callsign", "").upper()

  def getDefaultDestination(self):
    return self.getString("general", "DefaultDestination", "PRCHAT").upper()
