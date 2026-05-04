import os
from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔥 IMPORTANTE: usar la variable de entorno de Render
database_url = os.getenv("DATABASE_URL")

# Fix típico de Render (postgres:// -> postgresql://)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ----------------------
# MODELO
# ----------------------
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    comentario = db.Column(db.Text)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# ----------------------
# RUTAS
# ----------------------

# Página principal
@app.route("/")
def home():
    opiniones = Opinion.query.all()

    html = """
    <h1>Deja tu opinión</h1>
    <form method="POST" action="/opinar">
        <input name="nombre" placeholder="Tu nombre" required><br><br>
        <textarea name="comentario" placeholder="Tu opinión" required></textarea><br><br>
        <button type="submit">Enviar</button>
    </form>

    <h2>Opiniones:</h2>
    {% for op in opiniones %}
        <p><b>{{op.nombre}}</b>: {{op.comentario}}</p>
    {% endfor %}
    """

    return render_template_string(html, opiniones=opiniones)

# Guardar opinión
@app.route("/opinar", methods=["POST"])
def opinar():
    try:
        nombre = request.form.get("nombre")
        comentario = request.form.get("comentario")

        nueva = Opinion(nombre=nombre, comentario=comentario)
        db.session.add(nueva)
        db.session.commit()

        return "Opinión guardada 👍 <br><a href='/'>Volver</a>"

    except Exception as e:
        return f"Error: {str(e)}", 500


# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
