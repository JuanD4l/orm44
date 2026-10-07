from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

CORS(app)

def get_db_connection():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_contrasena"
    )
    return conexion


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Backend funcionando correctamente"
    })


@app.route("/baul", methods=["GET"])
def obtener_registros():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM baul")

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify(registros)


@app.route("/baul/<int:id_baul>", methods=["GET"])
def obtener_registro(id_baul):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM baul WHERE id_baul = %s",
        (id_baul,)
    )

    registro = cursor.fetchone()

    cursor.close()
    conexion.close()

    if registro is None:
        return jsonify({
            "mensaje": "Registro no encontrado"
        }), 404

    return jsonify(registro)


@app.route("/baul", methods=["POST"])
def crear_registro():
    datos = request.get_json()

    plataforma = datos["Plataforma"]
    usuario = datos["usuario"]
    clave = datos["clave"]

    conexion = get_db_connection()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO baul (Plataforma, usuario, clave)
        VALUES (%s, %s, %s)
    """

    valores = (
        plataforma,
        usuario,
        clave
    )

    cursor.execute(sql, valores)

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Registro creado correctamente"
    }), 201


@app.route("/baul/<int:id_baul>", methods=["PUT"])
def actualizar_registro(id_baul):
    datos = request.get_json()

    plataforma = datos["Plataforma"]
    usuario = datos["usuario"]
    clave = datos["clave"]

    conexion = get_db_connection()
    cursor = conexion.cursor()

    sql = """
        UPDATE baul
        SET Plataforma = %s,
            usuario = %s,
            clave = %s
        WHERE id_baul = %s
    """

    valores = (
        plataforma,
        usuario,
        clave,
        id_baul
    )

    cursor.execute(sql, valores)

    conexion.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Registro no encontrado"
        }), 404

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Registro actualizado correctamente"
    })


@app.route("/baul/<int:id_baul>", methods=["DELETE"])
def eliminar_registro(id_baul):
    conexion = get_db_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM baul WHERE id_baul = %s",
        (id_baul,)
    )

    conexion.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Registro no encontrado"
        }), 404

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Registro eliminado correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)