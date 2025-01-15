import json

from api.rag2_websocket import Rag2Websocket
from games.flappy.models.flappy_gestures import get_flappy_move_from_gesture
from games.happy.models.happy_gestures import get_happy_move_from_gesture


class HappyGestures(Rag2Websocket):
    def send_data(self, receivedData):
        move = get_happy_move_from_gesture()
        self.write_message(json.dumps({'jump': 1,'move': move}))