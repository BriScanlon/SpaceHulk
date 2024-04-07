from src.entities import SpaceMarine, Genestealer

def moveEntity(board, entity, newPosition):
    oldPosition = entity['position']
    distance = abs(newPosition[0] - oldPosition[0]) + abs(newPosition[1] - oldPosition[1])
    
    if distance <= entity.ap and board[newPosition[0]][newPosition[1]] == ' ':
        board[oldPosition[0]][oldPosition[1]] = ' '
        board[newPosition[0]][newPosition[1]] = 'M' if isinstance(entity, SpaceMarine) else 'G'
        entity['position'] = newPosition
        entity.ap -= distance
        return True
    return False

def attack(entity):
    entity.ap = 0  # Placeholder for actual attack logic
