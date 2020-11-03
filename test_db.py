from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base


server = 'DESKTOP-6DEN14D\SQLEXPRESS'
database = 'action_db'
SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://{0}/{1}?driver=SQL Server?Trusted_Connection=yes'.format(server, database)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
Base = declarative_base()

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


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
result = session.query(Customers).all()

movies= session.query(Customers).filter(Customers.Movie.like('%predator%'))
for movie in movies:
    print(movies)
    #print(movie.Movie)