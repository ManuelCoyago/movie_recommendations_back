from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from pydantic import BaseModel, Field, validator
from typing import Optional

# Modelo SQLAlchemy
class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    puntaje = Column(Integer, nullable=False)
    comentario = Column(String, nullable=False)
    vista = Column(Boolean, default=False)

# Modelo Pydantic (entrada)
class Movie(BaseModel):
    titulo: str = Field(..., min_length=1, description="Título de la película o serie")
    genero: str = Field(..., min_length=1, description="Género o categoría")
    puntaje: int = Field(..., ge=1, le=10, description="Puntaje entre 1 y 10")
    comentario: str = Field(..., min_length=1, description="Opinión personal")
    vista: Optional[bool] = Field(default=False, description="Si ya ha sido vista")

    @validator('titulo', 'genero' , 'comentario')
    def no_empty_strings(cls, v):
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v

# Modelo Pydantic (respuesta)
class MovieResponse(Movie):
    id: int

    class Config:
        orm_mode = True
