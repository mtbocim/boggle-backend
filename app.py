from flask_cors import CORS
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import connect_db, db
from config import DATABASE_URL
from uuid import uuid4
from flask_bcrypt import Bcrypt
from boggle import BoggleGame
from models.lobby import Lobby
from models.player_in_lobby import PlayerInLobby
from routes.websockets.intro import IntroNamespace
from routes.websockets.lobby import LobbyNamespace
# from models.player import player


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

bcrypt = Bcrypt(app)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")


from routes.static.lobby import lobby
from routes.static.player import player

# register blueprints
app.register_blueprint(lobby, url_prefix="/lobby")
app.register_blueprint(player, url_prefix="/player")

# register websocket namespaces
socketio.on_namespace(IntroNamespace('/intro'))
socketio.on_namespace(LobbyNamespace('/lobby'))

# @socketio.on('goodbye')
# def player_disconnect(player_data):
#     print("\033[95m"+"\nWEBSOCKET: Full disconnect\n" + "\033[00m")
    
#     player_id = player_data['playerId']
#     current_lobby = player_data['currLobby']
#     player_name = player_data['playerName']
    
#     PlayerInLobby.query.filter(PlayerInLobby.player_id==player_id).delete()
#     db.session.commit()
    
#     leave_room(current_lobby)
    
#     emit(
#             'left', 
#             {
#                 "playerName":player_name, 
#                 "message":f"{player_name} has left the lobby"
#             },
#             to=current_lobby
#         )
    
    
if __name__ == '__main__':
    socketio.run(app)
CORS(app)
connect_db(app)



# The boggle games created, keyed by game id
# games = {}

# @app.get("/")
# def homepage():
#     """Show board."""

#     return render_template("index.html")


# @app.post("/api/new-game")
# def new_game():
#     """Start a new game and return JSON: {game_id, board}."""

#     # get a unique string id for the board we're creating
#     game_id = str(uuid4())
#     game = BoggleGame()
#     games[game_id] = game

#     return {"gameId": "need-real-id", "board": "need-real-board"}