from TTS.api import TTS
from pprint import pprint
from playsound import playsound

tts=TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", gpu=True)

tts.tts_to_file("This is only a test", speaker_wav="input.wav", language="en", file_path="output.wav")
playsound("output.wav")
