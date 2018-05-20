import sys
sys.path.append("eve")

from argparse import ArgumentParser
import os
import cv2
import logging

from eve.grabbers import CameraGrabber
from eve.isolators import FaceIsolator, EyeIsolator
from eve.manager import Eve
from eve.training import check_dir, save_unlabeled_data
from eve.t import curr_millis

# https://github.com/Hironsan/BossSensor/blob/master/camera_reader.py
# https://github.com/gagolucasm/Classify-Real-Time-Desktop
# https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/

def draw_blobs( frame, blobs ):
    for b in blobs:
        cv2.rectangle( frame.data, (b.x, b.y), (b.x+b.w, b.y+b.h), (0, 255, 0), 2)
        cv2.putText( frame.data, b.estimation, (b.x,b.y-5), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0,255,0))

parser = ArgumentParser()
parser.add_argument("--data-path", dest="datapath", default='./evedata',help="Data path.", metavar="FOLDER")
parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="Enable debug output.")
args = parser.parse_args()

fmt = '[%(asctime)s] %(levelname)s - %(message)s'

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format=fmt)
else:
    logging.basicConfig(level=logging.INFO, format=fmt)

logging.info( "Eve v%s started." % Eve.VERSION )
logging.info( "Using datapath %s" % args.datapath )

check_dir(args.datapath)

cam = CameraGrabber(0)
w, h = cam.get_frame_dimensions()
isolators = [ FaceIsolator(), EyeIsolator() ]

logging.info( "Capturing at %dx%d, press 'q' to quit." % ( w, h ) )

prev = 0

while True:
    now = curr_millis()
    frame = cam.get_frame()

    if frame is None:
        logging.warning("Error reading frame.")
        continue

    # Isolate blobs in the frame
    blobs = []
    for i in isolators:
        blobs += i.isolate(frame)

    # TODO: Remove overlapping blobs.
    # TODO: Use TensorFlow model to predict labels for blobs.

    # Put unknown blobs in the training queue
    if len(blobs):
        # dump samples every 200ms
        snow = curr_millis()
        since_last = snow - prev
        if since_last >= 200:
            prev = snow
            save_unlabeled_data( args.datapath, frame, blobs ) 

        draw_blobs( frame, blobs )

    end = curr_millis()
    taken = end - now
    fps = 1000.0 / taken

    cv2.putText(frame.data, "fps: %.2f" % fps, (520,460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255))
    cv2.imshow("Eve", frame.data)

    if cv2.waitKey(1) & 0xFF == ord("q"):break



