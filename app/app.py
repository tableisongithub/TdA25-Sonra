from flask import Flask, request, jsonify, abort

from uuid import uuid4, UUID

from datetime import datetime

from pydantic import BaseModel, Field, ValidationError

from typing import List, Dict


app = Flask(__name__)


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

@app.route("/api/v1/games", methods=["POST"])

def create_game():

    game_data = request.json

    try:

        game_create = GameCreate(**game_data)

    except ValidationError as e:

        return jsonify(e.errors()), 400


    uuid = str(uuid4())

    now = datetime.utcnow()


    game = Game(

        uuid=uuid,

        createdAt=now,

        updatedAt=now,

        **game_create.dict()

    )


    if len(game.board) != 15 or any(len(row) != 15 for row in game.board):

        return jsonify({"detail": "Invalid board dimensions. Board must be 15x15."}), 400


    GAMES[uuid] = game

    return jsonify(game.dict()), 201


@app.route("/api/v1/games/<uuid>", methods=["GET"])

def get_game(uuid):

    if not validate_uuid4(uuid):

        return jsonify({"detail": "Invalid UUID format."}), 400

    game = GAMES.get(uuid)

    if not game:

        return jsonify({"detail": "Game not found."}), 404

    return jsonify(game.dict())


@app.route("/api/v1/games/<uuid>", methods=["PUT"])

def update_game(uuid):

    if not validate_uuid4(uuid):

        return jsonify({"detail": "Invalid UUID format."}), 400

    game = GAMES.get(uuid)

    if not game:

        return jsonify({"detail": "Game not found."}), 404


    updated_data = request.json

    try:

        game_update = GameUpdate(**updated_data)

    except ValidationError as e:

        return jsonify(e.errors()), 400


    updated_game = Game(

        uuid=game.uuid,

        createdAt=game.createdAt,

        updatedAt=datetime.utcnow(),

        name=game_update.name or game.name,

        difficulty=game_update.difficulty or game.difficulty,

        board=game_update.board or game.board,

        gameState=game.gameState

    )


    GAMES[uuid] = updated_game

    return jsonify(updated_game.dict())


@app.route("/api/v1/games/<uuid>", methods=["DELETE"])

def delete_game(uuid):

    if not validate_uuid4(uuid):

        return jsonify({"detail": "Invalid UUID format."}), 400

    if uuid not in GAMES:

        return jsonify({"detail": "Game not found."}), 404

    del GAMES[uuid]

    return '', 204


@app.route("/api/v1/games", methods=["GET"])

def list_games():

    return jsonify([game.dict() for game in GAMES.values()])


if __name__ == "__main__":

    app.run(debug=True)
