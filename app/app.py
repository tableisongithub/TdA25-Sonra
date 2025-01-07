from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from typing import List, Dict
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime

app = FastAPI()

# Models
class Game(BaseModel):
    uuid: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    difficulty: str
    gameState: str = Field(default="new")
    board: List[List[str]]

class GameCreate(BaseModel):
    name: str
    difficulty: str
    gameState: str = Field(default="new")
    board: List[List[str]] = Field(default_factory=lambda: [["."] * 15 for _ in range(15)])

class GameUpdate(BaseModel):
    name: str
    difficulty: str
    board: List[List[str]]

# In-memory storage
GAMES: Dict[str, Game] = {}

# Helpers
def validate_uuid4(uuid: str) -> bool:
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False
    return True

# Routes
@app.post("/api/v1/games", status_code=201)
def create_game(game_data: GameCreate):
    uuid = str(uuid4())
    now = datetime.utcnow()

    game = Game(
        uuid=uuid,
        createdAt=now,
        updatedAt=now,
        **game_data.dict()
    )

    if len(game.board) != 15 or any(len(row) != 15 for row in game.board):
        raise HTTPException(status_code=400, detail="Invalid board dimensions. Board must be 15x15.")

    GAMES[uuid] = game
    return game

@app.get("/api/v1/games/{uuid}")
def get_game(uuid: str):
    if not validate_uuid4(uuid):
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    game = GAMES.get(uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")
    return game

@app.put("/api/v1/games/{uuid}")
def update_game(uuid: str, updated_data: GameUpdate):
    if not validate_uuid4(uuid):
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    game = GAMES.get(uuid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")

    updated_game = Game(
        uuid=game.uuid,
        createdAt=game.createdAt,
        updatedAt=datetime.utcnow(),
        name=updated_data.name or game.name,
        difficulty=updated_data.difficulty or game.difficulty,
        board=updated_data.board or game.board,
        gameState=game.gameState
    )

    GAMES[uuid] = updated_game
    return updated_game

@app.delete("/api/v1/games/{uuid}", status_code=204)
def delete_game(uuid: str):
    if not validate_uuid4(uuid):
        raise HTTPException(status_code=400, detail="Invalid UUID format.")
    if uuid not in GAMES:
        raise HTTPException(status_code=404, detail="Game not found.")
    del GAMES[uuid]

@app.get("/api/v1/games")
def list_games():
    return list(GAMES.values())
