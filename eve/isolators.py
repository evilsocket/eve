from blob import Blob

class Isolator(object):
    def get_estimation_id(self):
        raise NotImplementedError()

    def isolate(self, frame):
        raise NotImplementedError()

import cv2

class HaarIsolator(Isolator):
    def __init__(self, min_size, cascade_path):
        self.path = cascade_path
        self.cascade = cv2.CascadeClassifier(self.path)
        self.min_size = min_size
        
    def isolate(self,frame):
        blobs = []
        grayscale  = cv2.cvtColor( frame.data, cv2.COLOR_BGR2GRAY )
        rectangles = self.cascade.detectMultiScale( grayscale, scaleFactor=1.2, minNeighbors=3, minSize=self.min_size)
        
        for r in rectangles:
            b = Blob( self.get_estimation_id() ) 
            b.x, b.y = r[0:2]
            b.w, b.h = r[2:4]
            blobs.append(b)

        return blobs

class FaceIsolator(HaarIsolator):
    def __init__(self):
        super(FaceIsolator, self).__init__( (30,30), '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

    def get_estimation_id(self):
        return "human-face"







