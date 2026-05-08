from flask import Flask, render_template, request, redirect, url_for
from db import get_conn

app = Flask(__name__)


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, activo FROM usuarios ORDER BY id;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", usuarios=usuarios)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        activo = request.form["activo"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (id,nombre, activo) VALUES (%s, %s, %s)",
            (112, nombre, activo)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("index"))

    return render_template("form.html", usuario=None)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        activo = request.form["activo"]

        cur.execute(
            "UPDATE usuarios SET nombre=%s, activo=%s WHERE id=%s",
            (nombre, activo, id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    cur.execute("SELECT id, nombre, activo FROM usuarios WHERE id=%s", (id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("form.html", usuario=usuario)


if __name__ == "__main__":
    app.run(debug=True)