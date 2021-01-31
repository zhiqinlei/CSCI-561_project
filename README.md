# A small version of the GO game AI agent
Developed a 5x5 GO AI by using UCS search, Game playing and reinforcement Learning teniques.

Rules:
- It starts with an empty board,
- Two players take turns placing stones on the board, one stone at a time,
- The players may choose any unoccupied point to play on (except for those forbidden by the
“KO” and “no-suicide” rules).
- Once played, a stone can never be moved and can be taken off the board only if it is captured.
The entire game of Go is played based on two simple rules: Liberty (No-Suicide) and KO.

Komi:
Because Black has the advantage of playing the first move, awarding White some compensation is called
Komi. This is in the form of giving White a compensation of score at the end of the game. In this
homework (a board size of 5x5), Komi for the White player is set to be 5/2 = 2.5.

Passing:
A player may waive his/her right to make a move, called passing, when determining that the game
offers no further opportunities for profitable play. A player may pass his/her turn at any time. Usually, passing is beneficial only at the end of the game, when further moves would be useless or maybe even harmful to a player's position.

End of Game:
A game ends when it reaches one of the four conditions:
- When a player makes an invalid move (invalid stone placement, suicide, violation of KO rule).
- When both players waive their rights to move. Namely, two consecutive passes end the game.
- When the game has reached the maximum number of steps allowed. In this homework (a board
size of 5x5), the maximum number of steps allowed is 5*5-1 = 24.

Winning Condition:
There are various scoring rules and winning criteria for Go. But we will adopt the following rules for this MiniGO.
- “Partial” Area Scoring: A player's partial area score is the number of stones that the player has
occupied on the board.
- Final Scoring: The Black player’s final score is the partial area score, while the White player’s
final score is the sum of the partial area score plus the score of compensation (Komi).
- Winning Criteria:
- If a player makes an invalid move (invalid stone placement, suicide, violation of KO rule),
s/he loses the game.
- If the game reaches the maximum number of steps allowed or if both players waive
their rights to move, the winner is the player that has a higher final score at the end of
the game. For example, in the following board at the end of a game, White’s partial area
score is 10 and Black’s partial area score is 12. White is the winner because
10 + 2.5 = 12.5 > 12 .

Input: 
agent should read input.txt from the current (“work”) directory. The format is as follows:
- Line 1: A value of “1” or “2” indicating which color you play (Black=1, White=2)
- Line 2-6: Description of the previous state of the game board, with 5 lines of 5 values each.
This is the state after your last move. (Black=1, White=2, Unoccupied=0)
- Line 7-11: Description of the current state of the game board, with 5 lines of 5 values each.
This is the state after your opponent’s last move (Black=1, White=2, Unoccupied=0).
For example:
========input.txt========
2
00110
00210
00200
02000
00000
00110
00210
00200
02010
00000
=======================
At the beginning of a game, the default initial values from line 2 - 11 are 0.

Output: 
To make a move, your agent should generate output.txt in the current (“work”) directory.
- The format of placing a stone should be two integers, indicating i and j as in Figure 2, separated
by a comma without whitespace. For example:
========output.txt=======
2,3
=======================
- If your agent waives the right to move, it should write “PASS” (all letters must be in uppercase)
in output.txt. For example:
========output.txt=======
PASS
=======================