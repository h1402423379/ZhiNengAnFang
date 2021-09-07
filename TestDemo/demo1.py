import cv2
import _thread
import numpy as np
import matplotlib

class myclass:
    def __init__(self,cap):
        self.cap=cap
    def capture(self):
        while(True):
            ret,frame = self.cap.read()
            frame= cv2.flip(frame,1)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()




