import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="impordycom_web"
    )

    return conexion