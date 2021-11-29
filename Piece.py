
# role
RoleDict = {'炸弹': 0, '工兵': 1, '排长': 2, '连长': 3, '营长': 4, '团长': 5,
            '旅长': 6, '师长': 7, '军长': 8, '司令': 9, '地雷': 10, '军旗': 11}

# state
Hidden = 0
Revealed = 1
Dead = 2

# side
Red = 0
Black = 1


class Piece:
    def __init__(self, role, side, pos=None, state=Hidden):
        self._role = role       # 棋子角色
        self._state = state     # 棋子状态
        self._pos = pos         # 棋子坐标
        self._side = side       # 棋子阵营

    def setPos(self, pos):
        self._pos = pos

    def setState(self, state):
        self._state = state

    def getPos(self):
        return self._pos

    def getState(self):
        return self._state

    def getSide(self):
        return self._side

    def getRole(self):
        return self._role

    def isMovable(self):
        return self._role not in ['地雷', '军旗']

    def compare(self, piece):
        if self._role == '炸弹' or piece.getRole() == '炸弹':
            return True
        elif self._role in ['地雷', '军旗']:
            return False
        else:
            if piece.getRole() in ['地雷', '军旗']:
                return self._role == '工兵'
            else:
                return RoleDict[self._role] > RoleDict[piece.getRole()]
