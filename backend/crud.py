# crud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import MovieModel, Movie, MovieResponse
from typing import List
from dependencies import get_db


router = APIRouter()

@router.get("/movies", response_model=List[MovieResponse])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(MovieModel).offset(skip).limit(limit).all()
    return movies

@router.post("/movies", response_model=MovieResponse)
def create_movie(movie: Movie, db: Session = Depends(get_db)):
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/movies/{movie_id}", response_model=MovieResponse)
def read_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: Movie, db: Session = Depends(get_db)):
    db_movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    for key, value in movie.dict().items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/movies/{movie_id}", response_model=MovieResponse)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return db_movie
