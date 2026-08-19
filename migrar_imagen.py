"""Agrega la columna de imagen a una base existente sin borrar sus datos."""

from sqlalchemy import inspect, text

from app import app
from models import db


with app.app_context():
    columnas = {columna["name"] for columna in inspect(db.engine).get_columns("productos")}
    if "imagen" not in columnas:
        with db.engine.begin() as conexion:
            conexion.execute(text(
                "ALTER TABLE productos ADD COLUMN imagen VARCHAR(255) DEFAULT 'default.jpg'"
            ))
            conexion.execute(text(
                "UPDATE productos SET imagen = 'default.jpg' WHERE imagen IS NULL"
            ))
        print("Migracion completada: columna imagen agregada.")
    else:
        print("La columna imagen ya existe; no se realizaron cambios.")