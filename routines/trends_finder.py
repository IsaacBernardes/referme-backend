import json
import os
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from models.Movie import Movie
from services.movies_service import MoviesService


def trends_schedule():
    last_search = open("routines/last_search.txt", "r").read()

    if last_search is None or len(last_search) == 0:
        next_search = datetime.now()
    else:
        last_search = datetime.fromisoformat(last_search)
        next_search = last_search + timedelta(weeks=1)

    if datetime.now() > next_search:
        schedule_and_execute()
    else:
        scheduler = BackgroundScheduler()
        scheduler.scheduled_job(func=schedule_and_execute, trigger='date', run_date=next_search)


def schedule_and_execute():
    scheduler = BackgroundScheduler()
    scheduler.scheduled_job(func=search_for_movies, trigger='interval', days=7)
    search_for_movies()


def search_for_movies():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    movie_service = MoviesService()

    service = Service()
    service.path = os.environ["CHROME_PATH"]

    browser = webdriver.Chrome(options=options, service=service)
    browser.get("https://filmow.com/filmes-em-dvd/")

    movies = list_movies(browser, 10)

    open("routines/last_search.txt", "w").write(datetime.now().isoformat())

    for movie in movies:
        build_movie = Movie()\
            .set_name(movie["name"])\
            .set_image(movie["image_url"])\
            .set_rating(movie["rating"])\
            .set_synopsis(movie["synopsis"])\
            .set_genres(movie["genres"])\
            .set_popular(True)

        movie_service.insert_movie(build_movie)


def list_movies(browser, last_page=10):
    page = 1
    movies_list = []

    while page <= last_page:

        wait_until_load(browser)

        list_elements = browser.find_elements(By.XPATH, '//ul[@id="movies-list"]/li/span/a[1]')
        for element in list_elements:
            href = element.get_attribute("href")
            if href not in movies_list:
                movies_list.append(href)

        page += 1
        next_button = browser.find_element(By.XPATH, f'//div[contains(@class, "pagination")]//a[contains(text(),"{page}")]')
        if next_button is not None:
            browser.get(next_button.get_attribute("href"))
        else:
            break

    movies = []
    for movie_data in movies_list:
        movie_info = get_movie_info(browser, movie_data)
        if movie_info is not None:
            movies.append(movie_info)

    return movies


def wait_until_load(browser):
    print("Waiting until '{}' loads".format(browser.current_url))
    page_state = browser.execute_script('return document.readyState;')
    while page_state != 'complete':
        time.sleep(1)
        page_state = browser.execute_script('return document.readyState;')
    return


def get_movie_info(browser: webdriver.Chrome, url):
    browser.get(url)
    wait_until_load(browser)

    try:
        status = browser.find_element(By.XPATH, '//div[contains(@class, "movie-status")]')
        if status is not None and str(status.text).lower() == "em breve":
            return None
    except selenium.common.exceptions.NoSuchElementException:
        pass

    movie = {
        "name": None,
        "synopsis": None,
        "year": None,
        "rating": None,
        "image_url": None,
        "trailer_url": None,
        "genres": []
    }

    movie_title = browser.find_element(By.CLASS_NAME, "movie-title")
    movie["name"] = movie_title.find_element(By.TAG_NAME, "h1").text
    movie["year"] = movie_title.find_element(By.TAG_NAME, "small").text

    movie_description = browser.find_element(By.CLASS_NAME, "description")
    movie["synopsis"] = movie_description.find_element(By.TAG_NAME, "p").text

    try:
        movie_image = browser.find_element(By.XPATH, '//div[@id="cover-carousel"]/ul/li[1]/a/img')
        movie["image_url"] = movie_image.get_attribute("src")
    except selenium.common.exceptions.NoSuchElementException:
        pass

    try:
        movie["rating"] = float(browser.find_element(By.XPATH, '//span[@itemprop="ratingValue"]').text)
    except selenium.common.exceptions.NoSuchElementException:
        pass

    try:
        movie_genres = browser.find_elements(By.XPATH, '//a[@itemprop="genre"]')
        for genre in movie_genres:
            movie["genres"].append(genre.text)
    except selenium.common.exceptions.NoSuchElementException:
        pass

    return movie
