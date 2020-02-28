# 中国象棋翻棋 Chinese Chess Flipping

[中文描述](https://github.com/Zhiyu-Lei/Chinese_Chess_Flipping#中文) | [English Description](https://github.com/Zhiyu-Lei/Chinese_Chess_Flipping#English)

## 中文
本游戏为中国象棋的一种特殊玩法，主要规则如下：
1. 象棋棋子反转分布在4×8的棋盘空格上，双方轮流翻棋或走棋，先行者翻出第一个棋子后，则确定该玩家持此种颜色棋子；
2. 走棋每步走一格，上下左右都可以；
3. 大小比较：帥(將) > 仕(士) > 相(象) > 俥(車) > 傌(馬) > 砲(包) > 兵(卒)，大子可以吃小子，同级可以互吃（取决于谁走棋）；
4. 帥(將)不能吃卒(兵)，反而被卒(兵)吃；
5. 砲(包)吃子时不受大小限制且横向或竖向走棋不受距离限制，但中间必须隔有且仅有一个棋子；
6. 棋子被吃光则判负，也可主动发出认输请求（十步以内无法认输），发出提和请求且对方同意则和棋。

详细规则请参考[百度百科相关词条](https://baike.baidu.com/item/%E6%9A%97%E6%A3%8B/3547791?fr=aladdin)！

---
启动程序（在项目目录下输入`python Chinese_Chess_Flipping.py`命令）后会先介绍规则，按回车键正式开始游戏。双方自行决定谁先谁后，先手开始翻棋，并确定双方颜色后轮流行动。

每次行动可以：
1. 翻棋：需输入一个两位数，第一位是棋子所在行数、第二位是棋子所在列数，这个棋子必须处于没翻开状态；
2. 走棋（吃子）：需连续输入两个两位数，第一个两位数的两位分别表示棋子所在行数与列数、这个棋子必须处于翻开状态且属于自己，第二个两位数的两位分别表示棋子目标位置的行数与列数、这步走棋（吃子）必须符合规则，若不输入第二个两位数则重新选择棋子；
3. 发出认输请求：输入`RS`（必须十步以后），然后输入`Y`确认认输，否则游戏继续；
4. 发出提和请求：输入`TH`，然后对方输入`Y`同意和棋，否则拒绝和棋、游戏继续。

每次翻棋或走棋（吃子）后，棋盘会刷新在命令行中，空格表示该位置没有棋子，〇表示该位置棋子没有翻开。

当某一方棋子被吃光或主动发出认输请求或双方同意和棋时，游戏结束，程序自动终止。

### 项目未来计划：
+ 增加长捉判负、相同局面反复出现自动判和等功能；
+ 利用期望极小化极大算法设计AI实现人机对战；
+ 实现AI辅助对战（即程序本身不存储棋盘信息，棋盘信息根据外部实际对战局面输入，AI根据局面做出合理决策）

---
---
## English
This game is a special version of Chinese Chess. Major rules are as follows:
1. All pieces are placed on a 4 by 8 chessboard, with reverse sides facing up. Two players make flips or moves in turn. After the first player makes the first flip, that player will play the color of the piece flipped.
2. One grid is allowed in each move, with any directions of up, down, left, or right.
3. Level ranking of the pieces: 帥(將) (General) > 仕(士) (Mandarin) > 相(象) (Bishop) > 俥(車) (Rook) > 傌(馬) (Knight) > 砲(包) (Cannon) > 兵(卒) (Pawn), where 帥, 仕, 相, 俥, 傌, 砲, 兵 are for red, while 將, 士, 象, 車, 馬, 包, 卒 are for black. Pieces with higher levels can kill pieces with lower levels. Pieces with the same levels can kill each other (depending on whose turn).
4. Generals cannot kill Pawns, but will be killed by Pawns instead.
5. When Cannons kill other pieces, there are no level-ranking restrictions nor distance restrictions in horizontal or vertical directions, but there must be only one piece between Cannon and its target.
6. One loses if all the pieces are killed. Surrender is allowed after 10 turns. A draw is reached if one makes a draw request and the other agrees.

For more detailed rules, please refer to [information on Wikipedia](https://en.wikipedia.org/wiki/Banqi)!

---
Run `python Chinese_Chess_Flipping.py` command under the project directory, and the rules will be introduced first. The game will start after Enter key is pressed. Two players determine who plays first on their own, and then play in turn after the first one makes the first flip and colors of the two players are determined.

The followings are allowed in each turn:
1. Making a flip: A two-digit number is required for input. The first digit indicates which row the piece is in, and the second indicates which column the piece is in. The piece must have reverse side facing up.
2. Making a move (killing an enemy piece): Two two-digit numbers are required for input. The two digits of the first number indicate the row and the column of the piece to move. The piece must have front side facing up and belong to the player making the move. The two digits of the second number indicate the row and the column of the target of the piece. Such move (killing) must conform to the rules. If there is no input for the second number, then the player can reselect the piece to move.
3. Making a surrender request: Input `RS` (only allowed after 10 turns), and input `Y` to confirm; otherwise the game continues.
4. Making a draw request: Input `TH`. Then, the opponent inputs `Y` to agree; otherwise, the draw request is rejected and the game continues.

Each time after making a flip or move (killing), the chessboard will be refreshed on the console. An empty space indicates there is no piece at that grid. A "〇" indicates the piece at that grid has reverse side facing up.

When a player has all pieces killed or makes a surrender request, or two players both agree to draw, the game is over and the program terminates automatically.

### Future Plans of This Project:
+ More features available: auto losing judgement if one continuously chases an enemy piece; auto draw judgement if same states appear repeatedly...
+ Using __Expected-Minimax Algorithm__ to design an AI for human-machine competition.
+ AI assisted game, i.e. the program itself does not store information about the chessboard, which instead is inputted according to the real game outside, and the AI makes reasonable decisons for the outside game.
