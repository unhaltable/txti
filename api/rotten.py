import urllib2
import json

query_call = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=pjyn7veq6mamhczedh99cse5&q={0}&page_limit=1'
movie_call = 'http://api.rottentomatoes.com/api/public/v1.0/movies/{0}.json?apikey=pjyn7veq6mamhczedh99cse5'

def query(movie):
    f = urllib2.urlopen(query_call.format(movie.replace(' ', '+')))
    json_string = f.read()
    f.close()
    return json.loads(json_string)

def query_movie(id):
    f = urllib2.urlopen(movie_call.format(id))
    json_string = f.read()
    f.close()
    return json.loads(json_string)


def get_movie(l):
    movie_list = query(l[0])
    id = -1
    for i in range(movie_list['total']):
        if movie_list['movies'][i]['title'] == l[0]:
            id = movie_list['movies'][i]['id']

    if id == -1:
        return 'Movie not found'

    movie_data = query_movie(id)

    title = movie_data['title']
    year = movie_data['year']
    runtime = movie_data['runtime']
    rating = movie_data['mpaa_rating']
    critics_rating = movie_data['ratings']['critics_rating']
    critics_score = movie_data['ratings']['critics_score']
    audience_rating = movie_data['ratings']['audience_rating']
    audience_score = movie_data['ratings']['audience_score']

    return '{0} ({1}): {2} minutes, rated {3}. Critics rating: {4} ({5}%). Audience rating: {6} ({7}%).'.format(title, year, runtime, 
                                                                                                                rating, critics_rating, 
                                                                                                                critics_score, 
                                                                                                                audience_rating, audience_score)


if __name__ == '__main__':
    print get_movie(['Toy Story 3'])