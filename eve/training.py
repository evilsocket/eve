import os
import cv2
import logging

def check_dir(path):
    if not os.path.exists(path):
        logging.info("Creating folder %s" % path)
        os.makedirs(path)

def save_unlabeled_data( path, frame, blobs ):
    path = os.path.join( path, 'training', 'unlabeled' )
    check_dir(path)
    for b in blobs:
        bpath = os.path.join( path, b.estimation )
        check_dir(bpath)
        bfile = os.path.join( bpath, "%d.jpg" % frame.timestamp )       
        logging.debug("Saving unlabeled blob to %s" % bfile)
        cv2.imwrite( bfile, frame.get_blob_subframe_data(b) )

        

