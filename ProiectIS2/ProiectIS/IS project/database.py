import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Sasha2014",
            database="royal_fitness"
        )
        if connection.is_connected():
            print("Conexiune reușită la baza de date!")
            return connection
    except Error as e:
        print(f"Eroare: {e}")
        raise e

if __name__ == "__main__":
    # Acest cod rulează doar când rulezi direct database.py
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        print(f"Număr de utilizatori în baza de date: {result[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Eroare la testarea conexiunii: {e}")