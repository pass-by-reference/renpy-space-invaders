init python:
  class Timer:
    def __init__(self, time):
      self.time = time
      self.st = None
      self.start = False
  
    def start_time(self,st):
      self.start = True
      self.st = st

    def has_time_elapsed(self,st):
      if(self.start):
        # 1. Check if current time is over allotted time
        # 2. Return time left
        return st > self.st + self.time, self.time-(st-self.st)
      else:
        # Timer did not start.
        return False, -1

  class DeltaTime:
    def __init__(self):
      self.dtime = None
      self.oldst = None

    def set_delta_time(self,st):
      """
      The driver for game speed. Calculates
      delta time
      """
      if self.oldst is None:
        self.oldst = st
      
      # Calculates delta time.
      self.dtime = st - self.oldst
      self.oldst = st