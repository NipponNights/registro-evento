from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "nippon.db"

# Inicializa la base de datos
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

init_db()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", message="")

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO usuarios (email) VALUES (?)", (email,))
        message = f"✔ Registro exitoso para: {email}"
    except sqlite3.IntegrityError:
        message = "✖ Este correo ya está registrado."
    return render_template("index.html", message=message)
from flask import request, abort

@app.route("/usuarios")
def ver_usuarios():
    password = request.args.get("pass")
    if password != "1ll0capor_06":
        abort(403)
    with sqlite3.connect("nippon.db") as conn:
        c = conn.cursor()
        c.execute("SELECT email, fecha_registro FROM usuarios")
        usuarios = c.fetchall()
    return "<h2>Usuarios registrados:</h2><br>" + "<br>".join([f"{email} - {fecha}" for email, fecha in usuarios])


if __name__ == "__main__":
    app.run(debug=True)
