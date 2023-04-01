import argparse
from getch import getch
from time import sleep
from multiprocessing import Process, Queue, Event, SimpleQueue, Manager
import multiprocessing
from modules.base import keyboard_in
from modules.stt import run_stt
from modules.tts import run_tts
from modules.run_wav2lip import run_wav2lip
from modules.new_alpaca import run_alpaca_damn_you
from modules.syvlc import play_output_file
import logging

logging.basicConfig(level=logging.INFO)

def main_func(args):
  with Manager() as manager:
    context = multiprocessing.get_context('spawn')
    exit_event = manager.Event()

    keyboard_in_queue = manager.Queue()

    stt_in_queue = manager.Queue()
    stt_out_queue = manager.Queue()
    alpaca_out_queue = manager.Queue()
    tts_out_queue = manager.Queue()
    wav2lip_out_queue = manager.Queue()
    player_out_queue = manager.Queue()

    keyboard_interpreter = context.Process(target=keyboard_in, args=(exit_event, keyboard_in_queue, [stt_in_queue]))
    stt_process = context.Process(target=run_stt, args=(exit_event, stt_in_queue, stt_out_queue))
    alpaca_process = context.Process(target=run_alpaca_damn_you, args=(exit_event, stt_out_queue, alpaca_out_queue))
    tts_process = context.Process(target=run_tts, args=(exit_event, alpaca_out_queue, tts_out_queue))
    wav2lip_process = context.Process(target=run_wav2lip, args=(exit_event, tts_out_queue, wav2lip_out_queue))
    vlc_process = context.Process(target=play_output_file, args=(exit_event, wav2lip_out_queue, player_out_queue))


    keyboard_interpreter.start()
    stt_process.start()
    alpaca_process.start()
    tts_process.start()
    wav2lip_process.start()
    vlc_process.start()

    while not exit_event.is_set():
      val = getch()
      keyboard_in_queue.put(val, block=False)
      sleep(0.01)

    stt_process.join()
    keyboard_interpreter.join()
    alpaca_process.join()
    tts_process.join()
    wav2lip_process.join()
    vlc_process.join()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  args = parser.parse_args()
  main_func(args)
