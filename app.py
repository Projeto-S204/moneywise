from app import create_app
from config import Config
import os


app = create_app()
port = int(os.getenv("AVAILABLE_PORT", 5000))

if __name__ == "__main__":
    app.run(debug=False, port=port)