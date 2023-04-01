from TTS.api import TTS
from pprint import pprint
from playsound import playsound
from queue import Empty
from multiprocessing import Event, Queue

def run_tts(exit_event: Event, input_queue: Queue, output_queue: Queue):
  tts=TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", gpu=True)

  while not exit_event.is_set():
    try:
      text_in = input_queue.get(timeout=0.1)
      tts.tts_to_file(text_in, speaker_wav="input.wav", language="en", file_path="output.wav")
      playsound("output.wav")
    except Empty:
      pass



