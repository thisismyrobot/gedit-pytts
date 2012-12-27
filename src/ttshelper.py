import pyttsx
import thread


class TTSHelper(object):
    """ A helper for TTS in Python code.
    """
    def __init__(self, rate):
        # setup
        self._ttsengine = pyttsx.init()
        self._ttsengine.setProperty('rate', rate)
        self.say("Python Dev TTS loaded")

    def say(self, text):
        self._ttsengine.say(text)
        self._ttsengine.runAndWait()
