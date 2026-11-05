
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.app.models import db, Baul

app = Flask(__name__)
CORS(app)

# Configuración de MySQL mediante SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost/gestor_contrasena"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# CONSULTAR TODOS LOS REGISTROS
@app.route("/baul", methods=["GET"])
def obtener_registros():
    registros = db.session.execute(
        db.select(Baul)
    ).scalars().all()

    return jsonify([registro.to_dict() for registro in registros])


# CONSULTAR UN REGISTRO
@app.route("/baul/<int:id_baul>", methods=["GET"])
def obtener_registro(id_baul):
    registro = db.session.get(Baul, id_baul)

    if registro is None:
        return jsonify({"mensaje": "Registro no encontrado"}), 404

    return jsonify(registro.to_dict())


# CREAR REGISTRO
@app.route("/baul", methods=["POST"])
def crear_registro():
    datos = request.get_json(silent=True) or {}

    plataforma = datos.get("Plataforma", "").strip()
    usuario = datos.get("usuario", "").strip()
    clave = datos.get("clave", "").strip()

    if not plataforma or not usuario or not clave:
        return jsonify({"mensaje": "Todos los campos son obligatorios"}), 400

    nuevo = Baul(
        Plataforma=plataforma,
        usuario=usuario,
        clave=clave
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"mensaje": "Registro creado correctamente"}), 201


# ACTUALIZAR REGISTRO
@app.route("/baul/<int:id_baul>", methods=["PUT"])
def actualizar_registro(id_baul):
    registro = db.session.get(Baul, id_baul)

    if registro is None:
        return jsonify({"mensaje": "Registro no encontrado"}), 404

    datos = request.get_json(silent=True) or {}

    plataforma = datos.get("Plataforma", "").strip()
    usuario = datos.get("usuario", "").strip()
    clave = datos.get("clave", "").strip()

    if not plataforma or not usuario or not clave:
        return jsonify({"mensaje": "Todos los campos son obligatorios"}), 400

    registro.Plataforma = plataforma
    registro.usuario = usuario
    registro.clave = clave

    db.session.commit()

    return jsonify({"mensaje": "Registro actualizado correctamente"})


# ELIMINAR REGISTRO
@app.route("/baul/<int:id_baul>", methods=["DELETE"])
def eliminar_registro(id_baul):
    registro = db.session.get(Baul, id_baul)

    if registro is None:
        return jsonify({"mensaje": "Registro no encontrado"}), 404

    db.session.delete(registro)
    db.session.commit()

    return jsonify({"mensaje": "Registro eliminado correctamente"})


if __name__ == "__main__":
    app.run(debug=True)
