import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Chessboard
import Piece
import Player


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Variables
        isHidden = False
        self.chessboard = Chessboard.Chessboard(isHidden)   # 棋盘
        self.players = [Player.Player(), Player.Player()]   # 玩家
        self.round = 0                                      # 回合
        self.isFinished = False                             # 游戏是否结束
        if not isHidden:
            self.players[0].init(Piece.Red)
            self.players[1].init(Piece.Black)

        # Parameters
        self.windowSize = (1000, 1200)
        self.imageSize = (1200, 1200)
        self.pushButtonSize = (80, 46)
        self.leftUpperPos = (65, 75)
        self.rightMiddlePos = (788, 478)
        self.leftMiddlePos = (65, 725)
        self.rightBottomPos = (788, 1129)

        # Scale
        qImage = QImage('image/chessboard.png')
        scale = min(self.imageSize[0] / qImage.width(), self.imageSize[1] / qImage.height())
        self.windowSize = self.scalePos(self.windowSize, scale)
        self.imageSize = self.scalePos((qImage.width(), qImage.height()), scale)
        self.pushButtonSize = self.scalePos(self.pushButtonSize, scale)
        self.leftUpperPos = self.scalePos(self.leftUpperPos, scale)
        self.rightMiddlePos = self.scalePos(self.rightMiddlePos, scale)
        self.leftMiddlePos = self.scalePos(self.leftMiddlePos, scale)
        self.rightBottomPos = self.scalePos(self.rightBottomPos, scale)

        # UI
        self.redIcon = QIcon('image/redFlag.png')
        self.blackIcon = QIcon('image/greenFlag.png')
        self.qImage = qImage.scaled(self.imageSize[0], self.imageSize[1])
        self.labelImage = QLabel(self)
        self.pushButtons = [QPushButton(self) for _ in range(60)]

        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layouts = [QVBoxLayout(), QVBoxLayout()]
        self.pushButtonPlayers = [QPushButton(self.redIcon, 'P1'), QPushButton(self.blackIcon, 'P2')]
        self.labelStates = [QLabel(), QLabel()]
        self.labelStates[0].setAlignment(Qt.AlignCenter)
        self.labelStates[1].setAlignment(Qt.AlignCenter)

        self.initUI()

    def initUI(self):
        # Set UI
        self.labelImage.setPixmap(QPixmap.fromImage(self.qImage))
        self.labelImage.setGeometry(0, 0, self.qImage.width(), self.qImage.height())
        self.initPushButtons()

        for i in range(2):
            self.layouts[i].addStretch(1)
            self.layouts[i].addWidget(self.pushButtonPlayers[i])
            self.layouts[i].addWidget(self.labelStates[i])
            self.layouts[i].addStretch(1)
            self.layout.addLayout(self.layouts[i])
        self.widget.setLayout(self.layout)
        self.widget.setGeometry(self.qImage.width(), 0, self.windowSize[0] - self.qImage.width(), self.windowSize[1])

        self.setWindowTitle('Military Chess')
        self.resize(self.windowSize[0], self.windowSize[1])
        self.updateUI()

        # Register callback
        for pushButton in self.pushButtons:
            pushButton.mousePressEvent = self.pushButtonCallback

    @staticmethod
    def scalePos(pos, scale):
        x, y = pos
        x = int(round(x * scale))
        y = int(round(y * scale))
        return x, y

    def figurePos2boardPos(self, pos):
        x, y = pos
        if y <= self.windowSize[1] / 2:
            alpha = float(x - self.leftUpperPos[0]) / (self.rightMiddlePos[0] - self.leftUpperPos[0])
            beta = float(y - self.leftUpperPos[1]) / (self.rightMiddlePos[1] - self.leftUpperPos[1])
            j = alpha * 4
            i = beta * 5
        else:
            alpha = float(x - self.leftMiddlePos[0]) / (self.rightBottomPos[0] - self.leftMiddlePos[0])
            beta = float(y - self.leftMiddlePos[1]) / (self.rightBottomPos[1] - self.leftMiddlePos[1])
            j = alpha * 4
            i = beta * 5 + 6
        j, i = int(round(j)), int(round(i))
        return j, i

    def boardPos2figurePos(self, pos):
        j, i = pos
        if i < 6:
            alpha = 1 - float(j) / 4
            beta = 1 - float(i) / 5
            x = alpha * self.leftUpperPos[0] + (1 - alpha) * self.rightMiddlePos[0]
            y = beta * self.leftUpperPos[1] + (1 - beta) * self.rightMiddlePos[1]
        else:
            alpha = 1 - float(j) / 4
            beta = 1 - float(i - 6) / 5
            x = alpha * self.leftMiddlePos[0] + (1 - alpha) * self.rightBottomPos[0]
            y = beta * self.leftMiddlePos[1] + (1 - beta) * self.rightBottomPos[1]
        x, y = int(round(x)), int(round(y))
        return x, y

    def getPieceFromPos(self, pos):
        j, i = self.figurePos2boardPos(pos)
        return self.chessboard.getPiece((j, i))

    def initPushButtons(self):
        for index, pushButton in enumerate(self.pushButtons):
            i, j = index // 5, index % 5
            figurePos = self.boardPos2figurePos((j, i))
            figurePos = self.scalePos(
                (figurePos[0] - self.pushButtonSize[0] / 2, figurePos[1] - self.pushButtonSize[1] / 2), 1.0)
            pushButton.move(figurePos[0], figurePos[1])
            pushButton.resize(self.pushButtonSize[0], self.pushButtonSize[1])

    def updateUI(self):
        for pushButton in self.pushButtons:
            self.drawPushButton(pushButton)

        for i in range(2):
            player = self.players[i]
            pushButtonPlayer = self.pushButtonPlayers[i]
            labelState = self.labelStates[i]
            labelState.setText(str(player.getNumPieces()))
            if player.isInit():
                if player.getSide() == Piece.Red:
                    pushButtonPlayer.setIcon(self.redIcon)
                else:
                    pushButtonPlayer.setIcon(self.blackIcon)
                pushButtonPlayer.setEnabled(self.isFinished or self.round == i)
            else:
                pushButtonPlayer.setEnabled(False)

            if self.isFinished:
                if player.isLose():
                    labelState.setText('Lose: ' + labelState.text())
                else:
                    labelState.setText('Win: ' + labelState.text())

    def drawPushButton(self, pushButton):
        currentPlayer = self.players[self.round]
        oldPiece = currentPlayer.getCurrentPiece()
        piece = self.getPieceFromPos((pushButton.x(), pushButton.y()))
        if piece is None:
            pushButton.setStyleSheet('background-color:transparent')
            pushButton.setText('')
            if oldPiece is None:
                pushButton.setEnabled(False)
            else:
                pushButton.setEnabled(True)
        else:
            state = piece.getState()
            side = piece.getSide()
            assert state in [Piece.Hidden, Piece.Revealed], 'state must be in [Piece.Hidden, Piece.Revealed]'
            if state == Piece.Hidden:
                pushButton.setStyleSheet('QPushButton{background-color: burlywood;border-radius: 4px;'
                                         'border: 1px gray;border-style: solid}'
                                         'QPushButton:hover{background-color: navajowhite;border-radius: 4px;'
                                         'border: 1px dodgerblue;border-style: solid}')
                pushButton.setEnabled(True)
            else:
                pushButton.setText(piece.getRole())
                if side == Piece.Red:
                    pushButton.setStyleSheet('QPushButton{background-color: gainsboro;color: red;'
                                             'border-radius: 4px;border: 1px gray;border-style: solid}'
                                             'QPushButton:hover{background-color: white;color: red;'
                                             'border-radius: 4px;border: 1px dodgerblue;border-style: solid}')
                else:
                    pushButton.setStyleSheet('QPushButton{background-color: gainsboro;color: forestgreen;'
                                             'border-radius: 4px;border: 1px gray;border-style: solid}'
                                             'QPushButton:hover{background-color: white;color: forestgreen;'
                                             'border-radius: 4px;border: 1px dodgerblue;border-style: solid}')
                font = QFont('幼圆')
                font.setBold(True)
                pushButton.setFont(font)
                if oldPiece is None:
                    pushButton.setEnabled(currentPlayer.getSide() == side and piece.isMovable())
                else:
                    if piece == oldPiece:
                        if side == Piece.Red:
                            pushButton.setStyleSheet('QPushButton{background-color: gainsboro;color: red;'
                                                     'border-radius: 4px;border: 4px red;border-style: solid}')
                        else:
                            pushButton.setStyleSheet('QPushButton{background-color: gainsboro;color: forestgreen;'
                                                     'border-radius: 4px;border: 4px green;border-style: solid}')
                        pushButton.setEnabled(False)
                    else:
                        pushButton.setEnabled(True)
        if self.isFinished:
            pushButton.setEnabled(False)

    def pushButtonCallback(self, event):
        if self.isFinished:
            return

        currentPlayer = self.players[self.round]
        anotherPlayer = self.players[1 - self.round]
        isOptSuccessful = False

        x = event.windowPos().x()
        y = event.windowPos().y()
        figurePos = (x, y)
        piece = self.getPieceFromPos(figurePos)
        pos = self.figurePos2boardPos(figurePos)
        print(figurePos, pos)

        if piece is None:
            oldPiece = currentPlayer.getCurrentPiece()
            assert oldPiece is not None, 'oldPiece must not be None'
            oldPos = oldPiece.getPos()
            result = self.chessboard.isReachable(oldPos, pos)
            if result == Chessboard.Reachable:
                currentPlayer.move(pos)
                self.chessboard.setPiece(pos, oldPiece)
                self.chessboard.clearPiece(oldPos)
                isOptSuccessful = True
        else:
            side = piece.getSide()
            state = piece.getState()
            assert state in [Piece.Hidden, Piece.Revealed], 'state must be in [Piece.Hidden, Piece.Revealed]'

            if currentPlayer.isInit():
                if state == Piece.Hidden:
                    currentPlayer.turn(piece)
                    isOptSuccessful = True
                else:
                    oldPiece = currentPlayer.getCurrentPiece()
                    if oldPiece is None:
                        currentPlayer.setCurrentPiece(piece)
                    else:
                        oldPos = oldPiece.getPos()
                        result = self.chessboard.isReachable(oldPos, pos)
                        if result == Chessboard.SameSide:
                            currentPlayer.setCurrentPiece(piece)
                        elif result == Chessboard.Assaultable and anotherPlayer.isEdible(piece):
                            if piece.compare(oldPiece):
                                currentPlayer.eaten(oldPiece)
                                anotherPlayer.eaten(piece)
                                self.chessboard.clearPiece(oldPos)
                                self.chessboard.clearPiece(pos)
                            else:
                                currentPlayer.move(pos)
                                anotherPlayer.eaten(piece)
                                self.chessboard.setPiece(pos, oldPiece)
                                self.chessboard.clearPiece(oldPos)
                            isOptSuccessful = True
            else:
                if side == Piece.Red:
                    currentPlayer.init(Piece.Red)
                    anotherPlayer.init(Piece.Black)
                else:
                    currentPlayer.init(Piece.Black)
                    anotherPlayer.init(Piece.Red)
                currentPlayer.turn(piece)
                isOptSuccessful = True

        if isOptSuccessful:
            currentPlayer.clearCurrentPiece()
            self.round = 1 - self.round
            self.isFinished = anotherPlayer.isLose() or currentPlayer.isLose()

        self.updateUI()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
