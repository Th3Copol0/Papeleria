from flask import Flask, render_template,jsonify, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import schedule
import time
import threading
from threading import Lock

app = Flask(__name__, static_url_path='/static')
db_lock = Lock()
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('paleteria.db', timeout=30)  # Incrementar timeout a 30 segundos
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT clave FROM seguridad WHERE id = 1")
        clave_actual = cursor.fetchone()[0]
        conn.close()
    
    for mensaje in alertas_stock:
        flash(mensaje, 'warning')
    
    alertas_stock.clear()
    
    return render_template('index.html', clave_actual=clave_actual)

    
@app.route('/productos', methods=['GET', 'POST']) 
def productos():
    with db_lock:
        conn = get_db_connection()
        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = request.form['precio']
            cantidad = request.form['cantidad']
            stock_minimo = request.form['stock_minimo']
            categoria_id = request.form['categoria_id']
            conn.execute('INSERT INTO productos (nombre, precio, cantidad, stock_minimo, categoria_id) VALUES (?, ?, ?, ?, ?)',
                         (nombre, precio, cantidad, stock_minimo, categoria_id))
            conn.commit()
            flash('Producto añadido con éxito', 'success')
        
        productos = conn.execute('SELECT p.*, c.nombre as categoria_nombre FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id').fetchall()
        conn.close()
        
    return render_template('productos.html', productos=productos)

@app.route('/producto/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    conn.close()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        stock_minimo = request.form.get('stock_minimo')
        categoria_id = request.form.get('categoria_id')

        if not nombre or not precio or not cantidad or not stock_minimo or not categoria_id:
            flash('Por favor, complete todos los campos.', 'error')
            return redirect(request.url)

        try:
            precio = float(precio)
            cantidad = int(cantidad)
            stock_minimo = int(stock_minimo)
        except ValueError:
            flash('El precio, la cantidad y el stock mínimo deben ser números válidos.', 'error')
            return redirect(request.url)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO productos (nombre, precio, cantidad, stock_minimo, categoria_id) VALUES (?, ?, ?, ?, ?)', 
                         (nombre, precio, cantidad, stock_minimo, categoria_id))
            conn.commit()
        except Exception as e:
            flash('Error al agregar el producto: {}'.format(str(e)), 'error')
            conn.rollback()
        finally:
            conn.close()

        return redirect(url_for('productos'))
    
    return render_template('agregar_producto.html', categorias=categorias)
@app.route('/producto/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with db_lock:
        conn = get_db_connection()
        producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
        categorias = conn.execute('SELECT * FROM categorias').fetchall()

        if request.method == 'POST':
            try:
                nombre = request.form['nombre']
                precio = request.form['precio']
                cantidad = request.form['cantidad']
                stock_minimo = request.form['stock_minimo']
                categoria_id = request.form['categoria_id']

                conn.execute('UPDATE productos SET nombre = ?, precio = ?, cantidad = ?, stock_minimo = ?, categoria_id = ? WHERE id = ?',
                             (nombre, precio, cantidad, stock_minimo, categoria_id, id))
                conn.commit()
                flash('Producto modificado con éxito', 'success')
                return redirect(url_for('productos'))
            except KeyError as e:
                flash(f'Error en el formulario: campo {e} faltante.', 'danger')

        conn.close()

    return render_template('modificar_producto.html', producto=producto, categorias=categorias)



@app.route('/producto/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))
# Gestión de Proveedores
@app.route('/proveedores')
def proveedores():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    proveedores = conn.execute('SELECT * FROM proveedores').fetchall()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedor/agregar', methods=['GET', 'POST'])
def agregar_proveedor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form.get('telefono')  # Obtener el valor del teléfono
        
        conn = get_db_connection()
        conn.execute('INSERT INTO proveedores (nombre, contacto, telefono) VALUES (?, ?, ?)', (nombre, contacto, telefono))
        conn.commit()
        conn.close()
        return redirect(url_for('proveedores'))
    
    return render_template('agregar_proveedor.html')

@app.route('/proveedor/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_proveedor(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    proveedor = conn.execute('SELECT * FROM proveedores WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        
        conn.execute('UPDATE proveedores SET nombre = ?, contacto = ?,telefono = ? WHERE id = ?', (nombre, contacto,telefono,id))
        conn.commit()
        conn.close()
        return redirect(url_for('proveedores'))
    
    conn.close()
    return render_template('modificar_proveedor.html', proveedor=proveedor)

@app.route('/proveedor/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_proveedor(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM proveedores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('proveedores'))

# User Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('register'))
        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Ruta para gestionar compras
@app.route('/compras')
def compras():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    compras = conn.execute('SELECT * FROM compras').fetchall()
    conn.close()
    return render_template('compras.html', compras=compras)

@app.route('/compra/agregar', methods=['GET', 'POST'])
def agregar_compra():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        proveedor_id = int(request.form['proveedor_id'])
        cantidad = int(request.form['cantidad'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

        conn = get_db_connection()
        conn.execute('INSERT INTO compras (producto_id, proveedor_id, cantidad, fecha) VALUES (?, ?, ?, ?)', (producto_id, proveedor_id, cantidad, fecha))
        conn.commit()

        # Verificar si es necesario generar una alerta de stock
        producto = conn.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()
        if producto and producto['cantidad'] < producto['stock_minimo']:
            flash(f'Alerta de stock para {producto["nombre"]}: cantidad actual {producto["cantidad"]} < mínimo deseado {producto["stock_minimo"]}', 'warning')

        conn.close()
        return redirect(url_for('compras'))
    
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    proveedores = conn.execute('SELECT * FROM proveedores').fetchall()
    conn.close()
    return render_template('agregar_compra.html', productos=productos, proveedores=proveedores)

@app.route('/compra/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_compra(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    compra = conn.execute('SELECT * FROM compras WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        proveedor_id = int(request.form['proveedor_id'])
        cantidad = int(request.form['cantidad'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

        conn.execute('UPDATE compras SET producto_id = ?, proveedor_id = ?, cantidad = ?, fecha = ? WHERE id = ?', (producto_id, proveedor_id, cantidad, fecha, id))
        conn.commit()
        conn.close()
        return redirect(url_for('compras'))
    
    productos = conn.execute('SELECT * FROM productos').fetchall()
    proveedores = conn.execute('SELECT * FROM proveedores').fetchall()
    conn.close()
    return render_template('modificar_compra.html', compra=compra, productos=productos, proveedores=proveedores)

@app.route('/compra/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_compra(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM compras WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('compras'))
alertas_stock = []

def verificar_stock():
    global alertas_stock
    alertas_stock = []
    try:
        with db_lock:
            conn = get_db_connection()
            if conn:
                try:
                    productos = conn.execute('SELECT nombre, cantidad, stock_minimo FROM productos WHERE cantidad < stock_minimo').fetchall()
                except sqlite3.Error as e:
                    print(f"Error al ejecutar la consulta: {e}")
                    return
                finally:
                    conn.close()
                
                for producto in productos:
                    mensaje_alerta = f'Alerta de stock para {producto["nombre"]}: cantidad actual {producto["cantidad"]} < mínimo deseado {producto["stock_minimo"]}\n'
                    alertas_stock.append(mensaje_alerta)
    except Exception as e:
        print(f"Error al verificar el stock: {e}")

        
def programar_verificacion_stock():
    schedule.every(1).minutes.do(verificar_stock)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/verificar_stock')
def trigger_verificar_stock():
     # Ejecutar la verificación de stock cuando se recibe una solicitud a esta ruta
    global alertas_stock 
    verificar_stock() # Asegúrate de que alertas_stock sea global
    return jsonify({'alertas_stock': alertas_stock})

#Ruta categoria
@app.route('/categorias')
def categorias():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categoria/agregar', methods=['GET', 'POST'])
def agregar_categoria():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO categorias (nombre) VALUES (?)', (nombre,))
        conn.commit()
        conn.close()
        return redirect(url_for('categorias'))
    
    return render_template('agregar_categoria.html')

@app.route('/categoria/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    categoria = conn.execute('SELECT * FROM categorias WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        
        conn.execute('UPDATE categorias SET nombre = ? WHERE id = ?', (nombre, id))
        conn.commit()
        conn.close()
        return redirect(url_for('categorias'))
    
    conn.close()
    return render_template('modificar_categoria.html', categoria=categoria)

@app.route('/categoria/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_categoria(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM categorias WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categorias'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/cambiar_clave', methods=['GET', 'POST'])
def cambiar_clave():
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
    
        if request.method == 'POST':
            print(request.form) 
            nueva_clave = request.form['nueva_clave']
            cursor.execute("UPDATE seguridad SET clave = ? WHERE id = 1", (nueva_clave,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))  # Redirige a la página principal después de cambiar la clave
        else:
            cursor.execute("SELECT clave FROM seguridad WHERE id = 1")
            clave_actual = cursor.fetchone()[0]
            conn.close()
            return render_template('cambiar_clave.html', clave_actual=clave_actual)
 


if __name__ == '__main__':
    programar_verificacion_stock()  # Programar la verificación de stock
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app.run(debug=True)