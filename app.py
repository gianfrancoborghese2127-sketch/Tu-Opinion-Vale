from flask import Flask, request, render_template_string, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


# ------------------ CONEXIÓN ------------------
def get_conn():
    return psycopg2.connect(DATABASE_URL)


# ------------------ CREAR TABLA ------------------
def crear_tabla():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS opiniones (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            opinion TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

crear_tabla()


# ------------------ PAGINA USUARIOS ------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nombre = request.form["nombre"]
        opinion = request.form["opinion"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO opiniones (nombre, opinion) VALUES (%s, %s)",
            (nombre, opinion)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    return render_template_string("""
    <html>
    <head>
        <title>Opiniones</title>
        <style>
            body {
                background: #0f172a;
                color: white;
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .box {
                background: #1e293b;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                width: 300px;
            }
            input, textarea {
                width: 100%;
                margin: 10px 0;
                padding: 10px;
                border-radius: 10px;
                border: none;
            }
            button {
                padding: 10px;
                border: none;
                border-radius: 10px;
                background: #38bdf8;
                color: black;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Dejá tu opinión</h2>
            <form method="POST">
                <input name="nombre" placeholder="Tu nombre" required>
                <textarea name="opinion" placeholder="Tu opinión" required></textarea>
                <button>Enviar</button>
            </form>
        </div>
    </body>
    </html>
    """)


# ------------------ LOGIN ADMIN ------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]

        if password == "Presidente2026GFB":
            return redirect("/panel")

    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                background: black;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial;
            }
            .box {
                background: #111;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
            }
            input {
                padding: 10px;
                margin: 10px;
                border-radius: 10px;
                border: none;
            }
            button {
                padding: 10px;
                border-radius: 10px;
                border: none;
                background: red;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Admin</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Contraseña">
                <br>
                <button>Entrar</button>
            </form>
        </div>
    </body>
    </html>
    """)


# ------------------ PANEL ADMIN ------------------
@app.route("/panel")
def panel():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT nombre, opinion FROM opiniones")
    datos = cur.fetchall()
    cur.close()
    conn.close()

    contenido = ""
    for n, o in datos:
        contenido += f"<p><b>{n}</b>: {o}</p>"

    return f"""
    <html>
    <body style="background:black; color:white; font-family:Arial; text-align:center;">
        <h1>Panel Admin</h1>
        {contenido}
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()
