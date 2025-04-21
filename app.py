from app import create_app
from config import Config
import os


app = create_app()
port = Config.find_available_port()

if __name__ == "__main__":
    app.run(debug=False, port=port)