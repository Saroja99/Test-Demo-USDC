import urllib.parse
import os

DATABASE_CONFIG = {
    "DRIVER": "ODBC Driver 17 for SQL Server",  # Ensure you have this driver installed
    "SERVER": "192.168.168.17",  # Replace with the actual IP address of your database server
    "DATABASE": "OnlineCourses_Do_Not_Delete",  # Your database name
    "USERNAME": "sa",  # SQL Server authentication username
    "PASSWORD": "Sql@4343",  # SQL Server authentication password
}

# Construct the connection string parameters securely
params = urllib.parse.quote_plus(
    f"DRIVER={DATABASE_CONFIG['DRIVER']};"
    f"SERVER={DATABASE_CONFIG['SERVER']};"
    f"DATABASE={DATABASE_CONFIG['DATABASE']};"
    f"UID={DATABASE_CONFIG['USERNAME']};"
    f"PWD={DATABASE_CONFIG['PASSWORD']};"
)

# SQLAlchemy Database URI
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

# Secret Key (Use environment variable for security - recommended)
SECRET_KEY = os.environ.get("SECRET_KEY", "b216c829e7bc9a28bef0ec46b2fe6d1c97e272f91ba3bbce")









# import urllib.parse
# import os

# DATABASE_CONFIG = {
#     "DRIVER": "ODBC Driver 17 for SQL Server",  # Ensure the correct ODBC driver is installed
#     "SERVER": "192.168.168.17",  # SQL Server instance
#     "DATABASE": "OnlineCourses_Do_Not_Delete",  # Your database name
#     "USERNAME": "sa",  # Replace with your SQL Server username
#     "PASSWORD": "Sql@4343",  # Replace with your SQL Server password
# }

# # Construct the connection string parameters for SQL Authentication
# params = urllib.parse.quote_plus(
#     "DRIVER=" + DATABASE_CONFIG["DRIVER"] + ";" +
#     "SERVER=" + DATABASE_CONFIG["SERVER"] + ";" +
#     "DATABASE=" + DATABASE_CONFIG["DATABASE"] + ";" +
#     "UID=" + DATABASE_CONFIG["USERNAME"] + ";" +  # SQL Server username
#     "PWD=" + DATABASE_CONFIG["PASSWORD"] + ";"  # SQL Server password
# )

# # SQLAlchemy Database URI
# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=" + params

# # Secret Key (Use environment variable for security)
# SECRET_KEY = os.environ.get("SECRET_KEY") or "b216c829e7bc9a28bef0ec46b2fe6d1c97e272f91ba3bbce"

# # Print the URI for debugging (remove in production)
# print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
