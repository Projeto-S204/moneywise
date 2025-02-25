from app import create_app, db
from config import find_available_port


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=find_available_port())
