from flask import Blueprint
from app.services import (
    baul_list,
    baul_detail,
    baul_add,
    baul_update,
    baul_delete
)

baul_bp = Blueprint("baul", __name__)

@baul_bp.route("/baul", methods=["GET"])
def get_baul_list():
    return baul_list()

@baul_bp.route("/baul/<int:id_baul>", methods=["GET"])
def get_baul_detail(id_baul):
    return baul_detail(id_baul)

@baul_bp.route("/baul", methods=["POST"])
def post_baul_add():
    return baul_add()

@baul_bp.route("/baul/<int:id_baul>", methods=["PUT"])
def put_baul_update(id_baul):
    return baul_update(id_baul)

@baul_bp.route("/baul/<int:id_baul>", methods=["DELETE"])
def delete_baul_delete(id_baul):
    return baul_delete(id_baul)