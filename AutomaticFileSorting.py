import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil



if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    text_event_handler = PatternMatchingEventHandler(patterns,ignore_patterns,ignore_directories,case_sensitive)
    


    def on_created(event):
        print(f"hey, {event.src_path} has been created!")      

        extension = os.path.splitext(event.src_path)[1].lower()
        if extension ==".txt" or extension==".pdf" or extension==".docx":
            shutil.move(event.src_path, r"C:\Users\Jugal\Downloads\Texto")
        elif extension ==".jpg" or extension==".jpeg" or extension==".png" or extension==".gif":
            shutil.move(event.src_path, r"C:\Users\Jugal\Downloads\Imageso")
        elif extension ==".mp4" or extension==".avi" or extension==".mkv" or extension==".wmv":
            shutil.move(event.src_path, r"C:\Users\Jugal\Downloads\VidsO")
        else:
            print("Unidentified extension")

    

  
    text_event_handler.on_created = on_created
    
    

    path = "C:\Users\Jugal\Downloads"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(text_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
