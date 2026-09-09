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
        host=os.environ["DB_ADDR"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

def saveGame(gamedata):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """INSERT INTO "sixzero-seeder".games 
                    (type, qtyno, seed, date_generated, comments) 
                    VALUES (%s, %s, %s, NOW(), %s) 
                    RETURNING gameid
            """

        cursor.execute(sql, (gamedata.get("type_id"), gamedata.get("qtyno"), gamedata.get("seed"), gamedata.get("comments")))
        gameid = cursor.fetchone()[0]

        sql_num = """INSERT INTO "sixzero-seeder".numbers
                        (number, gameid)
                        VALUES (%s, %s)
                """

        for number in gamedata.get("numbers", []):
            cursor.execute(sql_num, (number, gameid))

        conn.commit()

        return {
                "message": "Jogo salvo com sucesso!",
                "status": 0,
                "gameid": gameid
            }
    except Exception as e:
        conn.rollback()

        return {
            "message": "Erro ao salvar jogo!",
            "status": 1,
            "details": str(e)
        }

    finally:
        conn.close()

def getTypes():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        sql = """ Select 
        "type_id", 
        "type_name", 
        qty_numbers, 
        minval, 
        maxval, 
        cost 
        FROM "sixzero-seeder".gametypes 
        ORDER BY "type_id" ASC
        """

        cursor.execute(sql)
        result = cursor.fetchall()

        return result
        

    except Exception as e:
        conn.rollback()
        return {
            "message": "Erro ao consultar!",
            "status": 1,
            "details": str(e)
        }
    
    finally:
        conn.close()

def getAllGames():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        sql = """
            SELECT 
                g.gameid,
                g.type,
                gt.type_name,
                g.qtyno,
                g.seed,
                g.date_generated,
                g.date_finished,
                g.finished,
                g.comments,
                ARRAY_AGG(n.number ORDER BY n.number) AS numbers
            FROM "sixzero-seeder".games g
            INNER JOIN "sixzero-seeder".gametypes gt
                ON g.type = gt."type_id"
            LEFT JOIN "sixzero-seeder".numbers n
                ON n.gameid = g.gameid
            GROUP BY
                g.gameid,
                g.type,
                gt.type_name,
                g.qtyno,
                g.seed,
                g.date_generated,
                g.date_finished,
                g.finished,
                g.comments
            ORDER BY g.gameid DESC
        """
        
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        return result

    except Exception as e:
        conn.rollback()

        return {
            "message": "Erro ao consultar jogos!",
            "status": 1,
            "details": str(e)
        }
    
    finally:
        conn.close()


def finishGame(gameId):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """UPDATE "sixzero-seeder".games SET finished = true, date_finished = NOW() WHERE gameId = %s"""
        cursor.execute(sql, (gameId,))
        conn.commit()

        return {
            "message": "Sucesso ao atualizar status!",
            "status": 0,
            "gameid": gameId
        }

    except Exception as e:
        return {
            "message": "Erro ao atualizar status!",
            "status": 1,
            "details": str(e)
        }

    finally:
        conn.close()


def newType(typeName, qty_numbers, minval, maxval, cost):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = """INSERT INTO "sixzero-seeder".gametypes 
                    ("type_name", qty_numbers, minval, maxval, cost) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING "type_id"
            """
        cursor.execute(sql, (typeName, qty_numbSers, minval, maxval, cost))
        type_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "message": "Sucesso ao gravar novo tipo!",
            "status": 0,
            "type_id": type_id
        }

    except Exception as e:
        return {
            "message": "Erro ao inserir novo tipo!",
            "status": 1,
            "details": str(e)
        }

    finally:
        conn.close()