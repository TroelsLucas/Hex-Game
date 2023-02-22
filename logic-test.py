import numpy as np

board_size = 11

board = np.zeros((board_size, board_size), dtype=int)

player_no = 0


def is_empty(pos):
    return board[pos] == 0


def make_move(pos):
    global player_no
    if is_empty(pos):
        board[pos] = player_no + 1
        player_no = (player_no + 1) % 2
    else:
        print("Illegal move")


def find_neighbours(pos):
    (r, c) = pos
    nset = []

    # this loop will pass through all 8 neighbours of the array, plus the element itself ...
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # ... however, a hexagon has at most 6 neighbours. The surplus elements are skipped by:
            if i == j:
                continue
            # The edge cases are handled by catching "OutOfBounds"-exceptions
            try:
                nset.add((r + i, c + j, board[r + i, c + j]))
            except IndexError:
                pass
    return nset


# assumes that player is either number 1 or 2
def has_player_won(playerno):
    path_found = False
    r, c = 0
    visited_set = {}
    possible_path = {}
    while not path_found and r < board_size and c < board_size:
        if board[r, c] == player_no - 1:
            possible_path.add((r, c, board[r, c]))
            while len(possible_path - visited_set) > 0:
                for elem in possible_path - visited_set:
                    (x, y, _) = elem
                    possible_path = possible_path | find_neighbours((x, y))
                    visited_set.add(elem)
            for i in range(0, board_size):
                if (10, i, player_no) in possible_path:
                    path_found = True
                    break







