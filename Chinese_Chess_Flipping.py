#!/usr/bin/env python3
import os
import random

VALID_POSITION = [str(r * 10 + c) for r in range(1, 5) for c in range(1, 9)]  # 有效行列数输入


class Piece:
    def __init__(self, c, l, w):
        """
        :param c: color of the piece, True for red, False for black
        :param l: level of the piece, 7 for 帥將, 6 for 仕士, 5 for 相象, 4 for 俥車, 3 for 傌馬, 2 for 砲包, 1 for 兵卒
        :param w: word to show on the piece
        """
        self.color = c
        self.level = l
        self.word = w
        self.displayed = False

    def can_kill(self, piece):
        if self.level == 7 and piece.level == 1:
            return False  # 将帅不能吃兵卒
        elif self.level == 1 and piece.level == 7:
            return True  # 兵卒可以吃将帅
        elif self.level == 2:
            return False  # 炮不能吃相邻子
        else:
            return self.level >= piece.level  # 大子吃小子


class Player:
    def __init__(self, c):
        """
        :param c: color of the player, True for red, False for black
        """
        self.color = c
        self.name = "红方（帥仕相俥傌砲兵）" if c else "黑方（將士象車馬包卒）"

    def turn(self, bd, rdl, bdl):
        """
        Flip, move, surrender or draw
        :param bd: board
        :param rdl: red_death_list
        :param bdl: black_death_list
        :return: 0 if flip or move successfully; 1 if want to reselect; 2 if want to surrender; 3 if want to draw
        """
        while True:
            a = input("请" + self.name + "输入选择棋子所在行列数（例：11），输入RS认输、输入TH提和，按回车键结束：")
            if a.upper() == "RS":  # 认输
                return 2
            elif a.upper() == "TH":  # 提和
                return 3
            elif a in VALID_POSITION:  # 有效行列数
                row, col = int(a[0]), int(a[1])
                piece = bd[row - 1][col - 1]
                if piece is None:
                    print("此位置没有棋子！")
                else:
                    if piece.displayed and piece.color != self.color:  # 棋子为翻开但不属于自己
                        print("请选择您的棋子！")
                    else:
                        break
            else:
                print("请输入有效行列数或认输/提和请求！")
        if piece.displayed:  # 走棋
            while True:
                b = input("请" + self.name + "输入选择棋子目标行列数（例：11），不输入则重新选择棋子，按回车键结束：")
                if b == "":  # 无输入重新选子
                    return 1
                elif b in VALID_POSITION:  # 有效行列数
                    t_row, t_col = int(b[0]), int(b[1])
                    if t_row != row and t_col != col:
                        print("不能走斜线！")
                    else:
                        target = bd[t_row - 1][t_col - 1]
                        if target is None:  # 目标位置无棋子
                            if abs(t_row - row) == 1 or abs(t_col - col) == 1:  # 只走一格有效
                                bd[t_row - 1][t_col - 1] = piece
                                bd[row - 1][col - 1] = None
                                return 0
                            else:
                                print("只能走一格！")
                        else:  # 目标位置有棋子
                            if target.displayed and target.color != piece.color:  # 目标位置棋子为翻开且为对方
                                if piece.level == 2:  # 走棋为炮
                                    n_inside = 0
                                    if t_row == row:  # 横打炮
                                        min_col, max_col = min(col, t_col), max(col, t_col)
                                        for inside_col in range(min_col + 1, max_col):
                                            if bd[row - 1][inside_col - 1] is not None:  # 中间有隔子
                                                n_inside += 1
                                    else:  # 竖打炮
                                        min_row, max_row = min(row, t_row), max(row, t_row)
                                        for inside_row in range(min_row + 1, max_row):
                                            if bd[inside_row - 1][col - 1] is not None:  # 中间有隔子
                                                n_inside += 1
                                    if n_inside == 1:  # 中间只隔一子
                                        bd[t_row - 1][t_col - 1] = piece
                                        bd[row - 1][col - 1] = None
                                        if target.color:  # 阵亡子为红色
                                            rdl.append(target)
                                        else:  # 阵亡子为黑色
                                            bdl.append(target)
                                        return 0
                                    else:  # 中间不隔子或隔多子
                                        print("中间必须隔有且仅有一个棋子！")
                                else:  # 其它棋子
                                    if abs(t_row - row) == 1 or abs(t_col - col) == 1:  # 只走一格有效
                                        if piece.can_kill(target):  # 可以吃子
                                            bd[t_row - 1][t_col - 1] = piece
                                            bd[row - 1][col - 1] = None
                                            if target.color:  # 阵亡子为红色
                                                rdl.append(target)
                                            else:  # 阵亡子为黑色
                                                bdl.append(target)
                                            return 0
                                        else:
                                            print("无法吃子！")
                                    else:
                                        print("只能走一格！")
                            else:  # 目标位置棋子没翻开或为己方
                                print("走棋无效！")
                else:
                    print("请输入有效行列数！")
        else:  # 翻棋
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
    红方阵亡：……
    黑方阵亡：……
    """
    _ = os.system("cls")
    print("|----|----|----|----|----|----|----|----|")
    for row in bd:
        row_to_print = []
        for piece in row:
            if piece is None:  # 没有棋子
                row_to_print.append("  ")
            else:  # 有棋子
                if piece.displayed:  # 棋子为翻开
                    row_to_print.append(piece.word)
                else:  # 棋子为没有翻开
                    row_to_print.append("〇")
        print("| " + " | ".join(row_to_print) + " |\n|----|----|----|----|----|----|----|----|")
    print("红方阵亡：", end="")
    print_death_list(rdl)
    print("黑方阵亡：", end="")
    print_death_list(bdl)


if __name__ == "__main__":
    _ = input("""游戏规则：
1、象棋棋子反转分布在4×8的棋盘空格上，双方轮流翻棋或走棋，先行者翻出第一个棋子后，则确定该玩家持此种颜色棋子；
2、走棋每步走一格，上下左右都可以；
3、大小比较：帥(將) > 仕(士) > 相(象) > 俥(車) > 傌(馬) > 砲(包) > 兵(卒)，大子可以吃小子，同级可以互吃；
4、帥(將)不能吃卒(兵)，反而被卒(兵)吃；
5、砲(包)吃子时不受大小限制且横向或竖向走棋不受距离限制，但中间必须隔有且仅有一个棋子；
6、棋子被吃光则判负，也可主动发出认输请求（十步以内无法认输），发出提和请求且对方同意则和棋；
7、了解游戏规则后，按回车键开始游戏！""")
    board = shuffle()
    red_death_list, black_death_list = [], []
    print_board(board, red_death_list, black_death_list)
    while True:
        first_a = input("请第一位玩家输入选择棋子所在行列数（例：11），按回车键结束：")
        if first_a in VALID_POSITION:  # 有效行列数
            first_row, first_col = int(first_a[0]), int(first_a[1])
            first_piece = board[first_row - 1][first_col - 1]
            break
        else:
            print("请输入有效行列数！")
    first_piece.displayed = True  # 第一回合只能翻棋然后确定双方颜色
    print_board(board, red_death_list, black_death_list)
    player1 = Player(first_piece.color)
    player2 = Player(not first_piece.color)
    n_turn = 2
    while len(red_death_list) < 16 and len(black_death_list) < 16:
        if n_turn % 2 == 0:  # player2
            result = player2.turn(board, red_death_list, black_death_list)
        else:  # player1
            result = player1.turn(board, red_death_list, black_death_list)
        if result == 0:  # Successful turn
            print_board(board, red_death_list, black_death_list)
            n_turn += 1
        elif result == 2:  # 认输
            if n_turn <= 10:  # 十步以内
                print("十步以内无法认输！")
            else:  # 超过十步
                confirm = input("输入Y确定认输、其他字符继续游戏，按回车键结束：")
                if confirm.upper() == "Y":  # 确定认输
                    winner_color = player1.color if n_turn % 2 == 0 else player2.color
                    print("恭喜红方获胜！" if winner_color else "恭喜黑方获胜！")
                    break
        elif result == 3:  # 提和
            confirm_name = player1.name if n_turn % 2 == 0 else player2.name
            confirm = input("请" + confirm_name + "输入Y同意和棋、其他字符拒绝和棋，按回车键结束：")
            if confirm.upper() == "Y":  # 同意和棋
                print("和棋！")
                break
    else:  # 某一方棋子被吃光
        print("恭喜黑方获胜！" if len(red_death_list) == 16 else "恭喜红方获胜！")
