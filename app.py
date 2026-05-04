import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔑 Configuración DB (Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix para postgres en Render
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 📌 Modelo (IMPORTANTE: usa "opinion", NO comentario)
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    opinion = db.Column(db.Text)

# 🏠 Ruta base
@app.route("/")
def home():
    return "API funcionando 🚀"

# 📥 Obtener opiniones
@app.route("/opiniones", methods=["GET"])
def obtener_opiniones():
    opiniones = Opinion.query.all()

    resultado = []
    for o in opiniones:
        resultado.append({
            "id": o.id,
            "nombre": o.nombre,
            "opinion": o.opinion
        })

    return jsonify(resultado)

# 📤 Guardar opinión
@app.route("/opiniones", methods=["POST"])
def guardar_opinion():
    data = request.get_json()

    nueva = Opinion(
        nombre=data.get("nombre"),
        opinion=data.get("opinion")  # 👈 AQUÍ TAMBIÉN
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify({"mensaje": "Opinión guardada correctamente"}), 201

# 🚀 Arranque
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
