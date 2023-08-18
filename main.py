import pygame as pg

from game import Game


def main():
    pg.init()
    pg.display.set_caption('Py-k-mon')
    game = Game()
    game.reset_to_initial_state()
    game.loop()


if __name__ == '__main__':
    main()
