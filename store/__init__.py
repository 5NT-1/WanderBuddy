import os
from dotenv import load_dotenv
from peewee import *

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT") or '')

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

def create_tables():
    with db:
        db.create_tables([Trip, Location])

class BaseModel(Model):
    class Meta:
        database = db

class Trip(BaseModel):
    chat_id = CharField()

class Location(BaseModel):
    trip = ForeignKeyField(Trip, backref='locations')
    start_date = DateTimeField()
    end_date = DateTimeField()
    name = CharField()
