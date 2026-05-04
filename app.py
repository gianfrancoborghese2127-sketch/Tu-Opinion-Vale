from flask import Flask, request, render_template_string, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_PASSWORD = "Presidente2026GFB"

# Conexión a la base de datos
def get_conn():
    return psycopg2.connect(DATABASE_URL)

# Crear tabla si no existe
def crear_tabla():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS opiniones (
                id SERIAL PRIMARY KEY,
                texto TEXT NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla lista")
    except Exception as e:
        print("Error creando tabla:", e)

crear_tabla()

# Página principal
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        texto = request.form.get("opinion")
        if texto:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("INSERT INTO opiniones (texto) VALUES (%s)", (texto,))
            conn.commit()
            cur.close()
            conn.close()

    return render_template_string("""
        <h1>Dejá tu opinión</h1>
        <form method="post">
            <input name="opinion" placeholder="Escribí algo..." required>
            <button>Enviar</button>
        </form>
        <br>
        <a href="/admin">Ir al panel admin</a>
    """)

# ADMIN LOGIN + PANEL
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT * FROM opiniones ORDER BY id DESC")
            datos = cur.fetchall()
            cur.close()
            conn.close()

            return render_template_string("""
                <h1>Panel Admin</h1>

                {% for op in datos %}
                    <p>
                        {{ op[1] }}
                        <a href="/borrar/{{ op[0] }}">❌ Borrar</a>
                    </p>
                {% endfor %}

                <br>
                <a href="/">Volver</a>
            """, datos=datos)

    return render_template_string("""
        <h1>Login Admin</h1>
        <form method="post">
            <input type="password" name="password" placeholder="Contraseña">
            <button>Entrar</button>
        </form>
    """)

# BORRAR OPINIÓN
@app.route("/borrar/<int:id>")
def borrar(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM opiniones WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/admin")

if __name__ == "__main__":
    app.run()
