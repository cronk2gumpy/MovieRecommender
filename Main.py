import requests


def file_handler(filename):
    film_list = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                film_list.append(line)
    return film_list


def info_getter(title):
    search = "http://www.omdbapi.com/?t=" + "+".join(title.split()) + "&apikey=7d21ae56"
    response = requests.get(search).json()
    try:
        found = response.get('Response', "True")
    except AttributeError:
        found = "True"

    if found == "False":
        print("Sorry, " + title + " could not be found on the database")

    else:
        return response


def get_films_info(film_list):
    films_info = []
    for film in film_list:
        info = info_getter(film)
        if info is not None:
            films_info.append(info)

    return films_info


def display_film_info(database):
    database = sorted(database, key=lambda x: sorter(x), reverse=True)
    for film in database:
        try:
            print("")
            print("----------------")
            print(film['Title'] + ", " + film['Year'] + ", " + film['Country'])
            print("Starring: " + film['Actors'])
            print("Plot: " + film['Plot'])
            print("")
            for rating in film['Ratings']:
                print(rating["Source"] + ": " + rating['Value'])

        except KeyError:
            pass


def sorter(obj):
    imdb = float(obj.get('imdbRating', 0))
    meta = obj.get('Metascore', 0)

    if meta == "N/A":
        meta = 0
    meta = float(meta) / 10

    if imdb != 0:
        return imdb
    else:
        return meta


films = file_handler("/Users/Kieran/Desktop/Python Projects/MovieRecommender/films.txt")
film_database = get_films_info(films)
display_film_info(film_database)