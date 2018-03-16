import json

from movie import Movie
from utils import verify_uniqueness

class User:
    def __init__(self, name):
        self.name = name
        self.movies = []
        print(f'User {self.name} was successfully initialized.\n')

    def __repr__(self):
        movies_list = [str(movie['info']['title']) for movie in self.movies]
        return f"User's name is {self.name}. "

    def add_movie(self, movie):
        print(f'\nAdding {movie["title"]} to the collection of {self.name}.')

        if not verify_uniqueness(movie, [movie['info'] for movie in self.movies]):
            return print('Movie already exists.')

        self.movies.append({ 'info': movie, 'watched': False })
        print('Movie added.\n')

    def watch_movie(self, title):
        try:
            def find_if_matched(movie):
                if movie['info']['title'].lower().startswith(title.lower()):
                    return True
                return False

            matched_movies = list(filter(lambda movie: find_if_matched(movie), self.movies))
            selected_movie = matched_movies[0]
            if len(matched_movies) > 1:
                print(f'We found more than 1 movie matching your predicate.')
                for index, movie in enumerate(matched_movies):
                    print(f'{index+1}. {movie["info"].title}')
                response = None
                while response == None or 1 > response or response > len(matched_movies):
                    try:
                        response = int(input('Please, select (by number) the one that you want to watch:\n'))
                    except ValueError:
                        print('Wrong input!')
                selected_movie = matched_movies[response-1]
            selected_movie['watched'] = True
            print(f'\n{self.name} just watched {title}.\n')
        except IndexError:
            print(f'Movie "{title}" was not found.\n')
        # make a prompt to select a movie if more than 1 are inside selected_movie

    def print_all_movies(self):
        if len(self.movies) > 0:
            print(f'\n{self.name} has the following movies in their collection:')
            for index, movie in enumerate(self.movies):
                print(f'{index+1}. {movie["info"]["title"]}, status - {"watched" if movie["watched"] else "not watched"}')
        else:
            print(f'{self.name} does not have any movies in their collection.')

    def get_watched_movies(self):
        watched_movies = list(filter(lambda movie: movie['watched'], self.movies))
        if (len(watched_movies) > 0):
            return f"{self.name} has watched: {', '.join([str(movie['info'].title) for movie in watched_movies])}."
        else:
            return f'{self.name} has not watched any movies.'

    def to_json(self):
        return {
            'name': self.name,
            'movies': [
                { 'info': movie['info'], 'watched': movie['watched'] } for movie in self.movies
            ]
        }

    @classmethod
    def log_in_from_json(cls, json_data):
        name = json_data['name']
        movies = json_data['movies']
        new_user = User(name)
        if len(movies) == 0:
            print('No movies were found')
        else:
            for movie in movies:
                new_movie = Movie.from_json(movie)
                new_user.add_movie(new_movie)
        print('Successfully logged-in.')
        return new_user

    def save(self):
        users = []
        with open('users.txt', 'r+') as f:
            content = f.read()
            if content != '':
                users = json.loads(content)
            user_exists = False
            for user in enumerate(users):
                if user['name'] == self.name:
                    user_exists = True
            users.append(self.to_json())
        with open('users.txt', 'w') as f:
            json.dump(users, f)
        print(f'User {self.name} was successfully saved.\n')
