import cv2 as cv
from queue import Empty
from multiprocessing import Event, Queue

def run_cv2(exit_event, input_queue, output_queue):
    capture_dev=cv.VideoCapture(0)
    while not exit_event.is_set():
        ret, frame = capture_dev.read()
        if ret:
            try:
                msg = input_queue.get(timeout=0.1)
                cv.imwrite('face.jpg', frame)
            except Empty:
                pass
        cv.waitKey(1)
