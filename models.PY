from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="cliente")
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password) # Guardar en password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def es_admin(self):
        return self.rol == "admin"

    def __repr__(self):
        return f"<Usuario {self.email}({self.rol})>"

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    precio_base = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0) # Corregido Interger
    activo = db.Column(db.Boolean, default=True)

    imagen = db.Column(db.String(255), nullable=True, default="default.jpg")

    # Producto Fisico
    peso_kg = db.Column(db.Float, nullable=True)
    costo_envio_por_kg = db.Column(db.Float, nullable=True)

    # Producto Perecible
    dias_para_vencer = db.Column(db.Integer, nullable=True) # Corregido a Integer

    # Producto Digital
    licencia = db.Column(db.String(20), nullable=True)

    # Columna que decide qué clase usar
    tipo = db.Column(db.String(30))

    __mapper_args__ = {
        "polymorphic_identity": "producto",
        "polymorphic_on": tipo
    }

    def precio_final(self):
        return self.precio_base

    def ficha(self):
        return f"{self.codigo} {self.nombre} 1 Precio Final: {self.precio_final():.2f} | Stock: {self.stock}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.codigo} {self.nombre}>"
    
class ProductoFisico(Producto):
    __mapper_args__ = {"polymorphic_identity": "fisico"} # Corregido __mapper_args__

    def precio_final(self):
        envio = (self.peso_kg or 0) * (self.costo_envio_por_kg or 0)
        return self.precio_base + envio

class ProductoDigital(Producto):
    __mapper_args__ = {"polymorphic_identity": "digital"} # Corregido __mapper_args__

    MULTIPLICADORES = {
        "personal": 1.0,
        "comercial": 2.5,
        "educativa": 0.6,
    }

    def precio_final(self):
        multiplicador = self.MULTIPLICADORES.get(self.licencia, 1.0)
        return self.precio_base * multiplicador

class ProductoPerecible(Producto):
    __mapper_args__ = {"polymorphic_identity": "perecible"} # Corregido __mapper_args__

    def precio_final(self):
        dias = self.dias_para_vencer
        if dias is None:
            return self.precio_base
        if dias <= 3:
            return self.precio_base * 0.50
        elif dias <= 7:
            return self.precio_base * 0.80
        return self.precio_base
