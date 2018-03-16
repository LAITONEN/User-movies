from utils import verify_uniqueness
import json

# what i want to achieve?
# 1. I want to be able to pass ordered arguments to the Movie class and get the object created
# 2. I want to be able to pass unpacked(**) dict to the Movie class and get the object created
class Movie:
    def __init__(self, **new_movie):
        movies = []
        with open ('movies.txt', 'r') as f:
            content = f.read()
            if content != '':
                movies = json.loads(content)
        if not verify_uniqueness(new_movie, movies):
            print('\nMovie has already been added.')
            movie = [mov for mov in movies if mov['title'] == new_movie["title"]][0]
            self.title = movie['title']
            self.genre = movie['genre']
            self.director = movie['director']
            self.year = movie['year']
        else:
            self.title = new_movie['title']
            self.genre = new_movie['genre']
            self.director = new_movie['director']
            self.year = new_movie['year']
            Movie.save_json(new_movie)

    def __repr__(self):
        return self.title

    def get_info(self):
        return f'{self.genre} movie "{self.title}" was directed by {self.director} ' \
               f'and released in {self.year}.'

    def to_json(self):
        return {
            'title': self.title,
            'genre': self.genre,
            'director': self.director,
            'year': self.year
        }

    @classmethod
    def save_json(cls, new_movie):
        movies = []
        with open('movies.txt', 'r+') as f:
            content = f.read()
            if content != '':
                movies = json.loads(content)
            movies.append(new_movie)
        with open('movies.txt', 'w+') as f:
            json.dump(movies, f)
        print('Movies successfully updated.\n')

    @classmethod
    def from_json(cls, json_movie):
        movie = Movie(**json_movie['info'])
        return movie.to_json()

    @classmethod
    def get_all_movies(cls):
        with open('movies.txt', 'r') as f:
            movies = []
            content = f.read()
            if content != '':
                return json.loads(content)
            return None
