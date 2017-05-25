from frame import Frame

class Grabber(object):
    # return (width,height)
    def get_frame_dimensions(self):
        raise NotImplementedError()

    # return the current frame object
    def get_frame(self):
        raise NotImplementedError()

    def start():
        pass

    def stop():
        pass

import cv2

class CameraGrabber(Grabber):
    def __init__(self,dev):
        self.cam   = cv2.VideoCapture(dev)

    def get_frame_dimensions(self):
        width = self.cam.get( cv2.cv.CV_CAP_PROP_FRAME_WIDTH )
        height = self.cam.get( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT )
        return (width,height)

    def get_frame(self):
        ok, frame = self.cam.read()
        if ok:
            return Frame(frame)
        else:
            return None
