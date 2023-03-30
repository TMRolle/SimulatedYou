from multiprocessing import Process, Queue, Event
from queue import Empty
from getch import getch
from typing import List

keymap = {
    'r': 'RESET'
}

def keyboard_in(exit_event: Event, input_queue: Queue, output_queue: Queue):
  while not exit_event.is_set():
    try:
      input_val = input_queue.get()
      if input_val is not None:
        print(f"You pressed {input_val}!")
      if input_val in ['q', 'Q']:
        print(f"Exiting!")
        exit_event.set()
        return
      elif input_val in keymap:
        output_queue.put(keymap[input_val])
      
    except Empty:
      print('empty!')


  
