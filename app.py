from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)
DATABASE = "cafes.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cafes = connection.execute('SELECT * FROM cafe').fetchall()
    connection.close()
    return render_template('index.html', cafes=cafes)

@app.route('/add', methods=['GET', 'POST'])
def add_new_cafe():
    if request.method == 'POST':
        data = request.form

        has_wifi = 1 if 'has_wifi' in data else 0
        has_sockets = 1 if 'has_sockets' in data else 0
        has_toilet = 1 if 'has_toilet' in data else 0
        can_take_calls = 1 if 'can_take_calls' in data else 0

        connection = get_db_connection()
        connection.execute('INSERT INTO cafe (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (data['name'], data['map_url'], data['img_url'], data['location'], 'has_sockets', 'has_toilet', 'has_wifi', 'can_take_calls', data['seats'], data['coffee_price']))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    connection = get_db_connection()
    cafe = connection.execute('SELECT * FROM cafe WHERE id = ?', (cafe_id,)).fetchone()
    connection.close()
    if cafe is None:
        return "Cafe not found", 404
    return render_template('cafe_detail.html', cafe=cafe)

@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    connection = get_db_connection()
    connection.execute('DELETE FROM cafe WHERE id = ?', (cafe_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


