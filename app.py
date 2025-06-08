from app import create_app
from config import Config, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=Config.find_available_port())
