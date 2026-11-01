
import pygame
import random

pygame.init()

# settings
scrn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = scrn.get_size()

gridwidth = 160
gridlngth = 100
cellsize = min(screen_width // gridwidth, screen_height // gridlngth)
d = 100

# create random grid
g = [
    [random.choice([0, 0, 0, 1]) for x in range(gridwidth)]
    for y in range(gridlngth)
]

def box_draw(a, b):
    pygame.draw.rect(
        scrn,
        (255, 255, 255),
        (a, b, cellsize, cellsize)
    )


def draw():
    scrn.fill((0, 0, 0))

    for y in range(gridlngth):
        for x in range(gridwidth):
            c = g[y][x]
            if c == 1:
                xp = x * cellsize
                yp = y * cellsize
                box_draw(xp, yp)

    pygame.display.update()


def count_n(x, y):
    cnt = 0

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            nx = x + dx
            ny = y + dy

            if nx >= 0 and nx < gridwidth and ny >= 0 and ny < gridlngth:
                if g[ny][nx] == 1:
                    cnt = cnt + 1

    return cnt


def next_gen():
    global g
    ngrid = []

    for y in range(gridlngth):
        nrow = []
        for x in range(gridwidth):
            neybor = count_n(x, y)
            cellalive = g[y][x]

            if cellalive == 1:
                if neybor == 2 or neybor == 3:
                    nrow.append(1)
                else:
                    nrow.append(0)
            elif neybor == 3:
                nrow.append(1)
            else:
                nrow.append(0)

        ngrid.append(nrow)

    g = ngrid


def upd():
    draw()
    next_gen()



# start
running = True
started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            g = [
                [random.choice([0, 0, 0, 1]) for x in range(gridwidth)]
                for y in range(gridlngth)
            ]

            started = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                started = not started

    if started:
        upd()
        pygame.time.delay(d)
    else:
        draw()

pygame.quit()
