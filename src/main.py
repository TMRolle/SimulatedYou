import argparse
from getch import getch
from time import sleep
from multiprocessing import Process, Queue, Event, SimpleQueue, Manager
from modules.base import keyboard_in

def main_func(args):
  with Manager() as manager:
    exit_event = manager.Event()
    my_test_module_in = manager.Queue()
    my_test_module_out = manager.Queue()
    my_test_module_proc = Process(target=keyboard_in, args=(exit_event, my_test_module_in, my_test_module_out))
    my_test_module_proc.start()
    while not exit_event.is_set():
      val = getch()
      my_test_module_in.put(val, block=False)
      if val in ['q', 'Q']:
        exit_event.set()
        print('Waiting for child processes to exit...')
        my_test_module_proc.join()
        print('Child processes done exiting!')
        return

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  args = parser.parse_args()
  main_func(args)
