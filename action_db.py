import pyodbc 
import sqlalchemy
import pandas as pd

server = 'DESKTOP-6DEN14D\SQLEXPRESS'
database = 'action_db'


engine = sqlalchemy.create_engine('mssql+pyodbc://{0}/{1}?driver=SQL Server?Trusted_Connection=yes'.format(server, database))


data = pd.read_csv(r'C:\Users\smsmi\VS Projects\rest_api\finished_imdb_dataset_actual.csv')

data.to_sql('action_flicks', engine)
