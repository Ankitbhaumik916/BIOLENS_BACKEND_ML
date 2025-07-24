import mysql.connector as myp

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'KAERMORHEN2311',
    'database': 'nutrition_db'
}

def get_db_connection():
    return myp.connect(**db_config)
