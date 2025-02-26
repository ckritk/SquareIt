import sq
from sq import SIZE

MAX_PLAYER = 1  # Maximizing player (AI)
MIN_PLAYER = -1  # Minimizing player (Human)
DEPTH = 2
NEXT = 43

CHANGED = False

def evaluate_board(state, is_maximizing_player):
    if DEPTH%2==0:
        x4 = sq.count_4pt_squares(state, MAX_PLAYER)
        y3 = sq.count_3pt_squares(state, MIN_PLAYER)
        x3 = sq.count_3pt_squares(state, MAX_PLAYER)
    else:
        x4 = -sq.count_4pt_squares(state, MIN_PLAYER)
        y3 = sq.count_3pt_squares(state, MAX_PLAYER)
        x3 = -sq.count_3pt_squares(state, MIN_PLAYER)
    #print(x4,y3,x3)
    return x4*1000 - y3*100 + x3*5


def get_possible_moves(state, is_maximizing_player):
    global NEXT
    x = sq.get_points(NEXT)
    return x


def make_move(state, move, is_maximizing_player,change_weight = False):
    global CHANGED
    new = [i.copy() for i in state]
    if is_maximizing_player: player = MAX_PLAYER
    else: player = MIN_PLAYER
    new[move[0]][move[1]] = player

    if change_weight:
        CHANGED = True
        sq.adjust_weights_for_point(move, player,state)

    #print("State Sfter Move : \n")
    #for i in state: print(i)
    
    return new

def minimax(state1, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf'), use_alpha_beta=False):
    state = [i.copy() for i in state1]
    if depth == 0 or is_terminal(state):
        return evaluate_board(state, is_maximizing_player)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(state, is_maximizing_player):
            new_state = make_move(state, move, is_maximizing_player)
            eval_score = minimax(new_state, depth - 1, False, alpha, beta, use_alpha_beta)
            max_eval = max(max_eval, eval_score)
            if use_alpha_beta:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
        return max_eval

    else:  
        min_eval = float('inf')
        for move in get_possible_moves(state, is_maximizing_player):
            new_state = make_move(state, move, is_maximizing_player)
            eval_score = minimax(new_state, depth - 1, True, alpha, beta, use_alpha_beta)
            min_eval = min(min_eval, eval_score)
            if use_alpha_beta:
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
        return min_eval


def is_terminal(state):
    if sq.count_4pt_squares(state, MAX_PLAYER)+ \
    sq.count_4pt_squares(state, MIN_PLAYER)>0 : return True
    return False
""" change it to checking with last made move """

def find_best_move(state, depth, use_alpha_beta=False):
    best_move = None
    best_value = float('-inf') 

    for move in get_possible_moves(state, True):  
        new_state = make_move(state, move, True)
        move_value = minimax(new_state, depth - 1, False, float('-inf'), float('inf'), use_alpha_beta)
        #if not (move_value and best_value): return None
        if move_value > best_value:
            best_value = move_value
            best_move = move
            #print(best_move,best_value)
    return best_move



def main():
    state = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    depth = 2
    use_alpha_beta = True  

    while True:
        print_board(state)

        if is_terminal(state):
            print("Game over!")
            break

        move = get_human_move(state)
        state = make_move(state, move, False,True)

        if is_terminal(state):
            print("Game over! Human wins!")
            break

        best_move = find_best_move(state, depth, use_alpha_beta)
        if best_move:
            state = make_move(state, best_move, True,True)
            print(f"AI plays: {best_move}")

        if is_terminal(state):
            print("Game over! AI wins!")
            break

def print_board(state):
    """Function to display the game board."""
    for row in state:
        print(" | ".join(str(x) if x != 0 else '.' for x in row))
    print()

def get_human_move(state):
    """Function to get a valid move from the human player."""
    while True:
        try:
            move = input("Enter your move as 'row,col' (e.g., '0,1'): ")
            row, col = map(int, move.split(","))
            if state[row][col] == 0:
                return (row, col)
            else:
                print("Invalid move, spot already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid row and column.")

if __name__ == "__main__":
    main()
