from colorama import init, Fore, Back, Style
init(autoreset=True)
import time
import random as r

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
        self.turn_count = 0
        self.pseudoai = 'no'

    class Dummy():

        """
        This is the object used in blank spaces, given that it doesn't really take up any memory it's worth it for
        the convenience alone
        """

        def __init__(self):
            self.owner = 'None'
            self.piece = "Not a Piece"
        def __str__(self):
            return ' '

        def getpos(self, current_state_raw):
            self.position = "".join([k for k, v in current_state_raw.items() if self == current_state_raw[k]])

    class Piece():
        ''' Each subclass of the piece object has it\'s own function for checking the movment range against the
    imputted move. Currently the way most of them work is by testing every appicable string combination for a given piece
    (i.e. a-z,5 or a,1-5 for a rook) and discarding the ones that are invalid

    '''
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

        def move_range(self, current_state_raw, is_king_check=False):
            if self.owner == 'Black':
                foreward = chr(ord(self.position[0]) - 1) + self.position[1]
                if foreward[0] not in 'abcdefgh' or foreward[1] not in '12345678' \
                        or (current_state_raw[foreward]).owner != 'None':
                    foreward = -1
                avbmove = foreward if foreward != -1 else ['00']
                potatck = [chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1),
                           chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1)]
            if self.owner == 'White':
                foreward = chr(ord(self.position[0]) + 1) + self.position[1]
                if foreward[0] not in 'abcdefgh' or foreward[1] not in '12345678' \
                        or (current_state_raw[foreward]).owner != 'None':
                    foreward = -1
                avbmove = foreward if foreward != -1 else ['00']
                potatck = [chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1),
                           chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1)]
            if is_king_check == True:
                return potatck
            else:
                potatck = [p for p in potatck if p[0] in 'abcdefgh' and p[1] in '12345678']
                potatck = [p for p in potatck if
                       (current_state_raw[p]).owner != self.owner and (current_state_raw[p]).owner != 'None']
                if avbmove != ['00']: potatck.append(avbmove)

                return potatck

    class Rook(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Twr'

        def move_range(self, current_state_raw, is_king_check=False):
            moves = []
            e, f, g, h = self.position, self.position, self.position, self.position
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
                        if is_king_check and (current_state_raw[x]).piece == 'Kng':
                            moves.append(x)
                        else:
                            moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                e, f, g, h = abcd
            return moves

    class Bishop(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Bsp'

        def move_range(self, current_state_raw, is_king_check=False):
            a, b, c, d = self.position, self.position, self.position, self.position
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
                        if is_king_check and (current_state_raw[x]).piece == 'Kng':
                            moves.append(x)
                        else:
                            moves.append(pots.pop(pots.index(x)))

                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                a, b, c, d = abcd
            return moves

    class Knight(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Knt'

        def move_range(self, current_state_raw, *args):
            potmoves = \
                [chr(ord(self.position[0]) + 2) + str(int(self.position[1]) - 1),
                 chr(ord(self.position[0]) + 2) + str(int(self.position[1]) + 1),
                 chr(ord(self.position[0]) - 2) + str(int(self.position[1]) - 1),
                 chr(ord(self.position[0]) - 2) + str(int(self.position[1]) + 1),
                 chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 2),
                 chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 2),
                 chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 2),
                 chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 2)]
            potmoves = [x for x in potmoves if x[1] in '12345678' and '0' not in x[1:] and x[0] in 'abcdefgh']
            potmoves = [x for x in potmoves if (current_state_raw[x]).owner != self.owner]
            return potmoves

    class Queen(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Qun'

        def move_range(self, current_state_raw, is_king_check=False):
            a, b, c, d, e, f, g, h = self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
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
                        if is_king_check:
                            if (current_state_raw[x]).piece == 'Kng':
                                moves.append(x)
                            else:
                                moves.append(pots.pop(pots.index(x)))
                for x in pots: moves.append(x)
                for x in abcd: abcd[abcd.index(x)] = -1 if x not in pots else x
                if set(abcd) == {-1}:
                    break
                a, b, c, d, e, f, g, h = abcd
            return moves

    class King(Piece):
        def __init__(self, playerID):
            super().__init__(playerID)
            self.piece = 'Kng'

        def move_range(self, current_state_raw, king_check=False):
            a, b, c, d, e, f, g, h = self.position, self.position, self.position, self.position, self.position, self.position, self.position, self.position
            move_limits = []
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
                for x in pots: moves.append(x)
                return moves

            return moves

    def _king_check_function(self):

        self.king_check[self.current_player] = []
        for k, v in self._current_state_raw.items():
            if v.owner != self.current_player and v.owner in ['Black', 'White']:
                self.king_check[self.current_player] += v.move_range(self._current_state_raw, True)
            if v.owner == self.current_player and v.piece == 'Kng':
                self.king_pos, self.king = k, v

        if self.king_pos in self.king_check[self.current_player]:
            self.is_in_check = True
        else:
            self.is_in_check = False

    def _position_setup(self):
        '''
        This builds the intial chess board, calling constructors for all the chess pieces as well as a 'Dummy' piece to
        occupy empty spaces

        '''
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
            [v.getpos(self._current_state_raw) for k, v in self._current_state_raw.items()]

    def _board_setup(self):
        y = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i in range(0, len(y)):
            self.board.append([y[i] + str(x) for x in range(1, 9)])

    def piece_selector(self):

        if self.pseudoAI == 'yes':
            choices = [k for k, v in self._current_state_raw.items() if v.owner == self.current_player]
            select = choices[r.randint(0, len(choices) - 1)]
            self.current_piece = self._current_state_raw[select]
            return

        while 1 == 1:

            select = input('What piece would you like to move ?\n'
                           '(select piece from coordinates or 0 to exit)')
            if select == '0': exit()
            if select not in self._current_state_raw.keys():
                print('Invalid cordinates')
                continue
            elif (self._current_state_raw[select]).owner != self.current_player:
                print('This is not you piece!')
            else:
                self.current_piece = self._current_state_raw[select]
                return

    def move_selector(self):
        # TODO - Allow other pieces to be used to get the king out of check(if in check)
        potential_moves = self.current_piece.move_range(self._current_state_raw)

        if self.pseudoAI == 'yes':
            if self.is_in_check:
                self.current_piece = self.king
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                potential_moves = [x for x in potential_moves if x not in self.king_check[self.current_player]]
                if not potential_moves:
                    print('Player ' + self.current_player + ' has been forced into checkmate')
                    leave = 1
                    return leave
            elif (self.current_piece).piece == 'Kng':
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                potential_moves = [x for x in potential_moves if x not in self.king_check[self.current_player]]
                while not potential_moves:
                    self.piece_selector()
                    potential_moves = (self.current_piece).move_range(self._current_state_raw)
            else:
                while not potential_moves:
                    self.piece_selector()
                    potential_moves = (self.current_piece).move_range(self._current_state_raw)
            # print(s.__str__(True, potential_moves))

            for x in potential_moves:
                if (self._current_state_raw[x]).owner != self.current_player and self._current_state_raw[x] != 'None':
                    move = x
                else:
                    move = potential_moves[r.randint(0, len(potential_moves) - 1)]
            if (self.current_piece).piece == 'Pwn':
                if move[0] in 'ah':
                    holder = self.current_piece.position
                    self.current_piece = self.Queen(self.current_player)
                    (self.current_piece).position = holder
            replacer = self.current_piece.position
            self._current_state_raw[move] = self.current_piece
            (self.current_piece).position = move
            self._current_state_raw[replacer] = self.Dummy()
            for dict in self.current:
                for x in dict.keys(): dict[x] = self._current_state_raw[x]
            if self.pseudoAI == 'no': print(self)
            return

        #TODO match this section with the one above
        while 1 == 1:
            if self.is_in_check:
                self.current_piece = self.king
                potential_moves = (self.current_piece).move_range(self._current_state_raw)
                if not potential_moves:
                    exit('Player' + self.current_player + 'Has been forced into checkmate')
            move = input('Select where you would like to move this piece \n'
                         'or imput \'moves\' to show possible moves ')
            if move == '0':
                exit(print('Thanks for playing!'))
            if move == 'moves':
                print(s.__str__(True, potential_moves))
            elif move not in potential_moves:
                print('This is not a valid destination')
            else:
                confirm = input('Confirm move' + (self.current_piece).position + '--->' + move)
                if 'y' in confirm:
                    self._current_state_raw[move] = self.current_piece
                    self._current_state_raw[(self.current_piece).position] = self.Dummy()
                    for dict in self.current:
                        for x in dict.keys(): dict[x] = self._current_state_raw[x]
                    print(self)
                    return
                    # this will likely be how changes are incorporated

    def play_game(self):
        # TODO update to match the autotester
        while True:
            players = ['n/a', 'White', 'Black']
            leave = 0
            i = -1
            while not leave:
                i = -i
                self.current_player = players[i]
                print('\n----------' + self.current_player + '\'s Turn!' + '----------\n')
                if self.is_in_check:
                    print('The' + self.current_player + '\'s king is in check!')
                    self.move_selector() if not leave else leave
                else:
                    self.piece_selector() if not leave else leave
                    self.move_selector() if not leave else leave

    def _play_game_TESTER_ONLY(self):
        self.pseudoAI = 'yes'
        turncount = 0
        leave = 0
        i = -1
        players = ['na', 'White', 'Black']
        while turncount <= 150 and not leave:
            i = -i
            turncount += 1
                self.current_player = players[i]

            #print('----------' + self.current_player + '\'s Turn!' + '----------')
                self._king_check_function()
            if self.is_in_check:
                # print('\n-----The ' + self.current_player + 'king is in check!-----\n')
                leave = self.move_selector()
            else:
                    self.piece_selector()
                    self.move_selector()
        winner = players[-i] if leave else 'None'
        return turncount, winner

    def __str__(self, showmoves=False, moves=[]):

        """This just builds the actual board seen by the 'end-user' """

        rep_board = ''
        if showmoves == True:  # Outputs the board with the avalible moves for a given piece highlighted
            for dicts in self.current:
                rep_board += (
                                     "\n" + Back.LIGHTBLACK_EX + "|¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯||¯¯¯¯¯¯¯¯¯|" + Back.RESET + "\n" + Back.LIGHTBLACK_EX + '|' + Back.RESET +
                                     (Back.LIGHTBLACK_EX + "||").join([(Back.MAGENTA if k in moves else
                                                                        Back.LIGHTBLACK_EX if k != self.current_piece.position
                                                                        else Fore.YELLOW + Back.LIGHTBLACK_EX) + ' ' + k
                                                                       + ': ' +
                                                                       (Back.MAGENTA if k in moves else
                                                                        Back.LIGHTBLACK_EX) + Style.BRIGHT + (
                                                                           Fore.YELLOW if k == (
                                                                               self.current_piece).position and self.is_in_check != True \
                                                                               else Fore.LIGHTWHITE_EX + Style.BRIGHT if i.owner == 'White'
                                                                           else Fore.BLACK + Style.BRIGHT if i.owner == 'Black'
                                                                           else Fore.RESET) + str(i)
                                                                       + ('   ' if str(i) == ' ' else '')
                                                                       + Fore.RESET for k, i in
                                                                       dicts.items()]) + Back.LIGHTBLACK_EX + "|" + Back.RESET
                                     + "\n" + Back.LIGHTBLACK_EX + "|_________||_________||_________||_________||_________||_________||_________||_________|") + Back.RESET + '\n'

        else:
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

        return '\n' + rep_board + '\n'




# testing stuff
i = 0
z = []
timezero = time.time()
while i < 10000:
    inittime = time.time()
    s = Chessgame()
    z.append(s._play_game_TESTER_ONLY())
    z.append([x for x, y in s._current_state_raw.items() if y.piece == 'Kng'])
    del s
    i += 1
    runtime = time.time() - inittime
    totaltime = time.time() - timezero
    rt = time.gmtime(runtime)
    print(rt, runtime, totaltime)

print(z)
