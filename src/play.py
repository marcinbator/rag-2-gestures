import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

from games.flappy.flappy_handler import FlappyGestures
from games.flappy.models.flappy_gestures import flappy_start_gesture_recognition
from games.pong.models.pong_gestures import pong_start_gesture_recognition
from games.pong.pong_handler import PongGestures, PongBot, PongRandom

socket_registry = [
    (r"/ws/pong/", PongGestures),  # http://localhost:8001/ws/pong/
    (r"/ws/pong-bot/", PongBot),  # http://localhost:8001/ws/pong-bot/
    (r"/ws/pong-random/", PongRandom),  # http://localhost:8001/ws/pong-random/

    (r"/ws/flappy/", FlappyGestures),  # http://localhost:8001/ws/flappy/
]


def launch_models():
    # pong_gest_thread = threading.Thread(target=pong_start_gesture_recognition)
    flappy_gest_thread = threading.Thread(target=flappy_start_gesture_recognition)
    
    # pong_gest_thread.start()
    flappy_gest_thread.start()


if __name__ == "__main__":
    launch_models()

    app = tornado.web.Application(socket_registry)
    app.listen(8001)
    tornado.ioloop.IOLoop.current().start()
