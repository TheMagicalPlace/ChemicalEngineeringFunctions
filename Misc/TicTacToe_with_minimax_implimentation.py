from collections import defaultdict
from copy import deepcopy
from random import randint


class TTCGame:

    def __init__(self, ai):
        self.iswon = False
        self.turn = 1
        self.ai = ai
        self._create_board()
        self.gameid = defaultdict(list)
    class Move:
        def __init__(self):
            self.movetype = ' '

        def __str__(self):
            return self.movetype

    class Xmove(Move):

        def __init__(self):
            super().__init__()
            self.movetype = 'X'

    class Omove(Move):

        def __init__(self):
            super().__init__()
            self.movetype = 'O'

    def _create_board(self):
        self.ttcraws = {}
        self.ttcdisp = []
        for _ in range(1, 10):
            self.ttcraws[_] = self.Move()
            if _ % 3 == 0:
                t = [x for x in self.ttcraws.keys()][-3:]
                (self.ttcdisp).append(t)

    def _wincheck(self, board):
        if (board[1].movetype == board[2].movetype == board[3].movetype != ' ' or \
                board[4].movetype == board[5].movetype == board[6].movetype != ' ' or \
                board[7].movetype == board[8].movetype == board[9].movetype != ' ' or \
                board[1].movetype == board[4].movetype == board[7].movetype != ' ' or \
                board[2].movetype == board[5].movetype == board[8].movetype != ' ' or \
                board[3].movetype == board[6].movetype == board[9].movetype != ' ' or \
                board[1].movetype == board[5].movetype == board[9].movetype != ' ' or \
                board[3].movetype == board[5].movetype == board[7].movetype != ' '):
            # print(self.lastmove + ' is the winner!')
            return self.lastmove
        elif self.turn == 10:
            # print('It\'s a tie!')
            return 'Tie'
        else:
            return []

    def playttc(self):
        self.lastmove = 'None'
        while not self._wincheck(self.ttcraws):
            if self.turn % 2 != 0:
                print('player X move')
                move = randint(1, 9)
                if move not in self.ttcraws.keys():
                    continue
                else:
                    self.ttcraws[move] = self.Xmove()
                    self.lastmove = 'X'
                    self.turn += 1
            else:
                print('player O move')
                move = randint(1, 9)
                if str(self.ttcraws[move]) != ' ':
                    continue
                else:
                    self.ttcraws[move] = self.Omove()
                    self.lastmove = 'O'
                    self.turn += 1
        return self._wincheck(self.ttcraws)

    def playttcai(self, id=None):
        self.lastmove = 'None'
        while not self._wincheck(self.ttcraws):
            if id is not None: self.gameid[id].append(str(self))
            if self.turn % 2 != 0:
                # print('player X move')
                nextmove = self.ai(self.ttcraws, 5, True, -1000, 1000)
                self.ttcraws.update(nextmove)
                self.lastmove = 'X'
                self.turn +=1
            else:
                #print('player O move')
                move = randint(1, 9)
                while str(self.ttcraws[move]) != ' ':
                    move = randint(1, 9)
                else:
                    self.ttcraws[move] = self.Omove()
                    self.lastmove = 'O'
                    self.turn += 1
        if id is not None: self.gameid[id].append(str(self))
        return self._wincheck(self.ttcraws), self.gameid

    def __str__(self):
        self.ttcdisp = [list(self.ttcraws.values())[:3], list(self.ttcraws.values())[3:6],
                        list(self.ttcraws.values())[6:10]]
        repboard = ''
        for x in self.ttcdisp:
            repboard += \
                '|¯¯¯¯¯| |¯¯¯¯¯| |¯¯¯¯¯|\n' + \
                '|  {0}  | |  {1}  | |  {2}  |\n'.format(x[0], x[1], x[2]) + \
                '|_____| |_____| |_____|\n'

        return repboard


class minmaxAI():
    class Move:
        def __init__(self):
            self.movetype = ' '

        def __str__(self):
            return self.movetype

    class Xmove(Move):

        def __init__(self):
            super().__init__()
            self.movetype = 'X'

    class Omove(Move):

        def __init__(self):
            super().__init__()
            self.movetype = 'O'

    def all_branches(self, orig, player=True):
        noderaw = []
        for i in range(1, len(orig) +1):
            ttcraws = deepcopy(orig)
            if str(ttcraws[i]) != ' ':
                continue
            else:
                ttcraws[i] = self.Xmove() if player else self.Omove()
                noderaw.append(ttcraws)
        return noderaw

    def __str__(self):
        print()
        for y in self.node:
            x = [list(y.values())[:3], list(y.values())[3:6],
                 list(y.values())[6:10]]
            repboard = ''
            for x in x:
                repboard += \
                    '|¯¯¯¯¯| |¯¯¯¯¯| |¯¯¯¯¯|\n' + \
                    '|  {0}  | |  {1}  | |  {2}  |\n'.format(x[0], x[1], x[2]) + \
                    '|_____| |_____| |_____|\n'

            print(repboard)
        return ' '

    def __init__(self):
        self.branch = defaultdict(list)
        self.setflag = False
        self.node_value_pairs = {}
        self.depthlimit = 5

    def _wincheck(self, board):

        board = [[board[1].movetype, board[2].movetype, board[3].movetype],
                 [board[4].movetype, board[5].movetype, board[6].movetype],
                 [board[7].movetype, board[8].movetype, board[9].movetype]]
        value = 0

        for row in board:
            if set(row) == set('X'):
                value += 1000
            elif set(row) == set('O'):
                value -= 1000
            # elif ('X' in row) and ('O' in row): value -=10
        diag = [x for y in board for x in y]
        for row in [diag[0:9:4], diag[2:7:2]]:
            if set(row) == set('X'):
                value += 1000
            elif set(row) == set('O'):
                value -= 1000
            # elif ('X' in row) and ('O' in row): value -= 10
        for row in zip(*board):
            if set(row) == set('X'):
                value += 1000
            elif set(row) == set('O'):
                value -= 1000
            # elif ('X' in row) and ('O' in row): value -=10
        return value

    '''
        if ((board[1]).movetype == (board[2]).movetype == (board[3]).movetype =='X' != ' ' or \
                (board[4]).movetype == (board[5]).movetype == (board[6]).movetype =='X' != ' ' or \
                (board[7]).movetype == (board[8]).movetype == (board[9]).movetype =='X' != ' ' or \
                (board[1]).movetype == (board[4]).movetype == (board[7]).movetype =='X' != ' ' or \
                (board[2]).movetype == (board[5]).movetype == (board[8]).movetype =='X' != ' ' or \
                (board[3]).movetype == (board[6]).movetype == (board[9]).movetype =='X' != ' ' or \
                (board[1]).movetype == (board[5]).movetype == (board[9]).movetype =='X' != ' ' or \
                (board[3]).movetype == (board[5]).movetype == (board[7]).movetype =='X' != ' '):
                return 'X'
        elif ((board[1]).movetype == (board[2]).movetype == (board[3]).movetype =='O' != ' ' or \
            (board[4]).movetype == (board[5]).movetype == (board[6]).movetype =='O'!= ' ' or \
            (board[7]).movetype == (board[8]).movetype == (board[9]).movetype =='O' != ' ' or \
            (board[1]).movetype == (board[4]).movetype == (board[7]).movetype =='O'!= ' ' or \
            (board[2]).movetype == (board[5]).movetype == (board[8]).movetype =='O' != ' ' or \
            (board[3]).movetype == (board[6]).movetype == (board[9]).movetype =='O' != ' ' or \
            (board[1]).movetype == (board[5]).movetype == (board[9]).movetype =='O'!= ' ' or \
            (board[3]).movetype == (board[5]).movetype == (board[7]).movetype =='O' != ' ') :
                return 'O'
        elif [(board[1]).movetype(board[2]).movetype,(board[3]).movetype] == 'O' and 'X') or \
            (board[4]).movetype == (board[5]).movetype == (board[6]).movetype =='O'!= ' ' or \
            (board[7]).movetype == (board[8]).movetype == (board[9]).movetype =='O' != ' ' or \
            (board[1]).movetype == (board[4]).movetype == (board[7]).movetype =='O'!= ' ' or \
            (board[2]).movetype == (board[5]).movetype == (board[8]).movetype =='O' != ' ' or \
            (board[3]).movetype == (board[6]).movetype == (board[9]).movetype =='O' != ' ' or \
            (board[1]).movetype == (board[5]).movetype == (board[9]).movetype =='O'!= ' ' or \
            (board[3]).movetype == (board[5]).movetype == (board[7]).movetype =='O' != ' ') :
                print('memememe')
        elif ' ' not in tiecheck:
            print('yeet')
            return -10
        else: return 0
    '''

    def minMax(self, node, depth, player, *args):
        maxdepth = self.depthlimit
        if depth == 0:
            val = self._wincheck(node)
            if val:
                return val
            else:
                return 1
        elif player:
            value = -10000
            nodebranch = self.all_branches(node, player)
            for i in nodebranch:
                value = max(value, self.minMax(i, depth - 1, maxdepth, False))
                # self.branch[depth].append(self.minMax(i, depth - 1, maxdepth, False))
                if depth == maxdepth:
                    self.node_value_pairs[value] = i
            if depth == maxdepth:
                return self.node_value_pairs[value]
            else:
                return value
        else:
            value = 10000
            nodebranch = self.all_branches(node, player)
            for j in nodebranch:
                value = min(value, self.minMax(j, depth - 1, maxdepth, True))
                # self.branch[depth].append(self.minMax(j, depth - 1, maxdepth, True))

            return value

    def negMax(self, node, depth, maxdepth, color, alpha, beta):
        if depth == 0:
            val = self._wincheck(node) * color
            return val
        value = -1000
        subnode = self.all_branches(node)
        for node in subnode:
            value = max(value, self.negMax(node, depth - 1, maxdepth, -color, -beta, -alpha))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            if depth == maxdepth:
                self.node_value_pairs[value] = node
        if depth == maxdepth:
            return self.node_value_pairs[value]
        else:
            return value

    def alphabeta(self, node, depth, maxing_player, alpha, beta):
        if depth > self.depthlimit: depth = self.depthlimit
        if depth == 0:
            val = self._wincheck(node)
            return val
        if maxing_player:
            value = -1000
            subnodes = self.all_branches(node, maxing_player)
            for node in subnodes:
                value = max(value, self.alphabeta(node, depth - 1, False, alpha, beta))
                alpha = max(alpha, value)
                self.node_value_pairs[value] = node
                if alpha >= beta:
                    break
            if depth == self.depthlimit:
                return self.node_value_pairs[value]
            else:
                return value
        else:
            value = 1000
            subnodes = self.all_branches(node, maxing_player)
            for node in subnodes:
                value = min(value, self.alphabeta(node, depth - 1, True, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
                self.node_value_pairs[value] = node
            return value


import time

timezero = time.time()
xcount, ocount, tiecount = 0, 0, 0

gamedir = defaultdict(list)

for i in range(1, 101):
    s = TTCGame(minmaxAI().alphabeta)
    winner, gameid = s.playttcai(i)
    gamedir.update(gameid)
    if winner == 'X': xcount += 1
    if winner == 'O': ocount += 1
    if winner == 'Tie': tiecount += 1
    print('Game #', i, ' Winner: ', winner)
    print('X: ', xcount, 'O: ', ocount, 'Tie: ', tiecount)
totaltime = time.time() - timezero
print(totaltime)

timezero = time.time()
xcount, ocount, tiecount = 0, 0, 0

gamedir = defaultdict(list)

for i in range(1, 101):
    s = TTCGame(minmaxAI().minMax)
    winner, gameid = s.playttcai(i)
    gamedir.update(gameid)
    if winner == 'X': xcount += 1
    if winner == 'O': ocount += 1
    if winner == 'Tie': tiecount += 1
    print('Game #', i, ' Winner: ', winner)
    print('X: ', xcount, 'O: ', ocount, 'Tie: ', tiecount)
totaltime = time.time() - timezero
print(totaltime)
