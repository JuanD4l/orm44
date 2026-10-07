from flask import jsonify, request, abort
from app.models import Baul, db

# OBTENER TODOS LOS REGISTROS
def baul_list():
    registros = db.session.execute(db.select(Baul)).scalars().all()
    return jsonify([r.to_dict() for r in registros]), 200

# OBTENER UN REGISTRO POR ID
def baul_detail(id_baul):
    registro = db.session.get(Baul, id_baul)
    if not registro:
        abort(404, description="Registro no encontrado")
    return jsonify(registro.to_dict()), 200

# CREAR UN NUEVO REGISTRO
def baul_add():
    data = request.get_json()
    if not data:
        abort(400, description="No se recibió información JSON")
    
    required_fields = ["Plataforma", "usuario", "clave"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Falta el campo obligatorio: {field}")

    nuevo_registro = Baul(
        Plataforma=data["Plataforma"],
        usuario=data["usuario"],
        clave=data["clave"]
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify({"mensaje": "Registro creado correctamente", "data": nuevo_registro.to_dict()}), 201

# ACTUALIZAR UN REGISTRO
def baul_update(id_baul):
    data = request.get_json()
    if not data:
        abort(400, description="No se recibió información JSON")

    registro = db.session.get(Baul, id_baul)
    if not registro:
        abort(404, description="Registro no encontrado")

    registro.Plataforma = data.get("Plataforma", registro.Plataforma)
    registro.usuario = data.get("usuario", registro.usuario)
    registro.clave = data.get("clave", registro.clave)

    db.session.commit()
    return jsonify({"mensaje": "Registro actualizado correctamente", "data": registro.to_dict()}), 200

# ELIMINAR UN REGISTRO
def baul_delete(id_baul):
    registro = db.session.get(Baul, id_baul)
    if not registro:
        abort(404, description="Registro no encontrado")

    db.session.delete(registro)
    db.session.commit()
    return jsonify({"mensaje": "Registro eliminado correctamente"}), 200