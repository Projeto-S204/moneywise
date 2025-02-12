from app import create_app
from config import find_available_port

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=find_available_port())
