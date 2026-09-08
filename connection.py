import psycopg2 as pg, math, os
from datetime import datetime
import psycopg2.extras

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
        sql = """INSERT INTO "sixzero-seeder".games (type, qtyno, seed) VALUES (%s, %s, %s) RETURNING gameid"""
        cursor.execute(sql, (gamedata.get("type"), gamedata.get("qtyno"), gamedata.get("seed")))
        gameid = cursor.fetchone()[0]
        cursor.close()

        return {
                "message": "Jogo salvo com sucesso!",
                "status": 0,
                "gameid": gameid
            }
        
    finally:
        conn.close()


def getAllGames():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        sql = """SELECT 
                    g.gameid, 
                    g.type, 
                    t.typename, 
                    g.qtyno, 
                    g.seed, 
                    g.date_generated, 
                    g.date_finished, 
                    g.finished, 
                    g.comments 
                FROM "sixzero-seeder".games g 
                INNER JOIN "sixzero-seeder".types t on g.type = t.typeid
                ORDER BY g.gameid ASC
                """
        
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        return result

    except:
        return {
            "message": "Erro na consulta!",
            "status": 1,
            "details": ""
        }
    
    finally:
        conn.close()