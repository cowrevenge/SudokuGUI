import pygame
import requests
import pygame_widgets
from pygame_widgets.button import Button
pygame.init()

# set window parameters
win_x = 550
win_y = 600
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5  # Prevents removing of grid lines during number removals
red = (255, 0, 0)
green = (0, 128, 0)
current_select = (0, 0)
my_font = pygame.font.SysFont('Comic Sans MS', 35)


# API call for possible boards
grid_original = []
grid_guess = []
grid = []


def api_new_puzzle():
    global grid_original
    global grid
    global grid_guess
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    grid = response.json()['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    grid_guess = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


# Call function for puzzled displayed on start up
api_new_puzzle()


# Function for for new game button, calls api for new puzzle and redraws board
def new_game(window_name):
    # clear the board, should change this to a function since its used more the once.
    for i in range(0, 10):
        for j in range(0, 10):
            pygame.draw.rect(window_name, background_color, (
                i * 50 + buffer + 3, j * 50 + buffer + 3, 36, 36))
    api_new_puzzle()
    draw_puzzle_inputs(window_name)


# Populate Grid with generated puzzle from API
def draw_puzzle_inputs(window_name):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                window_name.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()


def pos_selector(win, pos1, pos2):
    pos_deselector(win)
    pygame.draw.rect(win, red, pygame.Rect(pos1, pos2, 42, 42), 5)
    pygame.display.update()
    global current_select
    current_select = (pos1, pos2)


def pos_deselector(win):
    cir_pos1 = current_select[0]
    cir_pos2 = current_select[1]
    pygame.draw.rect(win, background_color, pygame.Rect(cir_pos1, cir_pos2, 42, 42), 5)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((win_x, win_y))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    new_game_button_button = Button(
        win, 50, 510, 150, 50, text='New',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: new_game(win),
        font=pygame.font.SysFont('Comic Sans MS', 45),
    )
    check_solution_button = Button(
        win, 200, 510, 150, 50, text='Check',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: check(),
        font=pygame.font.SysFont('Comic Sans MS', 45),
    )
    solve_puzzle_button = Button(
        win, 350, 510, 150, 50, text='Solve',
        fontSize=50, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: solver(win),
        font=pygame.font.SysFont('Comic Sans MS', 45),
    )

    # Backtracking to find 1st solution, other solutions not possible under real Sudoku rules
    def solve(bo):
        find = find_empty(bo)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i
                if solve(bo):
                    return True
                bo[row][col] = 0
        return False

    def valid(bo, num, pos_check):
        # Check row
        for i in range(len(bo[0])):
            if bo[pos_check[0]][i] == num and pos_check[1] != i:
                return False
        # Column Check
        for i in range(len(bo)):
            if bo[i][pos_check[1]] == num and pos_check[0] != i:
                return False
        # 3x3 Grid Check
        box_x = pos_check[1] // 3
        box_y = pos_check[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if bo[i][j] == num and (i, j) != pos_check:
                    return False
        return True

    def find_empty(bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return i, j  # row, col
        return None

    def solver(solver_win):
        solve(grid)
        for i in range(0, 10):
            for j in range(0, 10):
                pygame.draw.rect(solver_win, background_color, (
                    i * 50 + buffer + 3, j * 50 + buffer + 3, 36, 36))
        draw_puzzle_inputs(solver_win)

    def draw_grind_lines():
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

    def check():
        solve(grid)
        for x in range(9):
            for y in range(9):
                if grid_guess[x][y] != 0:
                    if grid_guess[x][y] == grid[x][y]:
                        if grid_guess[x][y] != grid_original[x][y]:
                            grid_guess[x][y] == grid[x][y]
                            pygame.draw.rect(win, background_color, (y * 50 + 53, x * 50 + 53, 46, 46))
                            value2 = my_font.render(str(grid_guess[x][y]), True, green)
                            win.blit(value2, (y * 50 + 64, x * 50 + 51))
                    if grid_guess[x][y] != grid[x][y]:
                        pygame.draw.rect(win, background_color, (y * 50 + 53, x * 50 + 53, 46, 46))
                        value2 = my_font.render(str(grid_guess[x][y]), True, red)
                        win.blit(value2, (y * 50 + 64, x * 50 + 51))

    draw_grind_lines()

    draw_puzzle_inputs(win)
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                pos1 = pos[0]//50 * 50 + buffer
                pos2 = pos[1]//50 * 50 + buffer
                if 1 <= pos[0]//50 <= 9:
                    if 1 <= pos[1]//50 <= 9:
                        pos_selector(win, pos1, pos2)

            if event.type == pygame.KEYDOWN and current_select:
                #  Reverse X,Y to match grid?
                grid_check0 = current_select[1] // 50 - 1
                grid_check1 = current_select[0] // 50 - 1
                if grid_original[grid_check0][grid_check1] == 0:
                    if event.key == 48:  # ASCII "0" Value is 48
                        grid_guess[grid_check0][grid_check1] = event.key - 48
                        pygame.draw.rect(win, background_color, (current_select[0] - 2, current_select[1] - 2, 46, 46))
                        pos_selector(win, current_select[0], current_select[1])
                        pygame.display.update()

                    if 0 < event.key - 48 < 10:  # We are checking for valid input, then blanking the square
                        pygame.draw.rect(win, background_color, (current_select[0] - 2, current_select[1] - 2, 46, 46))
                        value = my_font.render(str(event.key-48), True, (0, 0, 0))
                        win.blit(value, (current_select[0] + buffer*2, current_select[1] - buffer))
                        grid_guess[grid_check0][grid_check1] = event.key - 48
                        pygame.draw.rect(win, red, pygame.Rect(current_select[0], current_select[1], 42, 42), 5)
                        pygame.display.update()

        pygame_widgets.update(events)
        pygame.display.update()


main()

