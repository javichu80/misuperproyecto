import reflex as rx
from .models import Materia

class State(rx.State):
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Alumnos de instituto"
    
    # Convertimos los objetos a diccionarios al inicializar
    paquetes: list[dict] = [
        Materia("Física Moderna", "2º Bachillerato", "Física", "Dominio de EBAU.", 45.0, "atom").to_dict(),
        Materia("Álgebra Lineal", "1º Bachillerato", "Matemáticas", "Matrices y cálculo.", 35.0, "grid").to_dict(),
        Materia("Iniciación a la Robótica", "4º ESO", "Tecnología", "Arduino práctico.", 25.0, "cpu").to_dict(),
        Materia("Qímica", "4º ESO", "Tecnología", "Arduino práctico.", 50.0, "cpu").to_dict(),    ]

    @rx.var
    def paquetes_filtrados(self) -> list[dict]:
        if self.filtro_curso == "Todos":
            return self.paquetes
        return [p for p in self.paquetes if p["curso"] == self.filtro_curso]

    def set_filtro(self, curso: str):
        self.filtro_curso = curso