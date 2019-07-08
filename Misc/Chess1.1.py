from colorama import init, Fore, Back, Style

init(autoreset=True)


class Chessgame():
    Names = ['Rook', 'Knight', 'Bishop',
             'Queen', 'King', 'Pawn']

    def __init__(self):
        self.board = []
        self.board_state = []
        self.current = []
        self._current_state_raw = {}
        self._board_setup()  # sets up the starting board
        self._position_setup()  # initiallizes the chess piece objects
        self.king_check = {'Black': [], 'White': []}

    class Dummy():
        def __init__(self):
            self.owner = 'None'

        def __str__(self):
            return ' '

    class Piece():

        def __init__(self, playerID):
            self.owner = playerID
            self.piece = 'Undef'

        def __str__(self):
            return self.piece + ' '  # self.owner + self.piece

        def getpos(self, current_state_raw):
            self.position = "".join([k for k, v in current_state_raw.items() if self == current_state_raw[k]])

    class Pawn(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Pwn'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            valid_moves = []
            self.getpos(current_state_raw)

            if self.owner == 'Black':
                foreward = chr(ord(self.position[0]) - 1) + self.position[1]
                if foreward[0] not in 'abcdefgh' or foreward[1] not in '12345678' \
                        or current_state_raw[foreward].owner != 'None':
                    foreward = -1
            if self.owner == 'White':
                foreward = chr(ord(self.position[0]) + 1) + self.position[1]
                if foreward[0] not in 'abcdefgh' or foreward[1] not in '12345678' \
                        or current_state_raw[foreward].owner != 'None':
                    foreward = -1
            avbmove = foreward if foreward != -1 else -1
            potatck = [chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1),
                       chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1)]
            potatck = [p for p in potatck if p[0] in 'abcdefgh' and p[1] in '12345678']
            return [p for p in potatck if (current_state_raw[p]).owner != self.owner] + [avbmove]
            return potatck

    class Rook(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Twr'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            moves = []
            self.getpos(current_state_raw)
            e, f, g, h = self.position, self.position, self.position, self.position
            self.getpos(current_state_raw)
            for i in range(1, 8):
                e = (chr(ord(self.position[0]) + i) + str(int(self.position[1]))) if e != -1 else -1
                f = (chr(ord(self.position[0]) - i) + str(int(self.position[1]))) if f != -1 else -1
                g = (chr(ord(self.position[0])) + str(int(self.position[1]) - i)) if g != -1 else -1
                h = (chr(ord(self.position[0])) + str(int(self.position[1]) + i)) if h != -1 else -1
                abcd = [str(e), str(f), str(g), str(h)]
                pots = [x for x in abcd if x[0] in 'abcdefgh' and x[1] in '12345678']
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner != self.owner and str(current_state_raw[x]) != ' ':
                        moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                e, f, g, h = abcd
            return moves

    class Bishop(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Bsp'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            potmoves = []
            self.getpos(current_state_raw)
            a, b, c, d = self.position, self.position, self.position, self.position
            self.getpos(current_state_raw)
            moves = []
            for i in range(1, 8):
                a = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) + i)) if a != -1 else -1
                b = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) - i)) if b != -1 else -1
                c = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) - i)) if c != -1 else -1
                d = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) + i)) if d != -1 else -1
                abcd = [str(a), str(b), str(c), str(d)]
                pots = [x for x in abcd if x[0] in 'abcdefgh' and x[1] in '12345678']
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner != self.owner and str(current_state_raw[x]) != ' ':
                        moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                a, b, c, d = abcd
            return moves

            print([x for x in potmoves if x[0] in 'abcdefgh' and x[1] in '12345678'])

    class Knight(Piece):
        # TODO - impliment knighs movment patterns
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Knt'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            moves = []
            self.getpos(current_state_raw)
            return [self.position]

    class Queen(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Qun'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            potmoves = []
            self.getpos(current_state_raw)
            a, b, c, d, e, f, g, h = self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
            self.getpos(current_state_raw)
            moves = []
            for i in range(1, 8):
                a = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) + i)) if a != -1 else -1
                b = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) - i)) if b != -1 else -1
                c = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) - i)) if c != -1 else -1
                d = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) + i)) if d != -1 else -1
                e = (chr(ord(self.position[0]) + i) + str(int(self.position[1]))) if e != -1 else -1
                f = (chr(ord(self.position[0]) - i) + str(int(self.position[1]))) if f != -1 else -1
                g = (chr(ord(self.position[0])) + str(int(self.position[1]) - i)) if g != -1 else -1
                h = (chr(ord(self.position[0])) + str(int(self.position[1]) + i)) if h != -1 else -1
                abcd = [str(a), str(b), str(c), str(d), str(e), str(f), str(g), str(h)]
                pots = [x for x in abcd if x[0] in 'abcdefgh' and x[1] in '12345678']
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner != self.owner and str(current_state_raw[x]) != ' ':
                        moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                a, b, c, d, e, f, g, h = abcd
            return moves

    class King(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Kng'

        def __str__(self):
            return super().__str__()

        def getpos(self, current_state_raw):
            super().getpos(current_state_raw)

        def move_range(self, current_state_raw):
            potmoves = []
            self.getpos(current_state_raw)
            a, b, c, d, e, f, g, h = self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
            self.getpos(current_state_raw)
            moves = []
            for i in range(1, 2):
                a = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) + i)) if a != -1 else -1
                b = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) - i)) if b != -1 else -1
                c = (chr(ord(self.position[0]) + i) + str(int(self.position[1]) - i)) if c != -1 else -1
                d = (chr(ord(self.position[0]) - i) + str(int(self.position[1]) + i)) if d != -1 else -1
                e = (chr(ord(self.position[0]) + i) + str(int(self.position[1]))) if e != -1 else -1
                f = (chr(ord(self.position[0]) - i) + str(int(self.position[1]))) if f != -1 else -1
                g = (chr(ord(self.position[0])) + str(int(self.position[1]) - i)) if g != -1 else -1
                h = (chr(ord(self.position[0])) + str(int(self.position[1]) + i)) if h != -1 else -1
                abcd = [str(a), str(b), str(c), str(d), str(e), str(f), str(g), str(h)]
                pots = [x for x in abcd if x[0] in 'abcdefgh' and x[1] in '12345678']
                pots = [x for x in pots if (current_state_raw[x]).owner != self.owner]
                for x in pots:
                    if (current_state_raw[x]).owner != self.owner and str(current_state_raw[x]) != ' ':
                        moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                a, b, c, d, e, f, g, h = abcd
            return moves

    def _king_check_function(self, turn_ID):
        # TODO - Implement the rest of the function used to check if a move by either player puts either king into check...
        #  this should cover moves by either king as well as those by other pieces.
        for k, v in self._current_state_raw.items():
            print(k, v)
            if v.owner != turn_ID and v.owner in ['Black', 'White']:
                self.king_check[turn_ID] += v.move_range(self._current_state_raw)

    def _position_setup(self):
        '''
        This builds the intial chess board, calling constructors for all the chess pieces as well as a 'Dummy' piece to
        occupy empty spaces

        :return:
        '''
        ### TODO - Update this to keep track of changes to the board
        back_row = lambda owner: [self.Rook(owner), self.Knight(owner), self.Bishop(owner),
                                  self.Queen(owner), self.King(owner), self.Bishop(owner), self.Knight(owner),
                                  self.Rook(owner)]

        for y in range(1, 9):
            self.board_state.append(back_row('White')) if (y == 1) else \
                self.board_state.append([self.Pawn('White') for i in range(1, 9)]) if (y == 2) else \
                    self.board_state.append([self.Pawn('Black') for i in range(1, 9)]) if (y == 7) else \
                        self.board_state.append(back_row('Black')) if (y == 8) else \
                            self.board_state.append([self.Dummy() for x in range(1, 9)])
        tracker = {}
        for (a, b) in zip([xx for x in self.board for xx in x], [yy for y in self.board_state for yy in y]):
            tracker[a] = b

            if a in list(zip(*self.board))[-1]:
                self.current.append(tracker)  # The list of dictionaries used in the __Str__ method
                self._current_state_raw.update(
                    tracker)  # the list of single dictionaries used for  tracking where everything is
                tracker = {}
        (self._current_state_raw['g3']).move_range(self._current_state_raw)

    def _board_setup(self):
        y = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i in range(0, len(y)):
            self.board.append([y[i] + str(x) for x in range(1, 9)])

    def __str__(self):
        '''This just builds the actual board seen by the 'end-user' '''
        rep_board = ''

        for dicts in self.current:
            rep_board += (
                                     "\n" + Back.LIGHTBLACK_EX + "|¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯|" + Back.RESET + "\n" + Back.LIGHTBLACK_EX + '|' + Back.RESET +
                                     (Back.LIGHTBLACK_EX + "||").join([Back.LIGHTBLACK_EX + ' ' + k
                                                                       + ': ' + Back.LIGHTBLACK_EX + Style.BRIGHT + (
                                                                           Fore.LIGHTWHITE_EX + Style.BRIGHT if i.owner == 'White'
                                                                           else Fore.BLACK + Style.BRIGHT if i.owner == 'Black'
                                                                           else Fore.RESET) + str(i)
                                                                       + ('   ' if str(i) == ' ' else '')
                                                                       + Fore.RESET for k, i in dicts.items()
                                                                       ]) + Back.LIGHTBLACK_EX + "|" + Back.RESET
                                     + "\n" + Back.LIGHTBLACK_EX + "|_________||_________||_________||_________||_________||_________||_________||_________|") + Back.RESET + '\n'

        return rep_board


s = Chessgame()

# testing stuff
print(s)
print(s.current)
s._current_state_raw['d4'] = Chessgame.King('White')
print(str(s._current_state_raw['d4']))
for dict in s.current:
    if 'd4' in dict.keys(): dict['d4'] = s._current_state_raw['d4']
print(s)
print((s._current_state_raw['d4']).move_range(s._current_state_raw))
w = (s._current_state_raw['h8']).owner
print(w)

s._king_check_function('White')
print(s.king_check['White'])
