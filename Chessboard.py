import random
import Piece


# Reachable
Reachable = 0
Unreachable = 1
SameSide = 2
Hidden = 3
Assaultable = 4
Invulnerable = 5


class Chessboard:
    def __init__(self, isHidden=True):
        roles = ['军旗'] + ['司令'] + ['军长'] + \
                ['炸弹'] * 2 + ['师长'] * 2 + ['旅长'] * 2 + ['团长'] * 2 + ['营长'] * 2 + \
                ['连长'] * 3 + ['排长'] * 3 + ['工兵'] * 3 + ['地雷'] * 3
        pieces = []
        for role in roles:
            if isHidden:
                redPiece = Piece.Piece(role, Piece.Red)
                blackPiece = Piece.Piece(role, Piece.Black)
            else:
                redPiece = Piece.Piece(role, Piece.Red, state=Piece.Revealed)
                blackPiece = Piece.Piece(role, Piece.Black, state=Piece.Revealed)
            pieces.append(redPiece)
            pieces.append(blackPiece)
        random.seed(0)
        random.shuffle(pieces)

        # 行营坐标
        self._campPoses = [(1, 2), (3, 2), (2, 3), (1, 4), (3, 4), (1, 7), (3, 7), (2, 8), (1, 9), (3, 9)]
        # 棋盘
        self._board = [[None for _ in range(5)] for _ in range(12)]
        index = 0
        for i in range(12):
            for j in range(5):
                if (j, i) in self._campPoses:
                    continue
                piece = pieces[index]
                piece.setPos((j, i))
                self._board[i][j] = piece
                index += 1

    def getPiece(self, pos):
        j, i = pos
        assert 0 <= i < 12 and 0 <= j < 5, 'pos must be in [0, 12) × [0, 5)'
        return self._board[i][j]

    def setPiece(self, pos, piece):
        j, i = pos
        assert 0 <= i < 12 and 0 <= j < 5, 'pos must be in [0, 12) × [0, 5)'
        self._board[i][j] = piece

    def clearPiece(self, pos):
        self.setPiece(pos, None)

    def isConnected(self, oldPos, newPos):
        oldJ, oldI = oldPos
        newJ, newI = newPos
        dj = abs(oldJ - newJ)
        di = abs(oldI - newI)
        if di + dj == 1:            # 横竖相邻
            return True
        elif di == 1 and dj == 1:   # 斜相邻
            if oldPos in self._campPoses or newPos in self._campPoses:
                return True
            else:
                return False
        elif dj == 0:               # 同列
            if (newJ == 0 or newJ == 4) and 0 < oldI < 11 and 0 < newI < 11:
                # 判断中间是否有阻挡
                for i in range(oldI + 1, newI):
                    if self.getPiece((newJ, i)) is not None:
                        return False
                return True
            else:
                return False
        elif di == 0:               # 同行
            if newI in [1, 5, 6, 10]:
                # 判断中间是否有阻挡
                for j in range(oldJ + 1, newJ):
                    if self.getPiece((j, newI)) is not None:
                        return False
                return True
            else:
                return False
        else:
            return False

    def isReachable(self, oldPos, newPos):
        oldPiece = self.getPiece(oldPos)
        assert oldPiece is not None, 'oldPiece must not be None'

        newPiece = self.getPiece(newPos)
        if newPiece is None:  # move
            if self.isConnected(oldPos, newPos):
                return Reachable
            else:
                return Unreachable
        else:
            newState = newPiece.getState()
            assert newState in [Piece.Hidden, Piece.Revealed], 'newState must be in [Piece.Hidden, Piece.Revealed]'
            if newState == Piece.Hidden:
                return Hidden
            else:
                oldSide = oldPiece.getSide()
                newSide = newPiece.getSide()
                if oldSide == newSide:
                    return SameSide
                else:
                    if self.isConnected(oldPos, newPos):
                        if newPos in self._campPoses:
                            return Invulnerable
                        else:
                            if oldPiece.compare(newPiece):
                                return Assaultable
                            else:
                                return Invulnerable
                    else:
                        return Unreachable
