import sys
from django.shortcuts import render
from mysqlx import FilterableStatement

import pygame as pg
from pygame.locals import *

import numpy as np

pg.init()
pg.font.init()

font = pg.font.SysFont("Aerial",30)

clock = pg.time.Clock()

display = pg.display.set_mode((500, 500))

game_a = np.full((50,50),False)
prev_game_a = np.full((50,50),False)

running = True
sim_running = False

finished = False

generation = 0

black = 0, 0, 0
white = 255, 255, 255

def set_tile(pos):
    x, y = pos[0], pos[1]

    if game_a[y//10, x//10]:
        game_a[y//10, x//10] = False
        pg.draw.rect(display, black, pg.Rect(x,y, 10, 10))
    else:
        game_a[y//10, x//10] = True
        pg.draw.rect(display, white, pg.Rect(x,y, 10, 10))

def run_simulation():
    global generation, game_a, prev_game_a, sim_running

    while not np.array_equal(prev_game_a, game_a) and sim_running:
        for y, row in enumerate(prev_game_a):
            for x, cell in enumerate(row):
                if cell:
                    neighbours = prev_game_a[y-1:y+2,x-1:x+2]

                    if np.count_nonzero(neighbours)-1 == 2 or np.count_nonzero(neighbours)-1 == 3:
                        game_a[y,x] = True

        for y, row in enumerate(prev_game_a):
            for x, cell in enumerate(row):
                if not prev_game_a[y,x]:
                    neighbours = prev_game_a[y-1:y+2,x-1:x+2]
                    
                    if np.count_nonzero(neighbours) == 3:
                        game_a[y,x] = True

        generation += 1

        display.fill(black)

        for y, row in enumerate(game_a):
            for x, cell in enumerate(row):
                if game_a[y,x]:
                    pg.draw.rect(display, white, pg.Rect(x*10, y*10, 10, 10))

        prev_game_a,game_a = game_a,np.full((50,50),False)

        text_surface = font.render(f"Generation: {generation}",False,white)
        display.blit(text_surface, (0,0))

        pg.display.flip()
        clock.tick(5)

    


def main():
    global running, prev_game_a, game_a, sim_running

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()

                rounded_mouse_pos = tuple(map(lambda x : 10*round(x/10),mouse_pos))
                    
                if rounded_mouse_pos[0] <= 490 and rounded_mouse_pos[1] <= 490:
                    set_tile(rounded_mouse_pos)

            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    if not sim_running:
                        prev_game_a = game_a
                        game_a = np.full((50,50),False)
                        sim_running = True
                        run_simulation()
                    else:
                        sim_running = False

                    

                    

        pg.display.flip()

if __name__ == "__main__":
    running = True
    main()
