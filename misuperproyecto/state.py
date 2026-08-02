import reflex as rx
from .models import Materia # Importamos el molde que acabamos de crear

class State(rx.State):
    # Lista profesional de paquetes basada en tu nicho
    paquetes: list[Materia] = [
        Materia(
            nombre="Física Moderna", 
            curso="2º Bachillerato", 
            categoria="Física",
            descripcion="Dominio de relatividad y cuántica para EBAU.", 
            precio=45.0, 
            icono="atom"
        ),
        Materia(
            nombre="Álgebra Lineal", 
            curso="1º Bachillerato", 
            categoria="Matemáticas",
            descripcion="Matrices, determinantes y sistemas de ecuaciones.", 
            precio=35.0, 
            icono="grid"
        ),
        Materia(
            nombre="Iniciación a la Robótica", 
            curso="4º ESO", 
            categoria="Tecnología",
            descripcion="Paquete práctico con Arduino y sensores.", 
            precio=25.0, 
            icono="cpu"
        ),
    ]

    def seleccionar_paquete(self, nombre: str):
        # Esta función (evento) permitiría saber qué paquete quiere comprar el alumno
        return rx.window_alert(f"Has seleccionado el paquete: {nombre}")
