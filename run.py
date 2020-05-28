from flask import Flask, redirect, url_for, request, make_response, session, flash
from flask.templating import render_template
import sqlite3

app = Flask(__name__)
app.secret_key = "random secret key"

@app.route('/')
def indexFun():
    conn = sqlite3.connect('gameroomRPS.db')
    # conn.execute('DROP TABLE IF EXISTS gameRoom')
    conn.execute('CREATE TABLE IF NOT EXISTS gameRoom (GameID TEXT, P1Move TEXT, P2Move TEXT)')
    conn.close()
    return render_template("index.html")

@app.route('/sudoku')
def sudoku():
    print("In sudoku")
    return render_template("sudoku.html")

@app.route('/rockPaperScissors/')
def rockPaperScissors():
    conn = sqlite3.connect('gameroomRPS.db')
    conn.row_factory = sqlite3.Row
    conn = conn.cursor()
    conn.execute('SELECT * FROM gameRoom')
    rows = conn.fetchall();
    return render_template('rockPaperScissors.html', rows = rows)

@app.route('/gameRoomDbWrite/', methods = ['POST'])
def gameRoomDbWrite():
    session['username'] = request.form['username']
    if request.method == 'POST':
        try:
            room = request.form['roomId']
            session['room'] = room
            print(room)

            with sqlite3.connect('gameroomRPS.db') as conn:
                print("1")
                conn.row_factory = sqlite3.Row
                print("1")
                cur = conn.cursor()
                print("1")
                cur.execute("SELECT * FROM gameRoom WHERE GameID = ?",(room))
                print("1")
                session['player'] = 'P2'
                rows = cur.fetchall()
                print("1")
                if len(rows) == 0:
                    cur.execute("INSERT INTO gameRoom (GameID, P1Move, P2Move) VALUES(?,?,?)", (room,"None", "None"))
                    cur.execute("SELECT * FROM gameRoom WHERE GameID = ?",(room))
                    session['player'] = 'P1'
                    rows = cur.fetchall()
                print("1")
                return render_template('playRockPaperScissors.html', rows = rows)
        except:
            print("***** ERROR *****")
            return render_template('index.html')
    return render_template('index.html')

@app.route('/playRockPaperScissors', methods = ['POST'])
def playRockPaperScissors():
    if request.method == 'POST':
        try:
            op = request.form['ans']
            session['sel'] = op
            print("2")
            with sqlite3.connect('gameroomRPS.db') as conn:
                print("2")
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                if session['player'] == 'P1':
                    print("2")
                    cur.execute("UPDATE gameRoom SET P1Move = ? WHERE GameID = ?", (op, session['room']))
                    print("2")
                    cur.execute("SELECT * FROM gameRoom WHERE GameID = ?", (session['room']))
                    print("2")
                    rows = cur.fetchall()
                    print("2")
                    return render_template('playRockPaperScissors.html', rows = rows)
                else:
                    cur.execute("UPDATE gameRoom SET P2Move = ? WHERE GameID = ?", (op, session['room']))
                    cur.execute("SELECT * FROM gameRoom WHERE GameID = ?", (session['room']))
                    rows = cur.fetchall()
                    return render_template('playRockPaperScissors.html', rows = rows)
        except:
            print("** ERROR **")
    cur.execute("SELECT * FROM gameRoom WHERE GameID = ?",(session['room']))
    rows = cur.fetchall()
    return render_template('playRockPaperScissors.html', rows = rows)

@app.route('/RPSWin/', methods = ['POST'])
def RPSWin():
    with sqlite3.connect('gameroomRPS.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute('SELECT P1Move, P2Move FROM gameRoom WHERE GameID = ?', (session['room']))
        rows = cur.fetchall()
        x = False
        winner = 'P1'
        for r in rows:
            if r[0] == "Rock" or r[0] == "Paper" or r[0] == "Scissors":
                if r[1] == "Rock" or r[1] == "Paper" or r[1] == "Scissors":
                    for r in rows:
                        if r[0] == 'Rock':
                            if r[1] == 'Scissors':
                                winner = 'P1'
                            elif r[1] == 'Rock':
                                winner = 'None'
                            else:
                                winner = 'P2'
                        elif r[0] == 'Paper':
                            if r[1] == 'Scissors':
                                winner = 'P2'
                            elif r[1] == 'Paper':
                                winner = 'None'
                            else:
                                winner = 'P2'
                        else:
                            if r[1] == 'Paper':
                                winner = 'P1'
                            elif r[1] == 'Scissors':
                                winner = 'None'
                            else:
                                winner = 'P2'
                        flash("Winner is " + winner)
                else:
                    flash("Wait for another player")
                    return render_template('playRockPaperScissors.html')
        return render_template('playRockPaperScissors.html')

if __name__ == '__main__':
    app.run(debug = True)