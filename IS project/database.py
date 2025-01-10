import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#Sasha2014",
        database="royal_fitness"
    )
