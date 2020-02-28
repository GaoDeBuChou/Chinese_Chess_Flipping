#!/usr/bin/env python3
import os
import random

VALID_POSITION = [str(r * 10 + c) for r in range(1, 5) for c in range(1, 9)]  # Valid input for row and column numbers


class Piece:
    def __init__(self, cl, lv, wd):
        """
        :param cl: color of the piece: True for red, False for black
        :param lv: level of the piece: 7 for 帥將 (Generals), 6 for 仕士 (Mandarins), 5 for 相象 (Bishops),
                   4 for 俥車 (Rooks), 3 for 傌馬 (Knights), 2 for 砲包 (Cannons), 1 for 兵卒 (Pawns)
        :param wd: word to show on the piece
        """
        self.color = cl
        self.level = lv
        self.word = wd
        self.displayed = False

    def can_kill(self, piece):
        if self.level == 7 and piece.level == 1:
            return False  # Generals cannot kill Pawns
        elif self.level == 1 and piece.level == 7:
            return True  # Pawns can kill Generals
        elif self.level == 2:
            return False  # Cannons have special way of killing
        else:
            return self.level >= piece.level  # higher levels can kill lower or equal levels


class Player:
    def __init__(self, cl):
        """
        :param cl: color of the player: True for red, False for black
        """
        self.color = cl
        self.cn_name = "红方（帥仕相俥傌砲兵）" if cl else "黑方（將士象車馬包卒）"
        self.en_name = "Red" if cl else "Black"

    def turn(self, bd, rdl, bdl):
        """
        Flip, move, surrender or draw
        :param bd: board
        :param rdl: red_death_list
        :param bdl: black_death_list
        :return: 0 if flip or move successfully; 1 if want to reselect; 2 if want to surrender; 3 if want to draw
        """
        while True:
            print("请" + self.cn_name + "输入选择棋子所在行列数（例：11），输入RS认输、输入TH提和：")
            a = input(self.en_name + ' inputs row and column of selected piece (eg. 11); "RS" for surrender; "TH" for draw: ')
            if a.upper() == "RS":  # surrender request
                return 2
            elif a.upper() == "TH":  # draw request
                return 3
            elif a in VALID_POSITION:  # valid input position
                row, col = int(a[0]), int(a[1])
                piece = bd[row - 1][col - 1]
                if piece is None:  # no piece at selected position
                    print("此位置没有棋子！ No piece at this position!")
                else:  # piece at selected position
                    if piece.displayed and piece.color != self.color:  # player's piece facing up
                        print("请选择您的棋子！ Please select your piece!")
                    else:  # piece facing down or player's piece facing up
                        break
            else:  # invalid input
                print("请输入有效行列数或认输/提和请求！")
                print("Please input valid row and column number or surrender/draw request!")
        if piece.displayed:  # piece facing up, i.e. making a move
            while True:
                print("请" + self.cn_name + "输入选择棋子目标行列数（例：11），不输入则重新选择棋子：")
                b = input(self.en_name + 'inputs row and column of target position (eg. 11); no input to reselect pieces: ')
                if b == "":  # no input, i.e. to reselect piece
                    return 1
                elif b in VALID_POSITION:  # valid input position
                    t_row, t_col = int(b[0]), int(b[1])
                    if t_row != row and t_col != col:  # not moving horizontally or vertically (invalid move)
                        print("不能走斜线！ Only horizontal or vertical move allowed!")
                    else:  # moving horizontally or vertically
                        target = bd[t_row - 1][t_col - 1]
                        if target is None:  # no piece at target position
                            if abs(t_row - row) == 1 or abs(t_col - col) == 1:  # moving one grid
                                bd[t_row - 1][t_col - 1] = piece
                                bd[row - 1][col - 1] = None
                                return 0
                            else:  # not moving one grid (invalid move)
                                print("只能走一格！ Only one grid allowed!")
                        else:  # piece at target position
                            if target.displayed and target.color != piece.color:  # opponent's piece facing up
                                if piece.level == 2:  # moving Cannon
                                    n_inside = 0
                                    if t_row == row:  # moving horizontally
                                        min_col, max_col = min(col, t_col), max(col, t_col)
                                        for inside_col in range(min_col + 1, max_col):
                                            if bd[row - 1][inside_col - 1] is not None:  # pieces between
                                                n_inside += 1
                                    else:  # moving vertically
                                        min_row, max_row = min(row, t_row), max(row, t_row)
                                        for inside_row in range(min_row + 1, max_row):
                                            if bd[inside_row - 1][col - 1] is not None:  # pieces between
                                                n_inside += 1
                                    if n_inside == 1:  # only one piece between
                                        bd[t_row - 1][t_col - 1] = piece
                                        bd[row - 1][col - 1] = None
                                        if target.color:  # red piece killed
                                            rdl.append(target)
                                        else:  # black piece killed
                                            bdl.append(target)
                                        return 0
                                    else:  # no piece or more than one pieces between (invalid killing)
                                        print("中间必须隔有且仅有一个棋子！")
                                        print("There must be only one piece between!")
                                else:  # moving other piece
                                    if abs(t_row - row) == 1 or abs(t_col - col) == 1:  # moving one grid
                                        if piece.can_kill(target):  # can kill target piece
                                            bd[t_row - 1][t_col - 1] = piece
                                            bd[row - 1][col - 1] = None
                                            if target.color:  # red piece killed
                                                rdl.append(target)
                                            else:  # black piece killed
                                                bdl.append(target)
                                            return 0
                                        else:  # cannot kill target piece (invalid killing)
                                            print("无法吃子！ Cannot kill the piece!")
                                    else:  # not moving one grid (invalid move)
                                        print("只能走一格！ Only one grid allowed!")
                            else:  # piece facing down or player's piece facing up (invalid killing)
                                print("走棋无效！ Invalid move!")
                else:  # invalid input
                    print("请输入有效行列数！ Please input valid row and column number!")
        else:  # piece facing down, i.e. making a flip
            piece.displayed = True
            return 0


def shuffle():
    l_piece = [Piece(True, 7, "帥"), Piece(True, 6, "仕"), Piece(True, 6, "仕"), Piece(True, 5, "相"),
               Piece(True, 5, "相"), Piece(True, 4, "俥"), Piece(True, 4, "俥"), Piece(True, 3, "傌"),
               Piece(True, 3, "傌"), Piece(True, 2, "砲"), Piece(True, 2, "砲"), Piece(True, 1, "兵"),
               Piece(True, 1, "兵"), Piece(True, 1, "兵"), Piece(True, 1, "兵"), Piece(True, 1, "兵"),
               Piece(False, 7, "將"), Piece(False, 6, "士"), Piece(False, 6, "士"), Piece(False, 5, "象"),
               Piece(False, 5, "象"), Piece(False, 4, "車"), Piece(False, 4, "車"), Piece(False, 3, "馬"),
               Piece(False, 3, "馬"), Piece(False, 2, "包"), Piece(False, 2, "包"), Piece(False, 1, "卒"),
               Piece(False, 1, "卒"), Piece(False, 1, "卒"), Piece(False, 1, "卒"), Piece(False, 1, "卒")]
    shuffled = random.sample(l_piece, 32)
    return [shuffled[0:8], shuffled[8:16], shuffled[16:24], shuffled[24:32]]


def print_death_list(dl):
    if dl:
        dl.sort(key=lambda p: p.level, reverse=True)
        dl_to_print = [p.word for p in dl]
        print(" ".join(dl_to_print))
    else:
        print("")


def print_board(bd, rdl, bdl):
    """
    |----|----|----|----|----|----|----|----|
    | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 |
    |----|----|----|----|----|----|----|----|
    | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 |
    |----|----|----|----|----|----|----|----|
    | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 |
    |----|----|----|----|----|----|----|----|
    | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 | 棋 |
    |----|----|----|----|----|----|----|----|
    红方阵亡 Red killed：……
    黑方阵亡 Black killed：……
    """
    _ = os.system("cls")
    print("|----|----|----|----|----|----|----|----|")
    for row in bd:
        row_to_print = []
        for piece in row:
            if piece is None:  # no piece at position
                row_to_print.append("  ")
            else:  # piece at position
                if piece.displayed:  # piece facing up
                    row_to_print.append(piece.word)
                else:  # piece facing down
                    row_to_print.append("〇")
        print("| " + " | ".join(row_to_print) + " |\n|----|----|----|----|----|----|----|----|")
    print("红方阵亡  Red killed ：", end="")
    print_death_list(rdl)
    print("黑方阵亡 Black killed：", end="")
    print_death_list(bdl)


if __name__ == "__main__":
    with open("./Rules.txt", encoding="UTF-8") as rules:
        print(rules.read())
    _ = input()
    board = shuffle()
    red_death_list, black_death_list = [], []
    print_board(board, red_death_list, black_death_list)
    while True:
        print("请第一位玩家输入选择棋子所在行列数（例：11）：")
        first_a = input("First player inputs row and column of selected piece (eg. 11): ")
        if first_a in VALID_POSITION:  # valid input position
            first_row, first_col = int(first_a[0]), int(first_a[1])
            first_piece = board[first_row - 1][first_col - 1]
            break
        else:
            print("请输入有效行列数！ Please input valid row and column number!")
    first_piece.displayed = True  # making a flip in the first turn, and colors determined for two players
    print_board(board, red_death_list, black_death_list)
    player1 = Player(first_piece.color)
    player2 = Player(not first_piece.color)
    n_turn = 2
    while len(red_death_list) < 16 and len(black_death_list) < 16:  # both players have pieces not killed
        if n_turn % 2 == 0:  # player2 turn
            result = player2.turn(board, red_death_list, black_death_list)
        else:  # player1 turn
            result = player1.turn(board, red_death_list, black_death_list)
        if result == 0:  # successful turn
            print_board(board, red_death_list, black_death_list)
            n_turn += 1
        elif result == 2:  # surrender request
            if n_turn <= 10:  # within 10 turns
                print("十步以内无法认输！ Surrender not allowed within 10 turns")
            else:  # after 10 turns
                print("输入Y确定认输、其他字符继续游戏：")
                confirm = input('Input "Y" to confirm; otherwise to continue the game: ')
                if confirm.upper() == "Y":  # confirm to surrender
                    winner_color = player1.color if n_turn % 2 == 0 else player2.color
                    print("恭喜红方获胜！ Red wins!" if winner_color else "恭喜黑方获胜！ Black wins!")
                    break
        elif result == 3:  # draw request
            confirm_cn_name = player1.cn_name if n_turn % 2 == 0 else player2.cn_name
            confirm_en_name = player1.en_name if n_turn % 2 == 0 else player2.en_name
            print("请" + confirm_cn_name + "输入Y同意和棋、其他字符拒绝和棋：")
            confirm = input(confirm_en_name + 'inputs "Y" to confirm; otherwise to reject: ')
            if confirm.upper() == "Y":  # confirm to draw
                print("和棋！ Draw!")
                break
    else:  # either player has all pieces killed
        print("恭喜黑方获胜！ Black wins!" if len(red_death_list) == 16 else "恭喜红方获胜！ Red wins!")
