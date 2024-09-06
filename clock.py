from turtle import Turtle
import time
from settings import FONT

class Clock(Turtle):
    def __init__(self, position, max_seconds):
        super().__init__()
        self.color('black')
        self.start_time = None
        self.end_time = None
        self.max_time = max_seconds
        self.mins = 0
        self.secs = 0
        self.penup()
        self.hideturtle()
        self.goto(position)
        self.stopped = True
        self.update_clock()

    def start_clock(self):
        self.stopped = False
        self.start_time = time.time()
        self.end_time = self.start_time + self.max_time

    def stop_clock(self):
        self.stopped = True
        self.update_clock() # make sure to show stopped time

    def get_run_time(self):
        run_time = self.end_time - time.time()
        if run_time > 0:
            self.mins, self.secs = divmod(run_time, 60)
            return run_time
        else:
            self.mins, self.secs = 0, 0
            return 0

    def update_clock(self):
        self.clear()
        if not self.stopped:
            self.get_run_time()
        self.write(f'{self.mins:02.0f}:{self.secs:02.0f}', align='center', font=FONT)

    def reset_clock(self, max_seconds):
        self.start_time = None
        self.end_time = None
        self.max_time = max_seconds
        self.mins = 0
        self.secs = 0
