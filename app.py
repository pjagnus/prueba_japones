from flask import Flask, render_template, request, redirect, url_for, Response 
#,send_from_directory
from db import get_conn
from flask_session import Session 
from flask import session 
from datetime import datetime, timedelta
import functools

import pdfs
app = Flask(__name__)
#app.config['JSON_AS_ASCII'] = False
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["SESSION_PERMANENT"] = False
app.permanent_session_lifetime = timedelta(minutes=30)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("usuario") is None:
            return redirect("/login")
        
        #elif session.get("cambiar_clave")  == True:
        
        #    return redirect("/clogin")                 
        #    #return render_template("clogin.html", texto="Debe cambiar la clave ")                

        return view(**kwargs)

    return wrapped_view

@app.route("/login",  methods=["GET","POST"])
def login():
    session["cambiar_clave"] = False
    name = request.form.get("name")
    clave = request.form.get("clave")
    if name is None:
        return render_template("login.html")
        
    name = name.lower()        
    #if sqls.val_clave(db, name,clave):
    if name =='victor' and clave == '1':     
        session["usuario"] = name
        return redirect("/")
    else:	
        session["usuario"] = None
    
    return render_template("login.html",texto="Los Datos Ingresados son Incorrectos")

@app.route("/salir",  methods=["GET","POST"])
def salir():
    if session.get("usuario"):
        session.pop("usuario")
    return render_template("login.html")



@app.route("/")
@login_required
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, activo FROM usuarios ORDER BY id;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", usuarios=usuarios)


@app.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        activo = request.form["activo"]
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO usuarios (id,nombre, activo) VALUES (%s, %s, %s)",
                (112, nombre, activo)
            )
            conn.commit()
        except:    
            conn.rollback()
        cur.close()
        conn.close()

        return redirect(url_for("index"))

    return render_template("form.html", usuario=None)
    

@app.route("/nuevoGrupo", methods=["GET", "POST"])
@login_required
def nuevoGrupo():
    if request.method == "POST":
        try:
            nro = int(request.form["id"])
        except:
            nro = 0
        if nro == 0:    
            return render_template("formGrupo.html")
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO grupos (id,jefe) VALUES (%s, %s)",
                (nro, 0)
            )
            conn.commit()
        except:    
            conn.rollback()
        cur.close()
        conn.close()

        return redirect(url_for("grupos"))

    return render_template("formGrupo.html")


@app.route("/grupos", methods=["GET", "POST"])
@login_required
def grupos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, jefe FROM grupos ORDER BY id;")
    grupos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("grupos.html", grupos=grupos)

@app.route("/socios", methods=["GET", "POST"])
@login_required
def socios():
    return redirect(url_for("index"))

@app.route("/consultas", methods=["GET", "POST"])
@login_required
def consultas():
    return render_template("consultas.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
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
@login_required
def modificarGrupo(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, jefe FROM grupos ORDER BY id;")
    grupos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("grupos.html", grupos=grupos)

@app.route("/integrantes/<int:id>", methods=["GET", "POST"])
@login_required
def integrantes(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, parentesco, fecha_nac, domicilio FROM socios where grupo =%s", (id,))
    integrantes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("integrantes.html", grupo=id, integrantes=integrantes)
    


@app.route("/nuevoIntegrante/<int:id>", methods=["GET", "POST"])
@login_required
def nuevoIntegrante(id):
    if request.method == "POST":
        nombre = request.form["nombre"].strip()[:50]
        parentesco = request.form["parentesco"]
        fecNac = request.form["fecNac"]
        domicilio = request.form["domicilio"].strip()[:50]
        grupo = request.form["grupo"]
        
        if nombre == '' or domicilio == '' or not validarFecha(fecNac):
            return render_template("formIntegrante.html", grupo=id, usuario = None)
            
        conn = get_conn()
        cur = conn.cursor()
        sql = "select max(id) from socios"
        cur.execute(sql)
        dato = cur.fetchone()
        if dato[0] is None:
            prox = 1
        else:    
            prox = dato[0] + 1
        
        try:
            cur.execute(
                "INSERT INTO socios (id, nombre, parentesco, fecha_nac, domicilio, grupo) VALUES (%s, %s, %s, %s, %s, %s)",
                (prox, nombre, parentesco, fecNac, domicilio, grupo)
            )
            conn.commit()
        except:
            conn.rollback()    
        cur.close()
        conn.close()

        return redirect(url_for("integrantes", id = grupo))

    return render_template("formIntegrante.html", grupo=id, usuario = None)
  

@app.route("/modificarIntegrante/<int:id>", methods=["GET", "POST"])
@login_required
def modificarIntegrante(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT grupo FROM socios WHERE id=%s", (id,))
    idGrupo = cur.fetchone()[0]

    if request.method == "POST":
        nombre = request.form["nombre"].strip()[:50]
        parentesco = request.form["parentesco"]
        fecNac = request.form["fecNac"]
        domicilio = request.form["domicilio"].strip()[:50]

        cur.execute(
            "UPDATE socios SET nombre=%s, parentesco=%s, fecha_nac=%s, domicilio=%s  WHERE id=%s",
            (nombre, parentesco, fecNac, domicilio, id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("integrantes", id = idGrupo))        
    
    cur.execute("SELECT id, nombre, parentesco, fecha_nac, domicilio FROM socios WHERE id=%s", (id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("formIntegrante.html", usuario=usuario, grupo = idGrupo)


@app.route("/eliminarIntegrante/<int:id>", methods=["GET", "POST"])
@login_required
def eliminarIntegrante(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT grupo FROM socios WHERE id=%s", (id,))
    idGrupo = cur.fetchone()[0]
    #if request.method == "POST":
    if 1:
        cur.execute(
            "delete from socios WHERE id=%s",
            (id,)
        )
        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for("integrantes", id = idGrupo))

@login_required
@app.route("/pdfPadron",  methods=["GET","POST"])
def pdfPadron():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT grupo, nombre, parentesco, fecha_nac, domicilio FROM socios order by grupo, parentesco, nombre ")
    socios = cur.fetchall()
    cur.close()
    conn.close()    
    pdf = pdfs.padron(socios)
        
    return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=padron.pdf'})

@app.route("/porJubilarse", methods=["GET", "POST"])
@login_required
def porJubilarse():
    return render_template("porJubilarse.html")


@login_required
@app.route("/pdfPorJubilarse",  methods=["GET","POST"])
def pdfPorJubilarse():
    if request.method == "POST":
        desde = int(request.form["desde"])
        hasta = int(request.form["hasta"])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT grupo, nombre, parentesco, EXTRACT(YEAR FROM age(fecha_nac)), domicilio FROM socios Where EXTRACT(YEAR FROM age(fecha_nac)) >= %s and EXTRACT(YEAR FROM age(fecha_nac)) <= %s order by fecha_nac, nombre ", (desde, hasta))
    socios = cur.fetchall()
    cur.close()
    conn.close()    
    pdf = pdfs.porJubilarse(socios)
        
    return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=porJubilarse.pdf'})



def validarFecha(fecha, vacia=False):
    resu = False
    if fecha=='':
        return vacia
    try:
        x_min=datetime.strptime('01/01/1900', '%d/%m/%Y')    
        x=datetime.strptime(fecha, '%Y-%m-%d')    
        if x > x_min:
            x_max=datetime.strptime('01/01/2100', '%d/%m/%Y')    
            resu = x < x_max
    except:
        resu = False
    
    return resu




if __name__ == "__main__":
    app.run(debug=True)