from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# 1. Inicializamos la aplicación Flask
app = Flask(__name__)

# Nombre del archivo de la base de datos
DATABASE = 'listado.db'

# Función para conectarnos a la base de datos SQLite
def get_db_connection():
    # Conectamos con el archivo de base de datos
    conn = sqlite3.connect(DATABASE)
    # Esto permite acceder a las columnas por su nombre (ej: fila['contenido'])
    conn.row_factory = sqlite3.Row
    return conn

# 2. Función para crear la tabla de la base de datos si no existe
def init_db():
    conn = get_db_connection()
    # Ejecutamos comando SQL para crear la tabla 'listado'
    conn.execute('''
        CREATE TABLE IF NOT EXISTS listado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 3. Ruta principal: Muestra la página con el listado
@app.route('/')
def index():
    conn = get_db_connection()
    
    # Verificamos si el usuario hizo clic en "Editar" algún elemento
    editar_id = request.args.get('editar')
    item_a_editar = None
    
    # Si hay un ID para editar, buscamos ese elemento en la base de datos (SQL SELECT con WHERE)
    if editar_id:
        item_a_editar = conn.execute(
            'SELECT * FROM listado WHERE id = ?', (editar_id,)
        ).fetchone()

    # Obtenemos todos los elementos ordenados del más nuevo al más viejo (SQL SELECT)
    items = conn.execute('SELECT * FROM listado ORDER BY id DESC').fetchall()
    conn.close()

    # Mostramos la página HTML enviándole los datos
    return render_template('index.html', items=items, item_a_editar=item_a_editar)

# 4. Ruta para agregar un nuevo elemento (SQL INSERT)
@app.route('/agregar', methods=['POST'])
def agregar():
    contenido = request.form['contenido'].strip()
    
    # Solo guardamos si el texto no está vacío
    if contenido:
        conn = get_db_connection()
        # Insertamos el nuevo texto en la tabla usando SQL
        conn.execute('INSERT INTO listado (contenido) VALUES (?)', (contenido,))
        conn.commit()
        conn.close()

    # Redirigimos a la página principal
    return redirect(url_for('index'))

# 5. Ruta para guardar la edición de un elemento (SQL UPDATE)
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    nuevo_contenido = request.form['contenido'].strip()
    
    if nuevo_contenido:
        conn = get_db_connection()
        # Actualizamos el contenido del registro con ese ID usando SQL
        conn.execute('UPDATE listado SET contenido = ? WHERE id = ?', (nuevo_contenido, id))
        conn.commit()
        conn.close()

    # Redirigimos a la página principal
    return redirect(url_for('index'))

# 6. Ruta para eliminar un elemento (SQL DELETE)
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    conn = get_db_connection()
    # Eliminamos el registro de la tabla usando SQL
    conn.execute('DELETE FROM listado WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    # Redirigimos a la página principal
    return redirect(url_for('index'))

# Iniciamos el servidor web
if __name__ == '__main__':
    # Creamos la base de datos y la tabla antes de iniciar
    init_db()
    print("Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)
