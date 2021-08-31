import pygame
import requests
import pygame_widgets
from pygame_widgets.button import Button


win_x = 550
win_y = 600
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5

# API call for possible boards
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


def possible(y, x, n):
    global grid
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


def solver():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        solver()
                        grid[y][x] = 0
                return


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if grid_original[i - 1][j - 1] != 0:
                    return
                if event.key == 48:  # checking with 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background_color, (
                        position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    return
                if 0 < event.key - 48 < 10:  # We are checking for valid input
                    pygame.draw.rect(win, background_color, (
                        position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0, 0, 0))
                    win.blit(value, (position[0]*50 + 15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return


def main():
    pygame.init()
    win = pygame.display.set_mode((win_x, win_y))
    pygame.display.set_caption("Sudoku")
    # Double brackets or pass single variable
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    button1 = Button(
        win, 50, 510, 150, 50, text='Hello',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: print('Click')
    )
    button2 = Button(
        win, 200, 510, 150, 50, text='Hello',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: print('Click')
    )
    button3 = Button(
        win, 350, 510, 150, 50, text='Hello',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: print(solver())
    )

    for i in range(0, 10):
        # Draw Bold Lines
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
        # X Lines
        pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        # Y Lines
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()

    # Populate Grid with generated puzzle from API
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()

    while True:
        events = pygame.event.get()
        for event in events:
            # if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # pos = pygame.mouse.get_pos()
                # insert(win, (pos[0] // 50, pos[1] // 50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame_widgets.update(events)
        pygame.display.update()


main()
