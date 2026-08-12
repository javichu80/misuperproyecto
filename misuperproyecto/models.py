import reflex as rx
from typing import Optional # Es buena práctica importarlo para IDs
from sqlmodel import Field, SQLModel # # SQLModel es la base que Reflex prefiere ahora

class Materia(SQLModel, table=True):
    """Modelo de base de datos siguiendo el nuevo estándar de Reflex."""
    # En SQLModel es mejor definir el ID de forma explícita
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    curso: str
    categoria: str
    descripcion: str
    precio: int
    icono: str
    url_demo: str = ""

























'''
class Materia:
    """Clase pura de Python para organizar los datos STEM."""
    def __init__(self, nombre, curso, categoria, descripcion, precio, icono, url_demo=""):
        self.nombre = nombre
        self.curso = curso
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.icono = icono
        self.url_demo = url_demo

    def to_dict(self):
        """Convierte el objeto a diccionario para que Reflex lo entienda sin errores."""
        return {
            "nombre": self.nombre,
            "curso": self.curso,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "icono": self.icono,
            "url_demo": self.url_demo,
        }

    '''