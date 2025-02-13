from app import create_app, db
from config import find_available_port
from app.users_authentication.models import User  # noqa: F401


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=find_available_port())
