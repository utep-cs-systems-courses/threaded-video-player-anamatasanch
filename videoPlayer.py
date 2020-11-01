#!/usr/bin/env python3

import threading
from threading import Thread, Lock
import cv2
import numpy as np
import base64
from Queue import ThreadyQueue
import time

# shared queue  
extractionQueue = ThreadyQueue(30)
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
        
        # initialize frame count
        count = 0
        
        #make sure queue has something
        time.sleep(1)
        
        #get first frame
        frame = extractionQueue.get()
        
        while frame != 'End':
            print(f'Displaying frame {count}')        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            count += 1
            frame = extractionQueue.get()

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
        
        while success:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)

            #encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)
                                    
            extractionQueue.put(image)
            count += 1
            success,image = vidcap.read()
            print(f'Reading frame {count} {success}')
            
        print('Frame extraction complete')
        extractionQueue.put('End')
        



extract = ExtractorThread(name='producer')
extract.start()

display = DisplayingThread(name='consumer')
display.start()

