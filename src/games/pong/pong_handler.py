import json
import random

from api.rag2_websocket import Rag2Websocket
from games.pong.models.pong_gestures import get_pong_move_from_gesture


class PongRandom(Rag2Websocket):
    def send_data(self, receivedData):
        move = random.choice([-1, 0, 1])
        self.write_message(json.dumps({'move': move}))


class PongBot(Rag2Websocket):
    def send_data(self, data):
        if data['playerId'] == 0:
            if data['state']['ballY'] < data['state']['leftPaddleY'] + 50:
                move = 1
            else:
                move = -1
        else:
            if data['state']['ballY'] < data['state']['rightPaddleY'] + 50:
                move = 1
            else:
                move = -1
        self.write_message(json.dumps({'move': move}))


class PongGestures(Rag2Websocket):
    def send_data(self, receivedData):
        move = get_pong_move_from_gesture(receivedData)
        self.write_message(json.dumps({'move': move}))
