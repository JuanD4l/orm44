from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db
from app.common import Config
from app.controller import baul_bp

app = Flask(__name__)

# Aplicar la configuración
app.config.from_object(Config)

# Inicializar extensiones
CORS(app)
db.init_app(app)

# Crear tablas automáticamente si no existen en la BD
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"mensaje": "Backend funcionando correctamente con ORM"})

# Registrar Blueprint de Baúl
app.register_blueprint(baul_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)