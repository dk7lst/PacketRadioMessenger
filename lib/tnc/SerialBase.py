import logging # https://docs.python.org/3/howto/logging.html
import serial # https://pyserial.readthedocs.io/en/latest/pyserial.html

# Base class for serial communication.
class SerialBase:
  def __init__(self, config, section):
    logging.debug("Init class SerialBase")
    self.ser = serial.Serial(port=config.getString(section, "device", "/dev/ttyUSB0"),
      baudrate=config.getInt(section, "devicebaud", 9600),
      bytesize=config.getInt(section, "bytesize", serial.EIGHTBITS),
      parity=config.getString(section, "parity", serial.PARITY_NONE),
      stopbits=config.getInt(section, "stopbits", serial.STOPBITS_ONE),
      xonxoff=config.getBool(section, "xonxoff", False),
      rtscts=config.getBool(section, "rtscts", False),
      dsrdtr=config.getBool(section, "dsrdtr", False),
      exclusive=config.getBool(section, "exclusive", True),
      timeout=None)
    logging.info('Serial port setting for port "%s": %s' % (self.ser.port, str(self.ser.get_settings())))

  def __del__(self):
    self.ser.close()

  def getLine(self):
    return self.ser.read_until(expected=b"\n", size=1000).decode("ascii")

  def sendLine(self, str):
    logging.debug('SerialBase:sendLine(): "%s"' % str)
    return self.ser.write(str.encode("ascii") + b"\r\n")

  def getFrame(self):
    return self.ser.read_until(expected=b"\xC0", size=2048)

  def sendFrame(self, frame):
    return self.ser.write(frame)
