import pyodbc

try:
    # Update with your actual database details
    conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ANUSHREE\SQLEXPRESS;'  # Your server instance
    'DATABASE=FlaskAppDB;'          # Your database name
    'Trusted_Connection=yes;'       # Windows Authentication
    )
    print("Connected successfully!")
except Exception as e:
    print("Connection failed:", str(e))


