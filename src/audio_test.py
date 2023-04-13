import pyaudio
import speech_recognition as sr
from pprint import pprint
import time

p = pyaudio.PyAudio()

pprint(p.get_device_info_by_index(1))
for i in range(p.get_device_count()):
  info=p.get_device_info_by_index(i)
  print(f"[{info.get('index')}] {info.get('name')}")

def stt_callback(r_i, audio_data):
  transcript = r_i.recognize_whisper(audio_data, **r_whisper_kwargs)
  logging.info(f"Recognized phrase: \"{transcript}\"")

r_instance = sr.Recognizer()
mic = sr.Microphone(0)
with mic as source:
  result = r_instance.listen(source)
print("got it!")
val = r_instance.recognize_whisper(result)
print(val)



