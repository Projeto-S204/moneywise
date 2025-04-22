from flask import Flask
from app import db
from app.transactions.routes import transactions_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)