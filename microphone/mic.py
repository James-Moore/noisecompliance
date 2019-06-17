import analyse
import numpy
import pyaudio


class Microphone:
    def __init__(self):
        self.pyaud = pyaudio.PyAudio()
        self.stream = self.pyaud.open( format = pyaudio.paInt16, channels = 1, rate = 44100, input_device_index = 2, input = True)

    def getDecible(self):
        rawsamps = self.stream.read(1024, False)
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        decible = analyse.loudness(samps)
        return decible