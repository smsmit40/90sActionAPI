import pyodbc 
from typing import Optional
from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy.sql import text
import random




app = FastAPI()

#allow all origins so anyone can call from the API
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "*"
]

#allows all headers but can only call GET methods from the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)



Base = declarative_base()

#Using the 90's Action film DB to create a model to be returned for each entry in the table.
class Customers(Base):
   __tablename__ = 'action_flicks'
   Index= Column("index",Integer, primary_key=True, index=True)
   poster= Column("poster", String)
   Produced_by= Column("Produced by", String)
   Screenplay_by= Column("Screenplay by", String)
   Starring= Column("Starring", String)
   Cinematography=Column("Cinematography", String)
   Edited_by=Column("Edited by", String)
   Production_Comapnies=("Productioncompanies", String)
   Distributed_by=Column("Distributed by", String)
   Running_Time= Column("Running time", String)
   Based_on=Column("Based on", String)
   Music_By=Column("Music by", String)
   Production_Company=Column("Productioncompany", String)
   Language=Column("Language", String)
   Budget=Column("Budget", String)
   Box_OFfice=Column("Box office", String)
   Story_by=Column("Story by", String)
   Written_by=Column("Written by", String)
   Movie=Column("movie", String, unique=True)
   director=Column("director", String)
   Stars=Column("stars", String)
   Country=Column("country", String)
   Url=Column("url", String)
   Release_Year= Column("Release Year", Float)
   Released = Column("Released", String)
   Plot=Column("plot", Text)

server = 'DESKTOP-6DEN14D\SQLEXPRESS'
database = 'action_db'
SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://{0}/{1}?driver=SQL Server?Trusted_Connection=yes'.format(server, database)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
SessionLocal = sessionmaker(bind = engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

#outputs a list of all action movies in the DB
@app.get('/')
def startup(session: Session= Depends(get_db)):
    result = session.query(Customers).all()
    return(result)

#get all movies in a given year in the 90's.
@app.get('/years/{year}')
def the_year(year, session: Session= Depends(get_db)):
    try:
        int(year)
    except:
        raise HTTPException(status_code=404, detail="Integer not returned")

    today='''select *from dbo.action_flicks where action_flicks.[Release Year] ={}'''.format(year)
    result = session.query(Customers).from_statement(text(today)).all()
    if int(year) > 1999 or int(year)<1990:
        raise HTTPException(status_code =404, detail="Invalid year provided")
    return(result)

#get random action movie from the 90s.  gets the total count of movies and uses the random module to gram one and return.
@app.get('/movie_rec')
def get_movie( session: Session= Depends(get_db)):
    total_movies=session.query(Customers.Movie).count()
    movie_list = session.query(Customers).all()
    number = random.randint(0, total_movies)
    return(movie_list[number])

#uses random function and input for a given year to  get a random movie recommendation from that year.
@app.get('movie_rec/year/{year}')
def get_movie_by_year(year,  session: Session= Depends(get_db)):
    try:
        int(year)
    except:
        raise HTTPException(status_code=404, detail="Integer not returned")

    today='''select movie from dbo.action_flicks where action_flicks.[Release Year] ={}'''.format(year)
    total_movies = session.query(Customers).from_statement(text(today)).count()
    result = session.query(Customers).from_statement(text(today)).all()
    number = random.randint(0, total_movies)
    if int(year) > 1999 or int(year) <1990:
        raise HTTPException(status_code=404, detail="Invalid year provided")
    return(result[number])

#uses a LIKE %{input}% query to do a quick movie search.
@app.get('/search/title/{movie_title}')
def get_movie_by_title(movie_title, session: Session= Depends(get_db)):
    today='''select * from dbo.action_flicks where action_flicks.[movie] like '%{}%' '''.format(movie_title)
    result = session.query(Customers).from_statement(text(today)).all()
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return(result)

#using the Microsoft SQL server get random query to return a set amount of results.
#checks against query getting totatl rows and returns an error if total amount is over total row amount.
@app.get('/movie_rec/get_rand_list/{total}')
def get_random_list(total, session: Session= Depends(get_db)):
    try:
        int(total)
    except:
        raise HTTPException(status_code=404, detail="Integer not returned")

    today='SELECT TOP {} * FROM action_db.dbo.action_flicks ORDER BY NEWID()'.format(total)
    result=session.query(Customers).from_statement(text(today)).all()
    total_Rows=session.query(Customers.Movie).count()
    if int(total) > int(total_Rows) or  int(total) <=0:
        raise HTTPException(status_code=404, detail="Invalid return amount.")
    return(result)

    


