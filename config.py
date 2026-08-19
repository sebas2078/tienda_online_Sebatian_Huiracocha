import os
from dotenv import load_dotenv

load_dotenv()

class Config: # Sin los paréntesis vacíos, es más pitónico
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "estu2026")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "tienda_online")
    
    SECRET_KEY = os.getenv("SECRET_KEY", "tienda_online_secret_key")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # Corregido: Agregada la 'S' al final
    SQLALCHEMY_TRACK_MODIFICATIONS = False
