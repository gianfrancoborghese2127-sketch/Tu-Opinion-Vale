from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    comentario = db.Column(db.Text)  # 👈 IMPORTANTE (no "opinion")

# Ruta principal
@app.route('/')
def home():
    return "API funcionando"

# Obtener opiniones
@app.route('/opiniones', methods=['GET'])
def obtener_opiniones():
    try:
        opiniones = Opinion.query.all()
        resultado = []

        for o in opiniones:
            resultado.append({
                "id": o.id,
                "nombre": o.nombre,
                "comentario": o.comentario  # 👈 IMPORTANTE
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear opinión
@app.route('/opiniones', methods=['POST'])
def crear_opinion():
    try:
        data = request.get_json()

        nueva = Opinion(
            nombre=data.get('nombre'),
            comentario=data.get('comentario')  # 👈 IMPORTANTE
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({"mensaje": "Opinión guardada"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
