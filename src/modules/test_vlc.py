import time
from multiprocessing import Process, Event, Queue

from syvlc import play_output_file
from queue import Queue

if __name__ == '__main__':
    exit_event = Event()
    input_queue = Queue()
    output_queue = Queue()

    loop_file = "./1280.avi"    
    play_output_file(loop_file, input_queue, output_queue)
