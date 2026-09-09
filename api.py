from fastapi import FastAPI, Query
import requests, math, json

import connection as conn

app = FastAPI(
    title="SixZero Seeder API",
    description="""
            API para transmissão e recepção de dados do sistema SixZero.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/getAllGames")
def getAllGames():
    return conn.getAllGames()

@app.get("/getGame")
def getGame(gameId: int = Query(ge=1, description="ID do jogo")):
    pass

@app.get("/getTypes")
def getTypes():
    return conn.getTypes()

@app.post("/saveGame")
def saveGame(
    type_id: int = Query(description="ID do tipo de jogo"),
    qtyno: int = Query(description="Quantidade de Números"),
    seed: str = Query(description="Seed do jogo"),
    numbers: list[int] = Query(description="Números do jogo", min_length=1, max_length=30),
    comments: str = Query("", description="Comentários")
):
    gamedata = {
        "type_id": typeId,
        "qtyno": qtyno,
        "seed": seed,
        "numbers": numbers,
        "comments": comments or ""
    }

    return conn.saveGame(gamedata)

@app.post("/finishGame")
def finishGame(gameId: int = Query(1, description="ID do jogo")):
    return conn.finishGame(gameId)

@app.post("/newType")
def newType(name: str = Query(description="Nome do tipo"),
            qty: int = Query(1, description="Quantidade de números por jogo"),
            minval: int = Query(1, description="Valor mínimo"),
            maxval: int = Query(1, description="Valor máximo"),
            cost: float = Query(description="Valor")
            ):
    return conn.newType(name, qty, minval, maxval, cost)
