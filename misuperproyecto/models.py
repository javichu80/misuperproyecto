import reflex as rx

# Usamos rx.Base para que Reflex pueda "entender" y mostrar estos datos en la web
class Materia(rx.Base):
    nombre: str
    curso: str       # Ej: Segundo Bachillerato
    categoria: str   # Ej: Fisica, Matematicas
    descripcion: str
    precio: float
    icono: str       # Nombre de un icono (ej: "atom", "function")