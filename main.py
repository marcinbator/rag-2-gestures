import tornado.ioloop
import tornado.web
import tornado.websocket

from pong import PongWebSocketHandler


def make_app():
    return tornado.web.Application([
        (r"/ws/pong/", PongWebSocketHandler),  # http://localhost:8005/ws/pong/
    ])


def run():
    app = make_app()
    app.listen(8005)
    print("Started")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
