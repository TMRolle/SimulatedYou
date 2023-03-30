from multiprocessing import Event, Queue
from queue import Empty
import logging

import speech_recognition as sr
from time import sleep

r_whisper_kwargs = {

}

p_timeout = 30

def no_op(param):
  logging.warning("Recording already stopped!")

def run_stt(exit_event: Event, input_queue: Queue, device_index = None, output_queue: Queue):
  def stt_callback(r_i, audio_data):
    transcript = r_i.recognize_whisper(audio_data, **r_whisper_kwargs)
    logging.info(f"Recognized phrase: \"{transcript}\"")
    output_queue.put(transcript)
    
  r_instance = sr.Recognizer()
  stop_func = no_op
  with sr.Microphone() as source:
    r_instance.adjust_for_ambient_noise(source)
    is_recording = False
    while not exit_event.is_set():
      try:
        state=input_queue.get(timeout=0.1)
        if state == 'RECORD' and not is_recording:
          stop_func = r_instance.listen_in_background(source, stt_callback, phrase_timeout=p_timeout)
          is_recording = True
        elif state == 'STOP_RECORD' and is_recording:
          stop_func(True)
          is_recording = False
        elif state == 'CALIBRATE_NOISE':
          if is_recording:
            stop_func(True)
            r_instance.adjust_for_ambient_noise(source)
            stop_func = r_instance.listen_in_background(source, stt_callback, phrase_timeout=p_timeout)
          else:
            r_instance.adjust_for_ambient_noise(source)
      except Empty:
        pass
    stop_func(False)


