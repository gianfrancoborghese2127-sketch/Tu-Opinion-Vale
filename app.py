from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config DB (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    mensaje = db.Column(db.Text)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# ----------- HTML BASE -----------
ESTILO = """
<style>
body {
    font-family: Arial;
    background: #f4f4f4;
    text-align: center;
}
.container {
    margin-top: 50px;
}
input, textarea {
    width: 300px;
    padding: 10px;
    margin: 5px;
}
button {
    padding: 10px 20px;
    background: black;
    color: white;
    border: none;
}
.opinion {
    background: white;
    margin: 10px auto;
    padding: 10px;
    width: 400px;
    border-radius: 10px;
}
</style>
"""

# ----------- PÁGINA USUARIO -----------
@app.route("/")
def index():
    return render_template_string(ESTILO + """
    <div class="container">
        <h1>Deja tu opinión</h1>
        <form action="/enviar" method="POST">
            <input name="nombre" placeholder="Tu nombre" required><br>
            <textarea name="mensaje" placeholder="Tu opinión" required></textarea><br>
            <button type="submit">Enviar</button>
        </form>
    </div>
    """)

# Guardar opinión
@app.route("/enviar", methods=["POST"])
def enviar():
    nombre = request.form["nombre"]
    mensaje = request.form["mensaje"]

    nueva = Opinion(nombre=nombre, mensaje=mensaje)
    db.session.add(nueva)
    db.session.commit()

    return redirect("/")

# ----------- LOGIN ADMIN -----------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == "Presidente2026GFB":
            return redirect("/panel")
        else:
            return "Contraseña incorrecta"

    return render_template_string(ESTILO + """
    <div class="container">
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Contraseña">
            <br>
            <button>Entrar</button>
        </form>
    </div>
    """)

# ----------- PANEL ADMIN -----------
@app.route("/panel")
def panel():
    opiniones = Opinion.query.all()

    html = """
    <div class="container">
        <h1>Panel Admin</h1>
    """

    for o in opiniones:
        html += f"""
        <div class="opinion">
            <b>{o.nombre}</b><br>
            {o.mensaje}
        </div>
        """

    html += "</div>"

    return render_template_string(ESTILO + html)
