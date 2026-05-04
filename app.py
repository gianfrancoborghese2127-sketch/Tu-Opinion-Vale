import os
from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔥 ARREGLAR DATABASE_URL DE RENDER
url = os.environ.get("DATABASE_URL")

if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 📌 MODELO
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    mensaje = db.Column(db.Text)

# 🔥 CREAR TABLA AUTOMÁTICAMENTE
with app.app_context():
    db.create_all()

# 🎨 HTML USUARIO (centrado bonito)
HTML_USER = """
<!DOCTYPE html>
<html>
<head>
<title>Tu Opinión Vale</title>
<style>
body {
    font-family: Arial;
    background: #f2f2f2;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    width: 300px;
    text-align: center;
}
input, textarea {
    width: 100%;
    margin: 10px 0;
    padding: 10px;
}
button {
    background: black;
    color: white;
    padding: 10px;
    border: none;
    width: 100%;
}
</style>
</head>
<body>
<div class="container">
<h2>Tu Opinión Vale</h2>
<form method="POST">
<input name="nombre" placeholder="Tu nombre" required>
<textarea name="mensaje" placeholder="Tu opinión" required></textarea>
<button>Enviar</button>
</form>
</div>
</body>
</html>
"""

# 🔐 HTML LOGIN ADMIN
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
<title>Admin</title>
</head>
<body style="text-align:center; margin-top:100px;">
<h2>Acceso Admin</h2>
<form method="POST">
<input type="password" name="password" placeholder="Contraseña">
<button>Entrar</button>
</form>
</body>
</html>
"""

# 📊 HTML ADMIN
HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head>
<title>Admin</title>
</head>
<body style="font-family:Arial; text-align:center;">
<h2>Opiniones</h2>
<ul>
{% for o in opiniones %}
<li><b>{{o.nombre}}</b>: {{o.mensaje}}</li>
{% endfor %}
</ul>
</body>
</html>
"""

# 🌐 RUTA PRINCIPAL (usuarios)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nombre = request.form["nombre"]
        mensaje = request.form["mensaje"]

        nueva = Opinion(nombre=nombre, mensaje=mensaje)
        db.session.add(nueva)
        db.session.commit()

        return redirect("/")

    return render_template_string(HTML_USER)

# 🔐 LOGIN ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == "Presidente2026GFB":
            return redirect("/panel")
    return render_template_string(HTML_LOGIN)

# 📊 PANEL ADMIN
@app.route("/panel")
def panel():
    opiniones = Opinion.query.all()
    return render_template_string(HTML_ADMIN, opiniones=opiniones)

# 🚀 RUN
if __name__ == "__main__":
    app.run()
