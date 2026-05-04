from flask import Flask, request, render_template_string, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_PASSWORD = "Presidente2026GFB"

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def crear_tabla():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS opiniones (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

crear_tabla()

# 🌐 PAGINA PRINCIPAL (BONITA Y CENTRADA)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        texto = request.form.get("opinion")
        if texto:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("INSERT INTO opiniones (texto) VALUES (%s)", (texto,))
            conn.commit()
            cur.close()
            conn.close()

    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                background: #f2f2f2;
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                text-align: center;
                width: 90%;
                max-width: 400px;
            }
            input {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
            }
            button {
                margin-top: 10px;
                padding: 10px;
                width: 100%;
                background: black;
                color: white;
                border: none;
                border-radius: 8px;
            }
            .admin-link {
                margin-top: 15px;
                display: block;
                font-size: 12px;
                color: gray;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Dejá tu opinión</h2>
            <form method="post">
                <input name="opinion" placeholder="Escribí algo..." required>
                <button>Enviar</button>
            </form>
            <a class="admin-link" href="/admin">Admin</a>
        </div>
    </body>
    </html>
    """)

# 🔐 LOGIN ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            return redirect("/panel")

    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                background: #111;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial;
            }
            .box {
                text-align: center;
            }
            input, button {
                padding: 10px;
                margin-top: 10px;
                width: 200px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Admin Login</h2>
            <form method="post">
                <input type="password" name="password" placeholder="Contraseña">
                <br>
                <button>Entrar</button>
            </form>
        </div>
    </body>
    </html>
    """)

# 🧠 PANEL ADMIN REAL
@app.route("/panel")
def panel():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM opiniones ORDER BY id DESC")
    datos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background: #222;
                color: white;
                padding: 20px;
            }
            .card {
                background: #333;
                padding: 10px;
                margin: 10px 0;
                border-radius: 10px;
            }
            a {
                color: red;
                float: right;
            }
        </style>
    </head>
    <body>
        <h2>Panel Admin</h2>

        {% for op in datos %}
            <div class="card">
                {{ op[1] }}
                <a href="/borrar/{{ op[0] }}">❌</a>
            </div>
        {% endfor %}
    </body>
    </html>
    """, datos=datos)

# ❌ BORRAR
@app.route("/borrar/<int:id>")
def borrar(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM opiniones WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/panel")

if __name__ == "__main__":
    app.run()
