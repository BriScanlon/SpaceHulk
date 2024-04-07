class Entity:
    def __init__(self, name, health, attack, ap):
        self.name = name
        self.health = health
        self.attack = attack
        self.ap = ap  # Action points
        self.position = (0, 0)  # Default starting position

class SpaceMarine(Entity):
    def __init__(self, name):
        super().__init__(name, health=100, attack=50, ap=3)

class Genestealer(Entity):
    def __init__(self, name):
        super().__init__(name, health=50, attack=70, ap=4)

def createBoard(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

def printBoard(board):
    for row in board:
        print('|' + '|'.join(row) + '|')

def isValidMove(board, newPosition):
    rows, cols = len(board), len(board[0])
    return 0 <= newPosition[0] < rows and 0 <= newPosition[1] < cols and board[newPosition[0]][newPosition[1]] == ' '

def playerMove(board, marine):
    print("Your turn! You can move one step (up, down, left, right).")
    move = input("Enter your move: ").strip().lower()
    current_position = marine.position
    new_position = current_position
    
    if move == "up":
        new_position = (current_position[0] - 1, current_position[1])
    elif move == "down":
        new_position = (current_position[0] + 1, current_position[1])
    elif move == "left":
        new_position = (current_position[0], current_position[1] - 1)
    elif move == "right":
        new_position = (current_position[0], current_position[1] + 1)
    else:
        print("Invalid move.")
        return False

    if isValidMove(board, new_position):
        board[current_position[0]][current_position[1]] = ' '
        board[new_position[0]][new_position[1]] = 'M'
        marine.position = new_position
        return True
    else:
        print("Move not allowed.")
        return False

def initializeGame(board, marines, genestealers):
    for marine in marines:
        board[marine.position[0]][marine.position[1]] = 'M'
    
    for genestealer in genestealers:
        board[genestealer.position[0]][genestealer.position[1]] = 'G'

def gameLoop(board, marines, genestealers):
    win_position = (len(board) - 1, len(board[0]) - 1)  # Target position for win condition

    while True:
        printBoard(board)
        if marines[0].position == win_position:
            print("Congratulations! You've reached the target position. You win!")
            break
        
        if not playerMove(board, marines[0]):
            continue  # If the move is invalid, skip the rest of the loop and try again
        
        # Here, you could add logic for Genestealers' moves or other game mechanics

def main():
    board = createBoard(10, 10)
    marines = [SpaceMarine("Marine1")]
    genestealers = [Genestealer("Genestealer1")]
    
    # Initial positions
    marines[0].position = (1, 1)
    genestealers[0].position = (8, 8)
    
    initializeGame(board, marines, genestealers)
    gameLoop(board, marines, genestealers)

if __name__ == "__main__":
    main()
