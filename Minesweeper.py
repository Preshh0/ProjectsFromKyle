#using recursion and classes to build
import random
import re

#lets create a board object to represent the minesweeper game
#this is so that we can just say "create a new board  project", or
# "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        #let's keep track of these parameters.
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #let's create the board
        #helper function
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row, col) tuples into this set
        self.dug = set() #if we dig at 0, 0, then self.dug = {(0, 0)}

    def make_new_board(self):
        '''
        Constructs a new biard based on the dim size and number of bombs
        we should construct the list of lists here (or whatever representation you prefer)
        but since we have a 2-D board, list of lists is most natural.
        '''
        # generates a new board
        board = [[0 for _ in range(self.dim_size)] for _ in range(self.dim_size) ]
        # this creates an array like this:
        # [
        #     [None, None, ...., None]
        #     [None, None, ...., None]
        #     [None, None, ...., None]
        # ]
        # we can see how this represents a board

        #plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) #return a random integer N such that a <= N <= b
            row = loc // self.dim_size #we want the number of times dim_size goes into loc to tell us the row
            col = loc % self.dim_size #we want the remainder to tell us what index in that row to look for

            if board[row][col] == '*':
                #this means we've actually planted bomb there already so keep going
                continue

            board[row][col] = '*' #plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        
        '''
        now that we have bombs planted, let's assign a number 0-8 for all the empty spaces, which
        represents how many neighbouring bombs there are. we can precompute these and it'll save us some
        effort checking what's around the board later on.
        '''
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    #if this is already a bomb, don't calculate anything
                    continue

                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)
            
 
    def get_num_neighbouring_bombs(self, row, col):

        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1))+1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1)+1):
                if r == row and c == col:
                    #our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        #self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r,c)
        #if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):

        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        #put this together in a string
        string_rep = ' '
        #get max column width for printing
        width = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            width.append(
                len(
                    max(columns, key = len)
                )
            )
        
        #print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = ' '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(width[idx]) + "s"
            cells.append(format % (col))
        indices_row += ' '.join(cells)
        indices_row += ' \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []     
            for idx, col in enumerate(row):
                format = '%-' + str(width[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)    
            string_rep += '|\n'
        
        
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size = 10, num_bombs=10):
    #step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    #step 2: show the user the board and ask for where they want to dig
    #step 3a: if location is a bomb, show game over message
    #step 3b: if location is not a bomb, dig recursively until each square is at least
    #           next to a bomb
    #step 4: repeat steps 2 and 3a/b until there are no more places to dig --> VICTORY!
    safe = True

    while len(board.dug) < board.dim_size** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue
        safe = board.dig(row, col)
        if not safe:
            break
    
    if safe:
        print("Congratulations")
    else:
        print("Sorry, game over")

        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()