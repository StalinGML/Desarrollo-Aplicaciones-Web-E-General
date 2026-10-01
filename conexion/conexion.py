import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="impordycom_web",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )