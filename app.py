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
    

@app.route("/nuevoGrupo", methods=["GET", "POST"])
def nuevoGrupo():
    if request.method == "POST":
        nro = request.form["id"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO grupos (id,jefe) VALUES (%s, %s)",
            (nro, 0)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("grupos"))

    return render_template("formGrupo.html", usuario=None)


@app.route("/grupos", methods=["GET", "POST"])
def grupos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, jefe FROM grupos ORDER BY id;")
    grupos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("grupos.html", grupos=grupos)

@app.route("/socios", methods=["GET", "POST"])
def socios():
    return redirect(url_for("index"))

@app.route("/consultas", methods=["GET", "POST"])
def consultas():
    return redirect(url_for("index"))

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

@app.route("/modificarGrupo/<int:id>", methods=["GET", "POST"])
def modificarGrupo(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, jefe FROM grupos ORDER BY id;")
    grupos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("grupos.html", grupos=grupos)

@app.route("/integrantes/<int:id>", methods=["GET", "POST"])
def integrantes(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM socios where grupo =%s", (id,))
    integrantes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("integrantes.html", grupo=id, integrantes=integrantes)
    


@app.route("/nuevoIntegrante/<int:id>", methods=["GET", "POST"])
def nuevoIntegrante(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        parentesco = request.form["parentesco"]
        fecNac = request.form["fecNac"]
        domicilio = request.form["domicilio"]
        grupo = request.form["grupo"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO socios (id, nombre, parentesco, fecha_nac, domicilio, grupo) VALUES (%s, %s, %s, %s, %s, %s)",
            (1, nombre, parentesco, fecNac, domicilio, grupo)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("integrantes", id = grupo))

    return render_template("formIntegrante.html", grupo=id)
  


if __name__ == "__main__":
    app.run(debug=True)