import scipy
import pandas as pd
from database.connection import Connection


base_df = None


def build_table():
    global base_df

    conn = Connection()
    cnx = conn.connect()
    cursor = cnx.cursor()

    query = """SELECT json_agg(dt) FROM (
                    SELECT m."id",
                           m."name",
                           m."rating" as "score",
                           m."image_url" as "image",
                           json_agg(g) as "genres"
                    FROM public."movie" m 
                    LEFT JOIN public."movie_genres" mg
                    ON m."id" = mg."id_movie"
                    LEFT JOIN public."genre" g
                    ON g."id" = mg."id_genre"
                    GROUP by m."id"
                    ORDER BY m."id"
               )dt"""

    cursor.execute(query)
    result = cursor.fetchone()[0]

    dataframe = pd.DataFrame(columns=["id", "name", "image", "score", "g-action", "g-adventure", "g-animation", "g-comedy",
                                      "g-drama", "g-family", "g-fantasy", "g-horror", "g-musical", "g-history", "g-mystery",
                                      "g-reality-show", "g-romance", "g-sport", "g-talk-show", "g-thriller", "g-war", "g-police"])

    genre_translator = {
        "Ação": "g-action",
        "Aventura": "g-adventure",
        "Animação": "g-animation",
        "Biografia": "g-history",
        "Comédia": "g-comedy",
        "Documentário": "g-history",
        "Drama": "g-drama",
        "Família": "g-family",
        "Fantasia": "g-fantasy",
        "Game-Show": "g-fantasy",
        "História": "g-history",
        "Terror": "g-horror",
        "Musical": "g-musical",
        "Mistério": "g-mystery",
        "Jornal": "g-history",
        "Reality-Show": "g-reality-show",
        "Romance": "g-romance",
        "Sci-Fi": "g-fantasy",
        "Curta-Metragem": "",
        "Esporte": "g-sport",
        "Talk-Show": "g-talk-show",
        "Thriller": "g-thriller",
        "Guerra": "g-war",
        "Policial": "g-police",
    }

    for movie in result:
        row = {
            "id": movie["id"],
            "name": movie["name"],
            "image": movie["image"],
            "score": movie["score"],
            "g-action": 0,
            "g-adventure": 0,
            "g-animation": 0,
            "g-comedy": 0,
            "g-drama": 0,
            "g-family": 0,
            "g-fantasy": 0,
            "g-horror": 0,
            "g-musical": 0,
            "g-history": 0,
            "g-mystery": 0,
            "g-reality-show": 0,
            "g-romance": 0,
            "g-sport": 0,
            "g-talk-show": 0,
            "g-thriller": 0,
            "g-war": 0,
            "g-police": 0
        }

        for genre in movie["genres"]:
            if genre is not None:
                translated_name = genre_translator[genre["alias"]]
                row[translated_name] += 1

        new_df = pd.DataFrame(row, index=[row["id"]])
        dataframe = pd.concat([dataframe, new_df])

    base_df = dataframe


def get_recommendations(likes=None, dislikes=None):

    global base_df

    if likes is None:
        likes = []

    if dislikes is None:
        dislikes = []

    if base_df is None:
        base_df = pd.DataFrame()
        build_table()

    liked_reference = []
    for liked_movie in likes:
        try:
            movie_info = base_df.loc[[liked_movie]].values[0][3:]
            user_neighbors = [base_df.values[j][0] for j in range(len(base_df)) if
                              scipy.spatial.distance.euclidean(movie_info, base_df.values[j][3:]) < 0.9]

            liked_reference.extend(user_neighbors)
        except Exception:
            pass

    disliked_reference = []
    for disliked_movie in dislikes:
        try:
            movie_info = base_df.loc[[disliked_movie]].values[0][3:]
            user_neighbors = [base_df["id"][j] for j in range(len(base_df)) if
                              scipy.spatial.distance.euclidean(movie_info, base_df.iloc[[j]].values[0][3:]) < 0.05]

            disliked_reference.extend(user_neighbors)
        except Exception:
            pass

    reference = list(set(liked_reference) - set(disliked_reference))

    result = base_df.loc[reference].iloc[:, :4].to_dict(orient='records')

    return result

