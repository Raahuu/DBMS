from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import difflib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
conn = sqlite3.connect('plagiarism.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
''')
conn.commit()
conn.close()

# Helper function to calculate similarity
def calculate_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio()

@app.route('/')
def index():
    conn = sqlite3.connect('plagiarism.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM documents')
    documents = cursor.fetchall()
    conn.close()
    return render_template('db.html', documents=documents)

@app.route('/add_document', methods=['POST'])
def add_document():
    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect('plagiarism.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO documents (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()
    flash('Document added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    input_content = request.form['input_content']
    conn = sqlite3.connect('plagiarism.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM documents')
    documents = cursor.fetchall()
    conn.close()

    similarities = []
    for doc in documents:
        similarity = calculate_similarity(input_content, doc[0])
        similarities.append(similarity)

    return render_template('re.html', similarities=similarities)

if __name__ == '__main__':
    app.run(debug=True)
