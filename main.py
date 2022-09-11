import os
from sanic import Sanic

from controllers import movies_controller, genre_controller, platforms_controller

app = Sanic("backend")


if __name__ == "__main__":
    movies_controller.create_app(app)
    genre_controller.create_app(app)
    platforms_controller.create_app(app)

    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", 8090))
    debug = os.getenv("PRODUCTION", "false").lower() not in ["true", "1"]
    app.run(host=host, port=port, debug=debug)
