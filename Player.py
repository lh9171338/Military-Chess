import Piece


class Player:
    def __init__(self):
        self._side = None               # 玩家阵营
        self._numMovablePieces = 22     # 玩家可移动棋子数量
        self._numMines = 3              # 玩家地雷数量
        self._numColors = 1             # 玩家军旗数量
        self._currentPiece = None       # 玩家当前操作的棋子

    def init(self, side):
        self._side = side

    def isInit(self):
        return self._side is not None

    def setCurrentPiece(self, piece):
        self._currentPiece = piece

    def getCurrentPiece(self):
        return self._currentPiece

    def clearCurrentPiece(self):
        self._currentPiece = None

    def getSide(self):
        return self._side

    def getNumPieces(self):
        return self._numMovablePieces + self._numMines + self._numColors

    @staticmethod
    def turn(piece):
        assert piece.getState() == Piece.Hidden, 'the state of piece must be Piece.Hidden'
        piece.setState(Piece.Revealed)

    def move(self, newPos):
        assert self._currentPiece is not None, 'current piece must not be None'
        self._currentPiece.setPos(newPos)

    def isEdible(self, piece):
        role = piece.getRole()
        if role == '军旗' and self._numMines > 0:
            return False
        else:
            return True

    def eaten(self, piece):
        assert piece.getState() == Piece.Revealed, 'the state of piece must be Piece.Revealed'
        piece.setState(Piece.Dead)
        role = piece.getRole()
        if role == '军旗':
            self._numColors -= 1
        elif role == '地雷':
            self._numMines -= 1
        else:
            self._numMovablePieces -= 1

    def isLose(self):
        return self._numMovablePieces == 0 or self._numColors == 0
