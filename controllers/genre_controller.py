from sanic import Sanic, response
from sanic.request import Request

from services.genres_service import GenresService


async def list_genres(request: Request):
    try:
        genres_service = GenresService()
        result = genres_service.list_all()
        return response.json({"result": result}, 200)

    except KeyError as ex:
        return response.json({
            "error": "KeyError",
            "message": "Invalid request params",
            "exception": str(ex)
        }, 400)

    except Exception as ex:
        return response.json({
            "error": "DefaultError",
            "message": "Unexpected error occurred",
            "exception": str(ex)
        }, 500)


def create_app(app: Sanic):
    app.add_route(list_genres, "/api/genres", methods=["GET"])