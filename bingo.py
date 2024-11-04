import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont

class BingoCard(QWidget):
    def __init__(self):
        super().__init__()

        # カードのパターンを管理するリスト
        self.card_patterns = []

        # カードの生成
        self.create_card()

        # ウィンドウの設定
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('ビンゴ')

        # ボタンの作成
        self.buttons = []
        for i in range(5):
            for j in range(5):
                button = QPushButton(str(self.card[i][j]), self)
                button.setGeometry(j * 40, i * 40, 40, 40)
                button.clicked.connect(lambda checked, row=i, col=j: self.check_number(row, col))
                self.buttons.append(button)

        # 中央のボタンを空白にする
        self.buttons[12].setText("")

        self.show()
        self.bingo_flag = False  # bingo_flag属性の追加


    def create_card(self):
        while True:
            # カードの生成
            b = random.sample(range(1, 16), 5)
            i = random.sample(range(16, 30), 5)  # I列は30まで
            n = random.sample(range(31, 46), 5)
            g = random.sample(range(46, 61), 5)
            o = random.sample(range(61, 76), 5)

            # カードのパターンを文字列化
            card_pattern = ''.join([str(num) for row in [b, i, n, g, o] for num in row])

            # 重複チェック
            if card_pattern not in self.card_patterns:
                self.card_patterns.append(card_pattern)
                self.card = [b, i, n, g, o]
                break

    def check_number(self, row, col):
        if self.bingo_flag:  # ビンゴになっていたら処理を終了
            return

        # 選択したボタンを無効化
        self.buttons[row * 5 + col].setEnabled(False)

        # ビンゴ判定
        self.check_bingo()

    def check_bingo(self):
        # ビンゴになったかどうかを管理するフラグ
        self.bingo_flag = False

        # 行、列、斜めの状態を保持するリスト
        rows = [0] * 5
        cols = [0] * 5
        diag1 = 0
        diag2 = 0

        for i in range(5):
            for j in range(5):
                if not self.buttons[i * 5 + j].isEnabled():
                    rows[i] += 1
                    cols[j] += 1
                    if i == j:
                        diag1 += 1
                    if i + j == 4:
                        diag2 += 1

        if 5 in rows or 5 in cols or diag1 == 5 or diag2 == 5:
            # ビンゴ！
            print("ビンゴです！")
            self.bingo_flag = True
            # すべてのボタンを無効化
            for button in self.buttons:
                button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication([])
    bingo_card = BingoCard()
    app.exec_()