def verify_uniqueness(new_movie, current_movies):
    for movie_dict in current_movies:
        if new_movie['title'] == movie_dict['title']:
            return False
    return True