from multiprocessing import Event, Queue
import vlc
import time
import queue

import logging
logging.basicConfig(level=logging.INFO)

logging.info('VLC is starting')
vlc.Instance('--no-xlib', '--quiet', '-I', 'dummy', '--plugin-path=/usr/lib/vlc/plugins')    

logging.info('VLC done starting')
output_file="output_vid.mp4"
loop_file="face.jpg"

def play_output_file(exit_event, input_queue, output_queue):
    logging.info('Background VLC process running!!!')
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(loop_file)
    player.set_media(media)
    player.play()

    while not exit_event.is_set():
        try:
            # Wait for a new file to play
            signal = input_queue.get(timeout=0.1)
            logging.info('playing vidya!!!')
            # Stop playing the loop file and play the new file
            player.stop()
            media = instance.media_new(output_file)
            player.set_media(media)
            player.play()

            # Wait for the new file to finish playing
            while player.get_state() != vlc.State.Ended:
                time.sleep(0.1)

            # Write to the output queue to signal that the file has finished playing
            output_queue.put("FINISHED")

            # Start playing the loop file again
            media = instance.media_new(loop_file)
            player.set_media(media)
            player.play()
        except queue.Empty:
            pass

    # Release resources                                                                                            
    player.stop()
    player.release()
