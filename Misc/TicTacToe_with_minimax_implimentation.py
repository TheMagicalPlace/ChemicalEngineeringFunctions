class TTCGame:

    def __init__(self):
        self.iswon = False
        self.turn = 1
        self._create_board()

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
            return self.lastmove + 'is the winner!'
        elif self.turn == 10:
            return 'It\'s a tie!'
        else:
            return []

    def playttc(self):
        self.lastmove = 'None'
        while not self._wincheck(self.ttcraws):
            if self.turn % 2 != 0:
                print('player X move')
                move = int(input('Select move'))
                if move not in self.ttcraws.keys():
                    continue
                else:
                    self.ttcraws[move] = self.Xmove()
                    self.lastmove = 'X'
                    self.turn += 1
            else:
                print('player O move')
                move = input('Select move')
                if move not in self.ttcraws.keys():
                    move = int(input('Select move'))
                else:
                    self.ttcraws[move] = self.Omove()
                    self.lastmove = 'O'
                    self.turn += 1

            print(self)

    def __str__(self):
        repboard = ''
        for x in self.ttcdisp:
            repboard += \
                '|¯¯¯¯¯| |¯¯¯¯¯| |¯¯¯¯¯|\n' + \
                '|  {0}  | |  {1}  | |  {2}  |\n'.format(x[0], x[1], x[2]) + \
                '|_____| |_____| |_____|\n'

        return repboard


s = TTCGame()

s.playttc()
