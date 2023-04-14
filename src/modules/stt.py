from multiprocessing import Event, Queue
from queue import Empty
import logging
import speech_recognition as sr
from time import sleep

logging.basicConfig(level=logging.INFO)

r_whisper_kwargs = {
#  'model': 'small',
}

p_timeout = 30

def run_stt(exit_event: Event, speech_lock: Event, input_queue: Queue, output_queue: Queue, device_index = None):
  # Set up callback function
  speech_lock.set()
  def stt_callback(r_i, audio_data):
    if speech_lock.is_set():
      return
    with open("input.wav", "wb") as wav_file:
      wav_file.write(audio_data.get_wav_data())
    transcript = r_i.recognize_whisper(audio_data, **r_whisper_kwargs)
    transcript = transcript.strip()
    if transcript not in ["", "Thank you."]:
      logging.info(f"Recognized phrase: \"{transcript}\"")
      output_queue.put(transcript)
      speech_lock.set()
  # Initialize recognizer
  r = sr.Recognizer()
  r.dynamic_energy_threshold = False
  r.pause_threshold = 1.2
  mic = sr.Microphone()
  with mic as source: r.adjust_for_ambient_noise(source)
  stop_func = r.listen_in_background(source, stt_callback)
  r.energy_threshold = 400
  # Main logic loop
  while not exit_event.is_set():
    try:
      state=input_queue.get(timeout=0.1)
      if state == 'TOGGLE_RECORD':
        if speech_lock.is_set():
          logging.info("Audio recording started")
          speech_lock.clear()
        elif not speech_lock.is_set():
          speech_lock.set()
          logging.info("Audio recording stopped")
      elif state == 'CALIBRATE_NOISE':
        logging.info("Calibrating noise level...")
        speech_lock.set()
        with mic as source: r.adjust_for_ambient_noise(source)
        speech_lock.clear()
        logging.info("Audio calibration complete.")
      elif state == 'LOWER_SENSITIVITY':
        logging.info(f"Raising energy threshold from {r.energy_threshold} to {r.energy_threshold + 10}")
        r.energy_threshold+=10
      elif state == 'RAISE_SENSITIVITY':
        logging.info(f"Lowering energy threshold from {r.energy_threshold} to {r.energy_threshold - 10}")
        r.energy_threshold-=10
      elif state == 'STOP_RECORD':
        speech_lock.set()
        logging.info("Audio recording stopped")
        speech_lock.set()
      elif state == 'START_RECORD':
        speech_lock.clear()
        logging.info("Audio recording started")
        speech_lock.clear()


    except Empty:
      pass
    # End main logic loop
  logging.info("Terminating speech module")
  stop_func(True)
  logging.info("Speech module terminated")


