from flask import Blueprint, render_template, request, redirect, url_for
from app.dao import PedidosDAO

bp = Blueprint('pedidos', __name__)
pedidos_dao = PedidosDAO()

@bp.route("/pedidos")
def mostrar_pedidos():
    pedidos_avaliar = pedidos_dao.buscar_pedidos_para_avaliar()
    return render_template("listar_pedidos.html", pedidos = pedidos_avaliar)
