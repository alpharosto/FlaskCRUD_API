from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import sqlite3
DATABASE ='word.db'

app = Flask(__name__)
app.config['http://localhost:5000'] = 'mysql+pymysql://mysql_app:1234@mysql_host:mysql_3000/mysql_db'

db =SQLAlchemy(app)



def get_db():
    db = getattr(app ,'_database' ,None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        app.batabase =db 
        return db
    
# creatting a table
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT
        )
    ''')
    conn.commit()
    
#create new word in db
@app.route('/words', methods=['POST'])
def create_word():
    word = request.json.get('word')

    if word:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
        conn.commit()
        return jsonify({"message": "Word created successfully!"}), 201
    else:
        return jsonify({"error": "Invalid request"}), 400
    
#read all word from data
@app.route('/words', methods=['GET'])
def read_words():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words")
    rows = cursor.fetchall()

    if rows:
        words = [{'id': row[0], 'word': row[1]} for row in rows]
        return jsonify(words), 200
    else:
        return jsonify({"message": "No words found in the database."}), 404


#update data
@app.route('/words/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    new_word = request.json.get('word')

    if new_word:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE words SET word = ? WHERE id = ?", (new_word, word_id))
        conn.commit()
        return jsonify({"message": "Word updated successfully!"}), 200
    else:
        return jsonify({"error": "Invalid request"}), 400
#delete
@app.route('/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
    conn.commit()
    return jsonify({"message": "Word deleted successfully!"}), 200


if __name__ == '__main__':
    create_table()
    app.run()
