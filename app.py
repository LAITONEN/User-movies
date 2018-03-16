from movie import Movie
from user import User
import json

user = None
user_choice = None
new_movie = None
response = None
welcome = 'Welcome to our app!\n'

# if a user is not logged-in - only have 3 options to sign up, log in and quit
# turn user_choice / response into readable human language form to avoid adding clarifying comments
# typing "s" anywhere should return to main menu
# movies are not being added
# we have 2 identical users and users are not being saved
# sign up should log out the current user if exists

def menu():
    global welcome, user, user_choice, new_movie
    greetings = f'Hello, {user.name}!\n' if user else ''
    while user_choice not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        try:
            user_choice = int(input(
                f'\n{greetings}'
                f'{welcome}'
                f'Please, select one of the following options by number:\n'
                f'1. Sign up.\n'
                f'2. Log in with your username.\n'
                f'3. Create a movie.\n'
                f'4. Add a movie to an existing user.\n'
                f'5. Watch a movie.\n'
                f'6. View your collection of movies\n'
                f'7. Save a user.\n'
                f'8. Log out.\n'
                f'9. Quit the app.\n'
                f'Your choice:\n'
            ))
        except ValueError:
            welcome = ''
            greetings = ''
            print('\nWrong input!')

    if user_choice == 1:
        name = input('Your username: ')
        user = User(name)

    elif user_choice == 2:
        if user:
            print(f'User {user["name"]} logged out.')
            user = None
        name = input('Your username: ')
        with open('users.txt', 'r') as f:
            json_user = list(filter(lambda user: user['name'] == name, json.load(f)))
            if len(json_user) == 0:
                print(f'\nUser {name} was not found. Please, create a new account.\n')
            if len(json_user) == 1:
                user = User.log_in_from_json(json_user[0])

    elif user_choice == 3:
        print('Enter movie information:')
        movie_data = {}
        movie_data['title'] = input('Title - ')
        movie_data['genre'] = input('Genre - ')
        movie_data['director'] = input('Director name - ')
        movie_data['year'] = input('Release year - ')
        new_movie = Movie(**movie_data).to_json()

        response = None
        while response not in ['add movie', 'don\'t add movie']:
            response = input(f'Do you want to add "{new_movie["title"]}" to your collection?\n'
                             'Enter "y" for "yes" or "n" for "no"\n')
            response = 'add movie' if response == 'y' else 'don\'t add movie' if response == 'n' else None
        if response == 'add movie' and user != None: user_choice = 4
        elif response == 'add movie' and user == None:
            response = None
            while response not in ['c', 'l', 'm', 'q']:
                response = input('You need to log in first.\n'
                                 'Type:\n'
                                 '"c" - to create a new account.\n'
                                 '"l" - to log in to an existing account.\n'
                                 '"m" - to return to menu\n'
                                 '"q" - to quit the app\n')
                if response in ['c', 'l', 'm']:
                    if response == 'c':
                        user_choice = 1
                        menu()
                    elif response == 'l':
                        user_choice = 2
                        menu()
                    else:
                        menu()

                else:
                    user_choice = 9
                    menu()


    elif user_choice == 4:
        if new_movie:
            while response not in ['y', 'n']:
                response = input(f'You have {new_movie["title"]} in your clipboard. Would you like to add it?'
                                 f'Type "y" to add {new_movie["title"]}'
                                 f'Type "n" to add another movie.')
                if response == 'y':
                    user.add_movie(new_movie)
        if not new_movie:
            all_movies = Movie.get_all_movies()
            if all_movies == None:
                print('No movies were created. Please, create a first movie.\n')
                user_choice = 3
                menu()
            response = select_movie(all_movies)

            if response != 's':
                new_movie = all_movies[response]
                user.add_movie(new_movie)
            else: new_movie = False
        if new_movie != False:
            response = None
            while response not in ['y', 'n']:
                response = input(f'Do you want to watch {new_movie["title"]} right now?\n'
                                 f'Type "y" for "yes" or "n" for "no":\n')
            if response == 'y':
                user_choice = 5
                menu()

    # Watching
    elif user_choice == 5:
        if not new_movie:
            all_movies = Movie.get_all_movies()
            print('all_movies', all_movies)
            response = select_movie(all_movies)
            new_movie = all_movies[response]
        user.watch_movie(new_movie['title'])

    elif user_choice == 6:
        user.print_all_movies()
        response = input(f'\nHit enter to proceed to the main menu.')

    elif user_choice == 7:
        user.save()
    elif user_choice == 8:
        user_choice = None
        log_out()
    elif user_choice != 9:
        user_choice = None
        welcome = ''
        menu()


def log_out():
    global user
    user = None
    menu()


def select_movie(all_movies):
    response = None
    while response not in [*range(1, len(all_movies) + 1), 's']:
        print('Select one of the following movies by number or type "s" to skip:')
        for index, movie in enumerate(all_movies):
            print(f'{index+1}. {movie["title"]}')
        response = input()
        try:
            if response != 's': response = int(response)
        except ValueError:
            print('Wrong input! Try again.')
    index = response - 1
    return index
# 1. when writing a user to users.txt, first load all the users, append a new user and then save
# 2. functionality to go back in the sequence of inputing data related to a particular object (create movie)
# 3. when a user created a movie and wants to add it to their collection, but are not logged-in =>
# => pass a callback to menu() / a new value of user_choice to actually save the movie after logging

menu()

# my_movie = Movie('Inception', 'Science fiction', 'Nolan', '2010')
# my_movie2 = Movie('The Matrix', 'Science fiction', 'Wachowski Brothers', '1999')
# my_movie3 = Movie('Fantastic Beasts', 'Science fiction', 'David Yates', '2016')
# my_movie4 = Movie('Star Wars 8', "Science Fiction", 'Not J.J. Abrams', '2017')
# my_movie5 = Movie('Star Wars 7', "Science Fiction", 'J.J. Abrams', '2015')
# user = User('Eduard')
# user2 = User('John')


# user.add_movie(my_movie)
# user.add_movie(my_movie2)
# user.add_movie(my_movie3)
# user.add_movie(my_movie4)
# user.add_movie(my_movie5)
# user.watch_movie('Inception')
# user2.add_movie(my_movie)
# user2.add_movie(my_movie4)
# user2.watch_movie('Star Wars 8')
#
#
# user.save_data()
# user.get_data()
# user.watch_movie('Star Wars')
# user.save_data()
# user.get_data()
# user3 = User.load_from_csv('file')
# user3.watch_movie('Inception')
# user3.save_data()
# user3.get_data()

# with open('file_json.txt', 'w') as f:
#     json.dump(user.to_json(), f)

# with open('file_json.txt', 'r') as f:
#     user = User.log_in_from_json(json.load(f))
#     user.print_all_movies()
#     user.add_movie(my_movie2)
#     user.watch_movie(my_movie2.title)
#     user.print_all_movies()
