#!/usr/bin/env python3

import threading
from threading import Thread, Lock
import cv2
import numpy as np
import base64
import queue
import time

# shared queue  
extractionQueue = queue.Queue()
queueSize = 30

# filename of lip to load
global filename
filename = 'clip.mp4'
lock = Lock()
event = threading.Event()

class DisplayingThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Display is running!")
        #make sure queue has something
        time.sleep(1)
        # initialize frame count
        count = 0
        
        not_empty = True
        while not_empty and not event.is_set():
            lock.acquire()
            if not extractionQueue.empty():
                # get the next frame
                frame = extractionQueue.get()
                lock.release()

                print(f'Displaying frame {count}')        

                # display the image in a window called "video" and wait 42ms
                # before displaying the next frame
                cv2.imshow('Video', frame)
                if cv2.waitKey(42) and 0xFF == ord("q"):
                    break

                count += 1
            elif event.is_set():
                #there will be no more frames
                lock.release()
                #it is empty for sure
                not_empty = False
            else:
                lock.release()
        print('Finished displaying all frames')
        # cleanup the windows
        cv2.destroyAllWindows()

    

class ExtractorThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        # Initialize frame count 
        count = 0
        
        # open video file
        vidcap = cv2.VideoCapture(filename)
        
        # read first image
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        #extractionQueue.put(image)
        
        while success:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)

            #encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)
                
            #if len(extractionQueue)>queueSize:
                    
            lock.acquire()
            # add the frame to the buffer
            if extractionQueue.qsize()<queueSize:
                extractionQueue.put(image)
                count += 1
                success,image = vidcap.read()
                print(f'Reading frame {count} {success}')
            lock.release()
            
        print('Frame extraction complete')
        event.set()
            



extract = ExtractorThread(name='producer')
extract.start()

display = DisplayingThread(name='consumer')
display.start()

