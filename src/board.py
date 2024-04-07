def createBoard(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

def printBoard(board):
    for row in board:
        print('|' + '|'.join(row) + '|')
