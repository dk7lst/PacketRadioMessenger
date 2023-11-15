import _thread
import queue # https://docs.python.org/3/library/queue.html
import logging # https://docs.python.org/3/howto/logging.html
import lib.tnc

# Class for messenger application protocol implementation.
class Protocol:
  def __init__(self, config, msgpad):
    self.config = config
    self.msgpad = msgpad
    self.txMsgQueue = queue.SimpleQueue()
    self.rxMsgQueue = queue.SimpleQueue()
    self.tnc = lib.tnc.TNC(config, self.txMsgQueue, self.rxMsgQueue)
    _thread.start_new_thread(self.ProtocolThread, ())

  def sendMessage(self, msgtext):
    msg = {"id": lib.newId(), "to": "TO", "from": self.config.getCallsign(), "via": [], "text": msgtext}
    self.msgpad.addMessage(msg, True)
    msg["payload"] = b"MSG " + msgtext.encode("utf-8") # TODO: Msg-Encoding!
    self.txMsgQueue.put(msg)

  def __del__(self, config, section):
    pass # TODO: Shutdown thread!

  # Process protocol events like incoming messages, resent-timer etc..
  def ProtocolThread(self):
    logging.debug("Protocol: ProtocolThread()")
    while True:
      msg = self.rxMsgQueue.get()
      msg["id"] = lib.newId()
      logging.debug("Protocol: ProtocolThread(): Processing " + str(msg))
      msg["text"] = msg["payload"].decode("utf-8") # TODO: Msg-Encoding!
      self.msgpad.addMessage(msg, False)
