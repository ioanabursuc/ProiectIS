from database import get_connection
from mysql.connector import Error

print("Start test conexiune...")

try:
    connection = get_connection()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"Conectat la baza de date: {db_name}")
        cursor.close()
        connection.close()
        print("Conexiunea MySQL este închisă")

except Error as e:
    print(f"A apărut o eroare MySQL: {e}")
except Exception as e:
    print(f"A apărut o altă eroare: {e}")

input("Apasă Enter pentru a ieși...")