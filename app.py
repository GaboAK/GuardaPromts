from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'listado.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS listado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    
    editar_id = request.args.get('editar')
    item_a_editar = None
    
    if editar_id:
        item_a_editar = conn.execute(
            'SELECT * FROM listado WHERE id = ?', (editar_id,)
        ).fetchone()

    items = conn.execute('SELECT * FROM listado ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', items=items, item_a_editar=item_a_editar)

@app.route('/agregar', methods=['POST'])
def agregar():
    contenido = request.form['contenido'].strip()
    
    if contenido:
        conn = get_db_connection()
        conn.execute('INSERT INTO listado (contenido) VALUES (?)', (contenido,))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    nuevo_contenido = request.form['contenido'].strip()
    
    if nuevo_contenido:
        conn = get_db_connection()
        conn.execute('UPDATE listado SET contenido = ? WHERE id = ?', (nuevo_contenido, id))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM listado WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)
