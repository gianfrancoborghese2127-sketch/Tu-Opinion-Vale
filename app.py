import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔗 conexión a la DB (Render usa DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")

# arreglo para postgres en Render
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 📦 modelo
class Opinion(db.Model):
    __tablename__ = "opinion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    comentario = db.Column(db.Text)

# 🔧 crear tabla si no existe
with app.app_context():
    db.create_all()

# 🏠 ruta base
@app.route("/")
def home():
    return "API funcionando 🚀"

# 📥 ver opiniones
@app.route("/opiniones", methods=["GET"])
def obtener_opiniones():
    try:
        opiniones = Opinion.query.all()
        resultado = []

        for op in opiniones:
            resultado.append({
                "id": op.id,
                "nombre": op.nombre,
                "comentario": op.comentario
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📤 agregar opinión
@app.route("/opiniones", methods=["POST"])
def agregar_opinion():
    try:
        data = request.get_json()

        nueva = Opinion(
            nombre=data.get("nombre"),
            comentario=data.get("comentario")
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({"mensaje": "Opinión agregada"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ▶️ correr app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
