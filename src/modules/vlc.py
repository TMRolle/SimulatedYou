import multiprocessing
import vlc

def play_output_file(exit_event: Event, input_queue: Queue, output_queue: Queue, loop_video):
    # Create a new instance of the VLC player
    player = vlc.MediaPlayer()
    player.set_media(loop_file)
    player.play()
    
    while not exit_event.is_set():
        try:
            # Try to get an update to the output file from the queue
            video_file = input_queue.get(block=True, timeout=1)
            player.set_media(video_file)
            player.play()
            # Process the update as needed (e.g., update the output file)
        except multiprocessing.queues.Empty:
            # If there are no updates in the queue, continue the loop
            continue

    # Once the loop is exited, stop playing the output file and release resources
    player.stop()
    player.release()
