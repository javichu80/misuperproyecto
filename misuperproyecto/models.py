import reflex as rx

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