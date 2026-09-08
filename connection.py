import psycopg2 as pg, math, os
from datetime import datetime
from psycopg2.extras import execute_values

# DB_ADDR="********"
# DB_PORT="********"
# DB_NAME="********"
# DB_USER="********"
# DB_PASSWORD="********"

def get_connection():
    return pg.connect(
        host=os.getenv("DB_ADDR"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def saveGame(gamedata):
    conn = get_connection()
    cursor = conn.cursor()
    conn.autocommit = True

    try:
        sql = """INSERT INTO "sixzero-seeder".games (gameid, type, qtyno, seed, date_generated) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, ())
        
    finally:
        cursor.close()
        conn.close()

    return {
        "message": "Jogo salvo com sucesso!",
        "status": 0
    }