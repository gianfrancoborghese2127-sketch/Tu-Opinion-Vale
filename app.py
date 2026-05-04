from flask import Flask, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

ADMIN_USER = "admin"
ADMIN_PASS = "presidente2026GFB"

# Conexión a PostgreSQL (Render)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)


# Crear tabla si no existe
def crear_tabla():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS opiniones (
            id SERIAL PRIMARY KEY,
            texto TEXT
        )
    """)
    conn.commit()
    conn.close()

crear_tabla()


# HOME
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        texto = request.form["opinion"]

        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO opiniones (texto) VALUES (%s)", (texto,))
        conn.commit()
        conn.close()

        return "<h3>Gracias por tu opinión ❤️</h3><a href='/'>Volver</a>"

    return '''
    <style>
    body {
        font-family: Arial;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: #f5f5f5;
        margin: 0;
    }
    .box {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        width: 90%;
        max-width: 400px;
        text-align: center;
    }
    textarea {
        width: 100%;
        padding: 10px;
        margin-top: 10px;
    }
    button {
        margin-top: 15px;
        padding: 10px 20px;
        background: black;
        color: white;
        border: none;
        border-radius: 5px;
    }
    </style>

    <div class="box">
        <h2>Tu Opinión Es Valorada</h2>
        <form method="post">
            <textarea name="opinion" rows="5" placeholder="Escribí tu opinión..."></textarea><br>
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
    <div style="text-align:center; margin-top:100px;">
        <h2>Login Admin</h2>
        <form method="post">
            <input name="user" placeholder="Usuario"><br><br>
            <input name="pw" type="password" placeholder="Contraseña"><br><br>
            <button>Entrar</button>
        </form>
    </div>
    '''


# PANEL ADMIN
@app.route("/panel")
def panel():
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, texto FROM opiniones ORDER BY id DESC")
    datos = c.fetchall()
    conn.close()

    html = "<h1 style='text-align:center;'>Panel</h1>"

    for d in datos:
        html += f"""
        <div style="max-width:600px;margin:20px auto;padding:10px;border:1px solid #ccc;">
            <p>{d[1]}</p>
            <form method="post" action="/borrar/{d[0]}">
                <button>🗑️ Borrar</button>
            </form>
        </div>
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


# RUN
if __name__ == "__main__":
    app.run()
