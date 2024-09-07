from turtle import Screen
from time import sleep
import random
import colorsys
from math import ceil, sqrt
import os

from settings import *
from card import Card
from scoreboard import Scoreboard
from clock import Clock


def is_card_clicked(click_pos, card) -> bool:
    center_x, center_y = card.pos()
    x, y = click_pos
    radius = card.radius
    return (x - center_x)**2 + (y - center_y)**2 <= radius**2

def flip_card(x, y):
    unsolved_deck = [card for card in game.deck if not card.solved_status and card.isvisible()]
    for card in unsolved_deck:
        if is_card_clicked((x, y), card):

            # Is current card the 2nd of a pair?
            if card in game.pair:
                game.pair.remove(card)
            else:
                game.pair.append(card)
                card.flip()

            if len(game.pair) == 2:
                game.update()
                sleep(1/2)
                if pair_solved():
                    for c in game.pair:
                        c.set_solved()
                    scoreboard.raise_score()
                clear_pair()
            return

def new_game():
    global scoreboard, clock, game

    game.clearscreen()
    scoreboard = Scoreboard((0, QUADRANT_H - 50))
    clock = Clock((-QUADRANT_W + 50, QUADRANT_H - 50), BASE_TIME * scoreboard.level)
    game_setup()

def create_deck():
    n = START_COLOR_NUM + scoreboard.level
    colors = create_colors(n)
    return [Card((0, 0), colors[i // 2]) for i in range(2 * n)]

def place_deck():
    n = len(game.deck)
    gap = 10
    game.deck = random.sample(game.deck, n)
    rows = ceil(sqrt(n))
    cols = ceil(n / rows)
    distance = game.deck[0].radius * 2 + gap

    x0 = -((cols * distance) // 2 - gap)
    y0 = (rows * distance) // 2 - gap
    for i, card in enumerate(game.deck):
        x = x0 + (i % rows * distance)
        y = y0 - (i // rows * distance)
        card.goto((x, y))

    flip_deck()

def pair_solved()->bool:
    return len(game.pair) == 2 and game.pair[0].colors['front'] == game.pair[1].colors['front']

def clear_pair():
    for card in game.pair:
        card.flip()
    game.pair = []

def create_colors(n, saturation=85, vibrance=75):
    colors = []
    for i in range(n):
        hue = round(i / n * 360)
        (r, g, b) = colorsys.hsv_to_rgb(hue / 360, saturation / 100, vibrance / 100)

        # Convert the RGB tuple to hexadecimal
        hex_color = f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
        colors.append(hex_color)
    return colors

def is_level_completed() -> bool:
    return all([card.solved_status for card in game.deck])

def new_level():
    global scoreboard, clock

    if scoreboard.score > game.highscore:
        set_highscore(scoreboard.score)
        scoreboard.show_message(f'New highscore! {scoreboard.score}')
        sleep(1)

    game.clearscreen()
    scoreboard.level += 1
    scoreboard.update_score() # go back to default position showing score (not message)
    clock.reset_clock(BASE_TIME + 3 * scoreboard.level)
    game_setup()

def game_setup():
    global clock

    game.tracer(0)
    game.deck = create_deck()
    place_deck()
    game.pair = []
    game.update()
    game.highscore = get_highscore()

    # time to memorize the deck
    sleep(3)
    flip_deck()
    clock.start_clock()

    # interactivity
    game.listen()
    game.onclick(flip_card)

def flip_deck():
    for card in game.deck:
        card.flip()

def get_highscore():
    file = 'Highscore.txt'
    if os.path.exists(file):
        with open(file, 'r') as f:
            hs = f.read()
            return int(hs.strip())
    else:
        return 0

def set_highscore(score):
    file = 'Highscore.txt'
    with open(file, 'w') as f:
        f.write(f'{score}')


if __name__ == "__main__":
    game = Screen()
    game.title('Color Memory')
    game.bgcolor(SCENE_BG)
    game.setup(width=QUADRANT_W * 2, height=QUADRANT_H*2)

    scoreboard = Scoreboard((0, QUADRANT_H - 50))
    clock = Clock((0, - QUADRANT_H + 50), BASE_TIME * scoreboard.level)
    game_setup()

    game_is_on = True
    clock.start_clock()

    while game_is_on:
        game.update()
        clock.update_clock()

        if clock.get_run_time() <= 0:
            clock.stop_clock()
            game.clearscreen()
            scoreboard.show_message(f"Time is up.\n\nYou're final score is {scoreboard.score}.")
            sleep(2)
            game_is_on = False
        else:
            if is_level_completed():
                clock.stop_clock()
                points = int(clock.mins * 60 + clock.secs)
                scoreboard.raise_score(points)
                game.clearscreen()
                scoreboard.show_message(f'Level complete')
                sleep(2)

                if scoreboard.level < MAX_LEVELS:
                    new_level()

    game.clearscreen()
    scoreboard.show_message('GOOD BYE')
    game.mainloop()


# ToDo:
#  show highscore
#  quit game button
#  cards in center
#  allow to start a new game
