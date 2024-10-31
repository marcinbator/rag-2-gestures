import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

from games.pong.models.pong_gestures import start_gesture_recognition
from games.pong.pong_handler import PongGestures, PongBot, PongRandom

socket_registry = [
    (r"/ws/pong/", PongGestures),  # http://localhost:8001/ws/pong/
    (r"/ws/pong-bot/", PongBot),  # http://localhost:8001/ws/pong-bot/
    (r"/ws/pong-random/", PongRandom),  # http://localhost:8001/ws/pong-random/
]


def launch_models():
    gest_thread = threading.Thread(target=start_gesture_recognition)
    gest_thread.start()


if __name__ == "__main__":
    launch_models()

    app = tornado.web.Application(socket_registry)
    app.listen(8001)
    tornado.ioloop.IOLoop.current().start()
