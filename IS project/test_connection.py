from database import get_connection

try:
    conn = get_connection()
    print("Conexiunea la baza de date a reușit!")
    conn.close()
except Exception as e:
    print("Eroare la conectarea bazei de date:", e)
