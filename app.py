from flask import Flask, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

ADMIN_USER = "admin"
ADMIN_PASS = "presidente2026GFB"

# Conexión a PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# Crear tabla si no existe
conn = get_conn()
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS opiniones (id SERIAL PRIMARY KEY, texto TEXT)")
conn.commit()
conn.close()

# HOME (usuarios)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        texto = request.form["opinion"]

        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO opiniones (texto) VALUES (%s)", (texto,))
        conn.commit()
        conn.close()

        return "<h3>Gracias por tu opinión 💙</h3>"

    return '''
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial;
            background: #f5f5f5;
        }
        .box {
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 10px;
            width: 90%;
            max-width: 400px;
        }
        textarea {
            width: 100%;
        }
    </style>

    <div class="box">
        <h1>Tu Opinión Es Valorada</h1>
        <h3>Dejá tu opinión anónima</h3>
        <form method="post">
            <textarea name="opinion" rows="5"></textarea><br><br>
            <button>Enviar</button>
        </form>
    </div>
    '''

# LOGIN ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["user"]
        pw = request.form["pw"]

        if user == ADMIN_USER and pw == ADMIN_PASS:
            session["admin"] = True
            return redirect("/panel")

    return '''
    <h2>Login Admin</h2>
    <form method="post">
        Usuario: <input name="user"><br><br>
        Contraseña: <input name="pw" type="password"><br><br>
        <button>Entrar</button>
    </form>
    '''

# PANEL ADMIN
@app.route("/panel")
def panel():
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, texto FROM opiniones")
    datos = c.fetchall()
    conn.close()

    html = "<h1>Panel</h1>"

    for d in datos:
        html += f"""
        <p>{d[1]}</p>
        <form method="post" action="/borrar/{d[0]}">
            <button>🗑️ Borrar</button>
        </form>
        <hr>
        """

    return html

# BORRAR
@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM opiniones WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return redirect("/panel")

if __name__ == "__main__":
    app.run()
