from turtle import Turtle
from settings import FONT, FONT_COLOR, SCORE_ALIGN


class Scoreboard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color = FONT_COLOR
        self.top_position = position
        self.penup()
        self.hideturtle()
        self.speed('fastest')
        self.score = 0
        self.level = 1
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(self.top_position)
        self.write(f'Score: {self.score} Level: {self.level}', font=FONT, align=SCORE_ALIGN)

    def show_message(self, msg):
        self.clear()
        self.goto((0, 0))
        self.write(msg, font=FONT, align=SCORE_ALIGN)

    def raise_score(self, *args):
        """Raise score either by 1 point for a found color pair or at the end of a level by the
        number of seconds left.
        """
        if not args:
            self.score += 1
        else:
            self.score += args[0]
        self.update_score()

    def raise_level(self):
        self.level += 1
        self.update_score()
