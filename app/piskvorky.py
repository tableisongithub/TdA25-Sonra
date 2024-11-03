from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Game:
    def __init__(self, size=16, win_length=5):
        self.size = size
        self.win_length = win_length
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.winner = None

    def is_winner(self, x, y):
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            count = 1
            for step in range(1, self.win_length):
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            for step in range(1, self.win_length):
                nx, ny = x - step * dx, y - step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            if count >= self.win_length:
                self.winner = self.current_player
                return True
        return False

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player
            if self.is_winner(row, col):
                return True
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return False

game = Game()

@app.route("/")
def index():
    return render_template("index.html", game=game)

@app.route("/move", methods=["POST"])
def move():
    row = int(request.form.get("row"))
    col = int(request.form.get("col"))
    game.make_move(row, col)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global game
    game = Game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
