from flask import Flask, render_template, redirect
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/start-game')
def start_game():
    # Launch your game.py file
    game_path = os.path.join(os.getcwd(), 'game', 'game.py')
    subprocess.Popen(['python', game_path])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
