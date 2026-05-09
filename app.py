from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(_name_)
DB = 'visitas.db'
ADMIN_KEY = "tuclave123"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS visitas 
        (id INTEGER PRIMARY KEY, rut TEXT, nombre TEXT, tipo_visita TEXT, 
         patente TEXT, direccion TEXT, vehiculo TEXT, personas INTEGER, hora TEXT)''')
    db.commit()
init_db()

@app.route('/')
def index():
    db = get_db()
    visitas = db.execute('SELECT * FROM visitas ORDER BY id DESC LIMIT 50').fetchall()
    hoy = datetime.now().strftime('%Y-%m-%d')
    total_hoy = db.execute('SELECT COUNT(*) FROM visitas WHERE DATE(hora) =?', (hoy,)).fetchone()[0]
    return render_template('index.html', visitas=visitas, total_hoy=total_hoy, admin_key=ADMIN_KEY)

@app.route('/registrar', methods=['POST'])
def registrar():
    db = get_db()
    rut = request.form['rut']
    nombre = request.form['nombre']
    tipo_visita = request.form['tipo_visita']
    patente = request.form.get('patente', '')
    direccion = request.form.get('direccion', '')
    vehiculo = request.form.get('vehiculo', '')
    personas = request.form.get('personas', '1')
    hora = request.form.get('hora', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.execute('INSERT INTO visitas (rut, nombre, tipo_visita, patente, direccion, vehiculo, personas, hora) VALUES (?,?,?,?,?,?,?,?)',
               (rut, nombre, tipo_visita, patente, direccion, vehiculo, personas, hora))
    db.commit()
    return redirect('/')
