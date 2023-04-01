from multiprocessing import Event, Queue
import vlc
import time
import queue
vlc.Instance('--no-xlib', '--quiet', '-I', 'dummy', '--plugin-path=/usr/lib/vlc/plugins')    

def play_output_file(loop_file, input_queue, output_queue):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(loop_file)
    player.set_media(media)
    player.play()

    while True:
        try:
            # Wait for a new file to play
            output_file = input_queue.get(timeout=1)

            # Stop playing the loop file and play the new file
            player.stop()
            media = instance.media_new(output_file)
            player.set_media(media)
            player.play()

            # Wait for the new file to finish playing
            while player.get_state() != vlc.State.Ended:
                time.sleep(0.1)

            # Write to the output queue to signal that the file has finished playing
            output_queue.put(output_file)

            # Start playing the loop file again
            media = instance.media_new(loop_file)
            player.set_media(media)
            player.play()
        except queue.Empty:
            pass

    # Release resources                                                                                            
    player.stop()
    player.release()
