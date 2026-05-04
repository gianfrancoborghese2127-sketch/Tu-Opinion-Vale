import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔑 DB config
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 🔥 MODELO CORRECTO
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    opinion = db.Column(db.Text)

# 🔥 CREAR TABLAS AUTOMÁTICAMENTE
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "API funcionando 🚀"

@app.route("/opiniones", methods=["GET"])
def obtener_opiniones():
    try:
        opiniones = Opinion.query.all()

        return jsonify([
            {
                "id": o.id,
                "nombre": o.nombre,
                "opinion": o.opinion
            }
            for o in opiniones
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/opiniones", methods=["POST"])
def guardar_opinion():
    try:
        data = request.get_json()

        nueva = Opinion(
            nombre=data.get("nombre"),
            opinion=data.get("opinion")
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({"mensaje": "Guardado"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
