#!/usr/bin/env python3

import threading
from threading import Thread
import cv2
import numpy as np
import base64
from Queue import ThreadyQueue
import time

# shared queue  
queueSize = 10 
extractionQueue = ThreadyQueue(queueSize)
displayingQueue = ThreadyQueue(queueSize)

# filename of clip to load
global filename
filename = 'clip.mp4'

class DisplayingThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Display is running!")
        
        # initialize frame count
        count = 0
        
        #get first frame
        frame = displayingQueue.get()
        
        while frame != 'End':
            print(f'Displaying frame {count}')        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            count += 1
            frame = displayingQueue.get()

        print('Finished displaying all frames')
        # cleanup the windows
        cv2.destroyAllWindows()    

class ExtractorThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Extract is running!")
        
        # Initialize frame count 
        count = 0
        
        # open video file
        vidcap = cv2.VideoCapture(filename)
        
        # read first image
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        
        while success:                 
            extractionQueue.put(image)
            
            count += 1
            
            success,image = vidcap.read()
            
            print(f'Reading frame {count} {success}')
            
        print('Frame extraction complete')
        extractionQueue.put('End')
        
class GreyscalingThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Greyscale is running!")
        
        # Initialize frame count 
        count = 0
        
        # read first image
        colorFrame = extractionQueue.get()
        
        while colorFrame != 'End':
            print(f'Converting frame {count}')

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
                                    
            displayingQueue.put(grayscaleFrame)
            count += 1
            
            colorFrame = extractionQueue.get()
            
        print('Frame greyscaling complete')
        displayingQueue.put('End')


extract = ExtractorThread(name='producer')
extract.start()

greyscale = GreyscalingThread(name='greyscaling')
greyscale.start()

display = DisplayingThread(name='consumer')
display.start()

