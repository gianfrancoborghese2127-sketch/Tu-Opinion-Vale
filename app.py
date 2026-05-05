from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# conexión a la DB (Render usa DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# modelo
class Opinion(db.Model):
    __tablename__ = 'opinion'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    comentario = db.Column(db.Text)

@app.route('/')
def home():
    return "API funcionando"

@app.route('/opiniones')
def opiniones():
    try:
        data = Opinion.query.all()

        resultado = []
        for o in data:
            resultado.append({
                "id": o.id,
                "nombre": o.nombre,
                "comentario": o.comentario
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
