import json

from api.rag2_websocket import Rag2Websocket
from games.flappy.models.flappy_gestures import get_flappy_move_from_gesture
from games.happy.models.happy_gestures import get_happy_move_from_gesture
from games.skijump.models.skijump_gestures import get_skijump_move_from_gesture


class SkijumpGestures(Rag2Websocket):
    def send_data(self, receivedData):
        space, up, down = get_skijump_move_from_gesture()
        self.write_message(json.dumps({'space': space,'up': up, 'down': down}))