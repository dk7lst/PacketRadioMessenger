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
      timeout=None)

  def __del__(self):
    self.ser.close()

  def getLine(self):
    return self.ser.read_until(expected=b"\n", size=1000).decode("ascii")

  def getFrame(self):
    return self.ser.read_until(expected=b"\xC0", size=1000).decode("ascii")
