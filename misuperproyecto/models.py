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


class ProgresoLeccion(SQLModel, table=True):
    """Guarda el progreso real de las lecciones completadas por cada alumno."""
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: str = Field(index=True)  # Ej: 'lesson_01', 'lesson_02'
    completada: bool = Field(default=True)
    
    # 🚀 PROYECCIÓN DE FUTURO: Dejamos el email listo para cuando tengamos base de datos de usuarios
    usuario_email: str = Field(default="alumno@misuperproyecto.com", index=True)

















