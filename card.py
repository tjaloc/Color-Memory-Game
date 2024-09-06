from turtle import Turtle
from settings import CARD_BG

class Card(Turtle):
    def __init__(self, position, color):
        super().__init__()
        self.shape('circle')
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.radius = self.get_radius()
        self.colors = {'front': color, 'back': CARD_BG}
        self.color(self.colors['back'])
        self.front = False
        self.speed('fastest')
        self.solved_status = False
        self.penup()
        self.goto(position)

    def set_solved(self):
        self.hideturtle()
        self.solved_status = True

    def flip(self):
        if self.front:
            self.color(self.colors['back'])
        else:
            self.color(self.colors['front'])
        self.front = not self.front

    def get_radius(self):
        """This is based on the assumption that self is a circle not an ellipse.
        The radius is calculated as half the distance between minimum x and maximum x.

        :return: float
        """
        X, _ = zip(*self.get_shapepoly())
        return (max(X) - min(X)) / 2
