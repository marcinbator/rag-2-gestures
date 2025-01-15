import json

from api.rag2_websocket import Rag2Websocket
from games.flappy.models.flappy_gestures import get_flappy_move_from_gesture


class FlappyGestures(Rag2Websocket):
    def send_data(self, receivedData):
        jump = get_flappy_move_from_gesture()
        if not receivedData['state']['isGameStarted']:
            self.write_message(json.dumps({'jump': 1}))
        else:
            self.write_message(json.dumps({'jump': jump}))