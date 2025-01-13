try:
    import mysql.connector
    print("MySQL Connector este instalat!")
    print("Versiune:", mysql.connector.__version__)
except ImportError:
    print("MySQL Connector nu este instalat!")