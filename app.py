from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

ADMIN_USER = "admin"
ADMIN_PASS = "presidente2026GFB"

# Crear DB
conn = sqlite3.connect("db.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS opiniones (texto TEXT)")
conn.commit()
conn.close()

# HOME
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        texto = request.form["opinion"]

        conn = sqlite3.connect("db.db")
        c = conn.cursor()
        c.execute("INSERT INTO opiniones VALUES (?)", (texto,))
        conn.commit()
        conn.close()

        return "<h3 style='text-align:center'>Gracias por tu opinión 🙌</h3>"

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tu Opinión</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background: white;
                padding: 25px;
                border-radius: 10px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            textarea {
                width: 100%;
                padding: 10px;
                border-radius: 5px;
            }
            button {
                background: black;
                color: white;
                padding: 10px;
                border: none;
                width: 100%;
                margin-top: 10px;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #333;
            }
        </style>
    </head>
    <body>

    <div class="box">
        <h2>Tu Opinión Es Valorada</h2>
        <p>Dejá tu opinión anónima</p>

        <form method="post">
            <textarea name="opinion" rows="5" placeholder="Escribí acá..."></textarea><br><br>
            <button>Enviar</button>
        </form>
    </div>

    </body>
    </html>
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
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background: white;
                padding: 25px;
                border-radius: 10px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            input {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
            }
            button {
                margin-top: 15px;
                padding: 10px;
                width: 100%;
                background: black;
                color: white;
                border: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>

    <div class="box">
        <h2>Login Admin</h2>
        <form method="post">
            <input name="user" placeholder="Usuario"><br>
            <input name="pw" type="password" placeholder="Contraseña"><br>
            <button>Entrar</button>
        </form>
    </div>

    </body>
    </html>
    '''

# PANEL ADMIN
@app.route("/panel")
def panel():
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    c.execute("SELECT rowid, texto FROM opiniones")
    datos = c.fetchall()
    conn.close()

    html = '''
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 20px;
        }
        .card {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        button {
            background: red;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    </head>
    <body>

    <h2>Panel de Opiniones</h2>
    '''

    for d in datos:
        html += f"""
        <div class="card">
            <p>{d[1]}</p>
            <form method="post" action="/borrar/{d[0]}">
                <button>🗑️ Borrar</button>
            </form>
        </div>
        """

    html += "</body></html>"
    return html

# BORRAR
@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    c.execute("DELETE FROM opiniones WHERE rowid = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/panel")

if __name__ == "__main__":
    app.run()
