from sanic import Sanic, response
from sanic.request import Request

from utils.request_tools import build_query_params
from services.movies_service import MoviesService
from services.genres_service import GenresService
from services.platforms_service import PlatformsService


async def list_movies(request: Request):
    try:

        movies_service = MoviesService()

        query_params = build_query_params(request.query_args)
        page = int(query_params.get("page", 0))
        result = movies_service.list_all_paginated(page, 100)
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


async def list_trends(request: Request):
    try:

        movies_service = MoviesService()
        result = movies_service.list_popular()
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


async def list_movie_details(request: Request, movie_id: int):
    try:

        movies_service = MoviesService()
        genres_service = GenresService()
        platforms_service = PlatformsService()

        result = movies_service.find_one(movie_id)
        if result is not None:
            result["genres"] = genres_service.list_all_by_movie(movie_id)
            result["platforms"] = platforms_service.list_all_by_movie(movie_id)

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
    app.add_route(list_movies, "/api/movies", methods=["GET"])
    app.add_route(list_trends, "/api/trends", methods=["GET"])
    app.add_route(list_movie_details, "/api/movies/<movie_id:int>", methods=["GET"])

