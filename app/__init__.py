from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Guilhormo@123'

    from app.routes import principal, avaliacoes, pedidos, relatorios

    app.register_blueprint(principal.bp)
    app.register_blueprint(avaliacoes.bp)
    app.register_blueprint(pedidos.bp)
    app.register_blueprint(relatorios.bp)

    return app