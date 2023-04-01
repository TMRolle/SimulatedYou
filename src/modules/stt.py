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

def no_op(param):
  logging.warning("Recording already stopped!")

def run_stt(exit_event: Event, input_queue: Queue, output_queue: Queue, device_index = None):
  # Set up callback function
  def stt_callback(r_i, audio_data):
    with open("input.wav", "wb") as wav_file:
      wav_file.write(audio_data.get_wav_data())
    transcript = r_i.recognize_whisper(audio_data, **r_whisper_kwargs)
    transcript = transcript.strip()
    if transcript not in ["", "Thank you."]:
      logging.info(f"Recognized phrase: \"{transcript}\"")
      output_queue.put(transcript)
  # Initialize recognizer
  r = sr.Recognizer()
  r.dynamic_energy_threshold = False
  stop_func = no_op
  mic = sr.Microphone()
  with mic as source: r.adjust_for_ambient_noise(source)
  r.energy_threshold = 300
  is_recording = False
  # Main logic loop
  while not exit_event.is_set():
    try:
      state=input_queue.get(timeout=0.1)
      if state == 'TOGGLE_RECORD':
        if not is_recording:
          stop_func = r.listen_in_background(source, stt_callback)
          logging.info("Audio recording started")
          is_recording = True
        elif is_recording:
          stop_func(True)
          logging.info("Audio recording stopped")
          is_recording = False
      elif state == 'CALIBRATE_NOISE':
        logging.info("Calibrating noise level...")
        if is_recording:
          stop_func(True)
          with mic as source: r.adjust_for_ambient_noise(source)
          stop_func = r.listen_in_background(source, stt_callback)
        else:
          with mic as source: r.adjust_for_ambient_noise(source)
        logging.info("Audio calibration complete.")
      elif state == 'LOWER_SENSITIVITY':
        logging.info(f"Raising energy threshold from {r.energy_threshold} to {r.energy_threshold + 10}")
        r.energy_threshold+=10
      elif state == 'RAISE_SENSITIVITY':
        logging.info(f"Lowering energy threshold from {r.energy_threshold} to {r.energy_threshold - 10}")
        r.energy_threshold-=10

    except Empty:
      pass
    # End main logic loop
  logging.info("Terminating speech module")
  stop_func(False)
  logging.info("Speech module terminated")


