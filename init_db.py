import sqlite3

def init_db():
    conn = sqlite3.connect('paleteria.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        cantidad INTEGER NOT NULL,
        stock_minimo INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT NOT NULL,
        telefono TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        proveedor_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos(id),
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS seguridad (
        id INTEGER PRIMARY KEY,
        clave TEXT NOT NULL
    )''')
    cursor.execute('INSERT OR IGNORE INTO seguridad (id, clave) VALUES (1, "default_clave")')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()