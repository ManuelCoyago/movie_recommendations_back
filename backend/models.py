from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Modelo SQLAlchemy
class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    puntaje = Column(Integer, nullable=False)
    comentario = Column(String, nullable=False)
    vista = Column(Boolean, default=False)

