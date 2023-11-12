import lib.TNC

# Class for messenger application protocol implementation.
class Protocol:
  def __init__(self, config):
    self.tnc = lib.TNC.TNC(config)

  def sendMessage(self, msgtext):
    return self.tnc.sendMessage(msgtext)
