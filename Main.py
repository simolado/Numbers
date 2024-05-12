import random
import pygame


class Table:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.table: list[list[int]] = []

    def new_tab(self) -> None:
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.table = [[random.choice(numbers) for _ in range(self.columns)] for _ in range(self.rows)]

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self) -> int:
        return self.columns

    def get_tab(self) -> None:
        print(f'{self.rows}x{self.columns} Table:')
        for row in self.table:
            print(row)

    def solve_rows(self) -> None:
        for row in range(self.rows):
            for col in range(0, self.columns - 1):
                if self.table[row][col] == self.table[row][col + 1] or self.table[row][col] + self.table[row][col + 1] == 10:
                    self.table[row][col] = self.table[row][col + 1] = 0
        print("Table solved horizontally:")
        for row in self.table:
            print(row)

    def solve_columns(self) -> None:
        for col in range(self.columns):
            for row in range(0, self.rows - 1):
                if self.table[row][col] == self.table[row + 1][col] or self.table[row][col] + self.table[row + 1][col] == 10:
                    self.table[row][col] = self.table[row][col + 1] = 0
        print("Table solved vertically:")
        for row in self.table:
            print(row)


pygame.init()

pygame.display.set_caption('Numbers')

default = True

if not default:
    r = int(input("set rows \n"))
    c = int(input("set columns \n"))

r, c = 10, 10
table = Table(r, c)
table.new_tab()

WIDTH, HEIGHT = 1000, 1000
ROWS, COLUMNS = table.get_rows(), table.get_columns()
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLUMNS

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont("verdana", 60, bold=True)

OUTLINE_THICKNESS = 10
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)


class Tile:

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT
        self.is_selected = False
        self.color = WHITE

    def show(self) -> None:
        print(
            f'x:{self.x}, y:{self.y}, value:{self.value}, row:{self.row + 1}, col:{self.col + 1}, color: {self.color}, is_selected:{self.is_selected}')

    def draw(self, window) -> None:
        back_color = WHITE
        if self.is_selected:
            self.color = RED
        elif self.color == GREEN:
            back_color = self.color
            self.color = BLACK
        else:
            self.color = BLACK
        pygame.draw.rect(window, back_color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, self.color)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def select(self) -> None:
        self.is_selected = True

    def position(self, tile2) -> str:
        if self.is_equal(tile2):
            return "same"
        if abs(self.row - tile2.row) == 1 and abs(self.col - tile2.col) == 1:
            return "diagonal"
        if self.row - tile2.row == 1 and tile2.col - self.col == table.columns - 1:
            return "previous line"
        if self.row - tile2.row == -1 and self.col - tile2.col == table.columns - 1:
            return "next line"
        if abs(self.row - tile2.row) > 1 or abs(self.col - tile2.col) > 1:
            return "not adjacent"
        if self.row - tile2.row == -1:
            return "down"
        if self.row - tile2.row == 1:
            return "up"
        if self.col - tile2.col == -1:
            return "right"
        if self.col - tile2.col == 1:
            return "left"

    def is_solvable(self, tile2) -> bool:
        if self.is_equal(tile2):
            return False
        if abs(self.row - tile2.row) == 1 and abs(self.col - tile2.col) == 1:
            return False
        if self.row - tile2.row == 1 and tile2.col - self.col == table.columns - 1:
            return True
        if self.row - tile2.row == -1 and self.col - tile2.col == table.columns - 1:
            return True
        if abs(self.row - tile2.row) > 1 or abs(self.col - tile2.col) > 1:
            return False
        else:
            return True

    def is_equal(self, tile2) -> bool:
        if tile2.row == self.row and tile2.col == self.col:
            return True
        else:
            return False

    def set_value(self, new_value) -> None:
        self.value = new_value

    def is_border(self) -> str:
        if 0 < self.row < table.rows - 1 and 0 < self.col < table.columns - 1:
            return "not border"
        if self.row == 0 and self.col == 0:
            return "ul angle"
        if self.row == 0 and self.col == table.columns - 1:
            return "ur angle"
        if self.row == table.rows - 1 and self.col == table.columns - 1:
            return "dr angle"
        if self.row == table.rows - 1 and self.col == 0:
            return "dl angle"
        if self.row == 0:
            return "upper border"
        if self.col == 0:
            return "left border"
        if self.col == COLUMNS - 1:
            return "right border"
        if self.row == COLUMNS - 1:
            return "lower border"


def draw(window, tab: Table, sel_tiles: list[Tile], valid_moves: list[Tile]) -> None:
    window.fill(WHITE)

    for row in range(tab.rows):
        for col in range(tab.columns):
            tile = Tile(tab.table[row][col], row, col)
            if tile.is_equal(sel_tiles[0]):
                tile.select()
            for tilex in valid_moves:
                if tile.is_equal(tilex):
                    tile.color = GREEN
            if tile.value != 0:
                tile.draw(window)

    draw_grid(window)

    pygame.display.update()


def get_tile_pos(x_pos, y_pos, tab: Table) -> Tile:
    for row in range(tab.rows):
        for col in range(tab.columns):
            if col * RECT_WIDTH < x_pos < (col + 1) * RECT_WIDTH and row * RECT_HEIGHT < y_pos < (
                    row + 1) * RECT_HEIGHT:
                return Tile(tab.table[row][col], row, col)


def get_tile_rc(sel_row: int, sel_col: int, tab: Table) -> Tile:
    if not 0 <= sel_row < table.rows or not 0 <= sel_col < table.columns:
        return Tile(0, table.rows, table.columns)
    return Tile(tab.table[sel_row][sel_col], sel_row, sel_col)


def move(tile1: Tile, direction: str) -> Tile:
    if direction == "up":
        return get_tile_rc(tile1.row - 1, tile1.col, table)
    if direction == "down":
        return get_tile_rc(tile1.row + 1, tile1.col, table)
    if direction == "left":
        return get_tile_rc(tile1.row, tile1.col - 1, table)
    if direction == "right":
        return get_tile_rc(tile1.row, tile1.col + 1, table)
    if direction == "next":
        return get_tile_rc(tile1.row + 1, 0, table)
    if direction == "previous":
        return get_tile_rc(tile1.row - 1, table.columns - 1, table)


def path(tile1: Tile, tile2: Tile) -> list[Tile]:
    result = []
    direction = ""
    if tile1.is_solvable(tile2):
        return result
    if tile1.col == tile2.col:
        if tile1.row < tile2.row:
            direction = "down"
        else:
            direction = "up"
    elif tile1.row == tile2.row:
        if tile1.col < tile2.col:
            direction = "right"
        else:
            direction = "left"
    elif tile1.row < tile2.row:
        while tile1.row < tile2.row:
            while tile1.col != table.columns - 1:
                tile1 = move(tile1, "right")
                result.append(tile1)
            tile1 = move(tile1, "next")
            result.append(tile1)
        if tile1.is_equal(tile2):
            del result[-1]
            return result
        while not tile1.position(tile2) == "right":
            tile1 = move(tile1, "right")
            result.append(tile1)
        return result
    elif tile1.row > tile2.row:
        while tile1.row > tile2.row:
            while tile1.col != 0:
                tile1 = move(tile1, "left")
                result.append(tile1)
            tile1 = move(tile1, "previous")
            result.append(tile1)
        if tile1.is_equal(tile2):
            del result[-1]
            return result
        while not tile1.position(tile2) == "left":
            tile1 = move(tile1, "left")
            result.append(tile1)
        return result
    while not tile1.is_solvable(tile2):
        tile1 = move(tile1, direction)
        if tile1.row == table.rows and tile1.col == table.columns:
            return result
        result.append(tile1)
    return result


"""def update_tile(tab: Table, *new_tile: Tile) -> None:
    for tile in new_tile:
        tab.table[tile.row][tile.col] = tile.value"""

def update_tile(tab: Table, *new_tile: Tile) -> None:
    for tile in new_tile:
        # Check if the row and column indices are within bounds
        if 0 <= tile.row < tab.rows and 0 <= tile.col < tab.columns:
            tab.table[tile.row][tile.col] = tile.value
        else:
            print("Error: Attempting to update tile outside table bounds.")

def solve(tile1: Tile, tile2: Tile) -> bool:
    if tile1.value + tile2.value == 10 or tile1.value == tile2.value:
        tile1.set_value(0)
        tile2.set_value(0)
        print("Solved")
        return True
    else:
        print("can't solve")
        return False


def draw_grid(window) -> None:
    real_height = HEIGHT*table.rows/ROWS
    for row in range(1, table.rows):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, BLACK, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, table.columns):
        x = col * RECT_WIDTH
        pygame.draw.line(window, BLACK, (x, 0), (x, real_height), OUTLINE_THICKNESS)

    pygame.draw.rect(window, BLACK, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def valid_moves(tile: Tile) -> list[Tile]:
    tiles_x = [Tile(table.table[row][col], row, col) for row in range(table.rows) for col in range(table.columns)]
    result = []
    for tile_x in tiles_x:
        if tile_x.value == 0:
            del tile_x
    for tile_x in tiles_x:
        route_x = path(tile, tile_x)
        if route_x is None:
            result.append(tile_x)
        for step in route_x:
            if step.value != 0:
                break
        else:
            result.append(tile_x)

    for res in result:
        if res.value == 0:
            del res
    return result


def empty_rows(tab: Table, tile1: Tile, tile2: Tile) -> None:
    print(table.rows)
    for row in [tile1.row, tile2.row]:
        if row == tab.rows:
            row = row-1
        if sum(tab.table[row]) == 0:
            del tab.table[row]
            tab.rows -= 1


# run indicator
run = True

click_count = 0
# list of selected tiles
Sel_Tiles: list[Tile] = [Tile(0, table.rows, table.columns)]
Valid_Moves: list[Tile] = []

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_count += 1
            pos = pygame.mouse.get_pos()  # mouse position

            # first click
            if click_count == 1:
                Tile_sel = get_tile_pos(pos[0], pos[1], table)  # selected tile
                if Tile_sel.value == 0:
                    click_count = 0
                    print("you can't")
                    break
                Sel_Tiles[0] = Tile_sel
                Valid_Moves = valid_moves(Tile_sel)
                print(Valid_Moves)
                print("Selected:")
                Tile_sel.show()
                print("-----------------")

            # second click
            elif click_count == 2:
                Tile2 = get_tile_pos(pos[0], pos[1], table)
                print("Tile2:")
                Tile2.show()

                if Tile2.value == 0:
                    print("selected a 0")
                    Sel_Tiles[0] = Tile_sel
                    click_count = 1
                    break

                # equal check
                if Tile2.is_equal(Tile_sel):
                    print("same")
                    Sel_Tiles = [Tile(0, table.rows, table.columns)]
                    Valid_Moves: list[Tile] = []
                    click_count = 0
                    break

                # not normal check
                if not Tile_sel.is_solvable(Tile2):
                    route = path(Tile_sel, Tile2)
                    print(route)
                    if type(route) is None:
                        print("continue selection (None)")
                        Sel_Tiles[0] = Tile_sel
                        click_count = 1
                        break
                    for el in route:
                        if el.value != 0:
                            print("continue selection (obstacle)")
                            click_count = 1
                            break
                    if click_count == 1:
                        break
                    # check if solvable
                    if solve(Tile2, Tile_sel):
                        # update
                        update_tile(table, Tile2, Tile_sel)
                        # empty rows
                        empty_rows(table, Tile2, Tile_sel)
                        # reset selection
                        Sel_Tiles = [Tile(0, table.rows, table.columns)]
                        Valid_Moves: list[Tile] = []
                        print("-----------------")
                        click_count = 0
                    else:
                        print("continue selection (None)")
                        Sel_Tiles[0] = Tile_sel
                        click_count = 1
                if click_count == 1:
                    break
                # check if solvable
                if solve(Tile2, Tile_sel):
                    # update
                    update_tile(table, Tile2, Tile_sel)
                    # empty rows
                    empty_rows(table, Tile2, Tile_sel)
                    # reset selection
                    Sel_Tiles = [Tile(0, table.rows, table.columns)]
                    Valid_Moves: list[Tile] = []
                    print("-----------------")
                    click_count = 0
                else:
                    print("continue selection (None)")
                    Sel_Tiles[0] = Tile_sel
                    click_count = 1

    draw(WINDOW, table, Sel_Tiles, Valid_Moves)

    pygame.display.update()
