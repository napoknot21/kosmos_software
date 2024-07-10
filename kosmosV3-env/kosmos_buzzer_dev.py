from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
from kosmos_melody import KMelody

BuzzerPin = 12

Buzz = TonalBuzzer(BuzzerPin, octaves = 4)

KMelody.playMelody(Buzz, KMelody.STARTING_MELODY)
