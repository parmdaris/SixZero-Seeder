from fastapi import FastAPI, Query
import requests, math, json

import connection

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
    return [{
        "gameId": 0,
        "numbers": [],
        "date_generated": "0000",
        "date_finished": "",
        "finished": False,
        "comments": ""
    }]

@app.get("/getGame")
def getGame(gameId: int = Query(ge=1, description="ID do jogo")):
    pass

@app.get("/getTypes")
def getTypes():
    return [
        {
            "id": 0,
            "name": "TYPE",
            "qtyNumbers": 6,
            "minNumbers": 1,
            "maxNumbers": 6
        }
    ]

@app.post("/saveGame")
def saveGame(
    typeId: int = Query(description="ID do tipo de jogo"),
    qtyNo: int = Query(description="Quantidade de Números"),
    seed: int = Query(description="Seed do jogo"),
    date_generated: str = Query(description="Data de geração"),
    numbers: list = Query(description="Números do jogo")
):
    gamedata = {
        "typeId": typeId,
        "qtyNo": qtyNo,
        "seed": seed,
        "date_generated": date_generated,
        "numbers": numbers
    }

    return connection.saveGame(gamedata)

@app.post("/finishGame")
def finishGame(gameId: int = Query(1, description="ID do jogo")):
    pass

@app.post("/newType")
def newType(qty: int = Query(1, description="Quantidade de números por jogo"),
            min: int = Query(1, description="Valor mínimo"),
            max: int = Query(1, description="Valor máximo"),
            name: str = Query(description="Nome do tipo")):
    pass
