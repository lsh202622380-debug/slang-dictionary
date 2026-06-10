from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '1234'

def init_db():
    conn = sqlite3.connect('slang.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS slang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            meaning TEXT,
            example TEXT
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    search = request.args.get('search', '')

    conn = sqlite3.connect('slang.db')
    c = conn.cursor()

    # 전체 목록
    c.execute("SELECT id, word, meaning, example FROM slang")
    all_data = c.fetchall()

    # 검색 결과
    search_data = []
    if search:
        c.execute("""
            SELECT id, word, meaning, example
            FROM slang
            WHERE word LIKE ?
        """, ('%' + search + '%',))
        search_data = c.fetchall()

    conn.close()

    return render_template(
        'index.html',
        all_data=all_data,
        search_data=search_data,
        search=search
    )

@app.route('/add', methods=['POST'])
def add():
    word = request.form['word']
    meaning = request.form['meaning']
    example = request.form['example']

    conn = sqlite3.connect('slang.db')
    c = conn.cursor()

    c.execute("SELECT * FROM slang WHERE word=?", (word,))
    exists = c.fetchone()

    if exists:
        flash("이미 존재하는 단어입니다!")
    else:
        c.execute("""
            INSERT INTO slang (word, meaning, example)
            VALUES (?, ?, ?)
        """, (word, meaning, example))
        conn.commit()
        flash("단어가 추가되었습니다!")

    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('slang.db')
    c = conn.cursor()

    c.execute("DELETE FROM slang WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    init_db()

    # 🔥 다른 컴퓨터에서 접속 가능하게 핵심 설정
    app.run(host='0.0.0.0', port=5000, debug=True)