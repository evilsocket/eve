from . import t

class Frame(object):
    def __init__(self, data):
        self.timestamp = t.curr_millis()
        self.data = data

    def get_blob_subframe_data(self,blob):
        return self.data[ blob.y - 10: blob.y + blob.h, blob.x: blob.x + blob.w ]

