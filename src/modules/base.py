from multiprocessing import Process, Queue, Event
from queue import Empty
from getch import getch
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

keymap = {
  'r': 'RESET',
  's': 'TOGGLE_RECORD',
  'c': 'CALIBRATE_NOISE',
  'q': 'QUIT',
  'l': 'LIST',
  '[': 'LOWER_SENSITIVITY',
  ']': 'RAISE_SENSITIVITY',
}

def keyboard_in(exit_event: Event, input_queue: Queue, output_queue: List):
  while not exit_event.is_set():
    try:
      input_val = input_queue.get()
      signal = keymap.get(input_val.lower(), None)
      if signal == 'QUIT':
        logging.info(f"Exiting!")
        exit_event.set()
        return
      elif signal is not None:
        logging.info(f"Sending {signal} signal!")
        for q in output_queue:
          q.put(signal)
    except Empty:
      logging.debug('empty!')
