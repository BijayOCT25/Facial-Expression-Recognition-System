import datetime

class FPS(object):
    """description of class"""

    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        #start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        #stop the timer
        self._end = datetime.datetime.noe()

    def update(self):
        #increase the total frames examined during the interval
        self._numFrames += 1

    def elapsed(self):
        #retutn total time elapsed
        return (self.end - self.start).total_seconds()

    def fps(self):
        return self._numFrames / self.elapsed()




