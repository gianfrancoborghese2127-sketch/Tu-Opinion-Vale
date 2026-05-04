from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

CODIGO_ACCESO = "opina123"
ADMIN_USER = "admin"
ADMIN_PASS = "presidente2026GFB"

# Crear DB
conn = sqlite3.connect("db.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS opiniones (texto TEXT)")
conn.commit()
conn.close()

# HOME (usuarios)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        codigo = request.form["codigo"]
        texto = request.form["opinion"]

        if codigo == CODIGO_ACCESO:
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            c.execute("INSERT INTO opiniones VALUES (?)", (texto,))
            conn.commit()
            conn.close()
            return "<h3>Gracias por tu opinión, muy pronto será charlada</h3>"
        else:
            return "<h3>Código incorrecto</h3>"

    return '''
    <h1>Tu Opinión Es Valorada</h1>
    <h3>Dejá tu opinión anónima</h3>
    <form method="post">
        Código: <input name="codigo"><br><br>
        <textarea name="opinion" rows="5" cols="40"></textarea><br><br>
        <button>Enviar</button>
    </form>
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
    <h1>Tu Opinión Es Valorada</h1>
    <h2>Login Admin</h2>
    <form method="post">
        Usuario: <input name="user"><br>
        Contraseña: <input name="pw" type="password"><br><br>
        <button>Entrar</button>
    </form>
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

    html = "<h1>Panel - Tu Opinión Es Valorada</h1>"

    for d in datos:
        html += f"""
        <p>{d[1]}</p>
        <form method="post" action="/borrar/{d[0]}" 
              onsubmit="return confirm('¿Seguro que querés borrar esta opinión?');">
            <button type="submit">🗑️ Borrar</button>
        </form>
        <hr>
        """

    return html

# BORRAR OPINIÓN (POST)
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
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        if user == ADMIN_USER and password == ADMIN_PASS:
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            c.execute("SELECT texto FROM opiniones")
            opiniones = c.fetchall()
            conn.close()

            lista = "<h2>Opiniones:</h2>"
            for op in opiniones:
                lista += f"<p>{op[0]}</p>"

            return lista
        else:
            return "<h3>Credenciales incorrectas</h3>"

    return '''
        <h2>Login Admin</h2>
        <form method="post">
            Usuario: <input name="user"><br><br>
            Contraseña: <input name="password" type="password"><br><br>
            <button>Entrar</button>
        </form>
    '''
