class Blob(object):
    def __init__(self, estimation):
        self.estimation = estimation
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0

    def __str__(self):
        return "%s[(%d,%d) %dx%d]" % ( self.estimation, self.x, self.y, self.w, self.h ) 
