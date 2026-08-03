import reflex as rx
from .models import Materia

class State(rx.State):
    brand_name: str = "Mi Academia STEM"
    filtro_curso: str = "Todos"
    
    # Convertimos los objetos a diccionarios al inicializar
    paquetes: list[dict] = [
        Materia("Mates Fáciles", "1º ESO", "Mates", "Dominio de EBAU.", 45.0, "calculator").to_dict(),
        Materia("Tecnologia", "2º ESO", "Naturaleza", "maquinaria industrial.", 35.0, "settings").to_dict(),
        Materia("Iniciación a la Robótica", "4º ESO", "Tecnología", "Arduino práctico.", 25.0, "cpu").to_dict(),
        Materia("Química", "2º Bachillerato", "Física", "Dominio de EBAU.", 45.0, "flask-conical").to_dict(),
        Materia("Álgebra Lineal", "1º Bachillerato", "Matemáticas", "Matrices y cálculo.", 35.0, "pi").to_dict(),
        Materia("Robótica", "4º ESO", "Automatas", "MicroBIT.", 25.0, "bot").to_dict(),
        Materia("Química", "3º ESO", "Tecnología", "Arduino práctico.", 50.0, "atom").to_dict(),    ]

    @rx.var
    def paquetes_filtrados(self) -> list[dict]:
        if self.filtro_curso == "Todos":
            return self.paquetes
        return [p for p in self.paquetes if p["curso"] == self.filtro_curso]

    def set_filtro(self, curso: str):
        self.filtro_curso = curso