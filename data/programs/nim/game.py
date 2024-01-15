from random import randrange
class Game:
    def __init__(self, state, on_move=True, hardcore=False):
        self.on_move = on_move
        self.state = list(filter(lambda x: x > 0, state))
        self.opp = Opponent(hardcore)

    def __str__(self):
        s = ''
        if self.on_move:
            s += 'human to move: '
        else:
            s += 'computer to move: '
        s += ' | '.join([k*'*' for k in self.state])
        return s
        
    def legal_move(self, move):
        return move.col >= 0 and move.col < len(self.state) and move.num >= 0 and self.state[move.col] >= move.num

    def take(self, move):
        self.on_move = not self.on_move
        if move.col >= 0 and move.col < len(self.state):
            self.state[move.col] -= move.num
        self.state = list(filter(lambda x: x > 0, self.state))
    
    def over(self):
        return len(self.state) == 0
    
    def winner(self):
        return not self.on_move

    def moves(self):
        return [Move(x,y+1) for x in range(len(self.state)) for y in range(self.state[x])]

    def auto(self):
        return self.opp.decision(self)

    def update(self):
        self.take(self.auto())

class Opponent:
    def __init__(self, hardcore):
        self.hardcore = hardcore

    def decision(self, game):
        if self.hardcore:
            return None
        else:
            ms = game.moves()
            return ms[randrange(len(ms))]

class Move:
    def __init__(self, col, num):
        self.col = col
        self.num = num

    def __str__(self):
        return f'take {self.num} from {self.col}'
