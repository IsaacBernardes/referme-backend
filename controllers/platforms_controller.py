from sanic import Sanic, response
from sanic.request import Request

from services.platforms_service import PlatformsService


async def list_platforms(request: Request):
    try:
        platforms_service = PlatformsService()
        result = platforms_service.list_all()
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
    app.add_route(list_platforms, "/api/platforms", methods=["GET"])
