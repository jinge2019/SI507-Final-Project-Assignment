import requests
import json
import pprint


key1 = '0248bc9fb0139dc7be83695a44daed53'
key2 = 'k_pu0i1qhq'
key3 = '59f3385d'


# get all movies with available Bechdel Test result,
# put it into a list of dictionary, update the format of IMDB id. example
# {
# 'title': 'La Rosace Magique',
# 'rating': 0, 
# 'imdbid': 'tt14495706', 
# 'year': 1877, 
# 'id': 9804
# }

bechdel = 'https://bechdeltest.com/index.pl/api/v1/getAllMovies?'
response = requests.get(bechdel)
bechdel_list = response.json()
for movie in bechdel_list:
    movie['imdbid'] = 'tt' + movie['imdbid']

id_bechdel = [m['imdbid'] for m in bechdel_list] # a list of all 9331 movies with Bechdel test


# get top 200 box office movies. sample data:
# {
# 'id': 'tt4154796', 
# 'rank': '2', 
# 'title': 'Avengers: Endgame', 
# 'worldwideLifetimeGross': '$2,797,501,328', 
# 'domesticLifetimeGross': '$858,373,000', 
# 'domestic': '30.7%', 
# 'foreignLifetimeGross': '$1,939,128,328', 
# 'foreign': '69.3%', 
# 'year': '2019'
# }
url_200 = f"https://imdb-api.com/en/API/BoxOfficeAllTime/{key2}"
response_200 = requests.get(url_200)
movie_200 = response_200.json()["items"]


# turn gross/pertentage data from string into integer or float
for m in movie_200: 
    m['worldwideLifetimeGross'] = int(m['worldwideLifetimeGross'][1:].replace(',',''))
    try:
        m['domesticLifetimeGross'] = int(m['domesticLifetimeGross'][1:].replace(',',''))
    except:
        m['domesticLifetimeGross'] = 0
    try:
        m['domestic'] = float(m['domestic'][:-1])
    except:
        m['domestic'] = 0
    m['foreignLifetimeGross'] = int(m['foreignLifetimeGross'][1:].replace(',',''))
    m['foreign'] = float(m['foreign'][:-1])


# a list of all 200 movie IMDB id    
id_200 = [m['id'] for m in movie_200] 

# add Bechdel Test result to the 200 highest box office movie list
n = 0
for m in movie_200:
    if m['id'] in id_bechdel:
        i = id_bechdel.index(m['id'])
        m['bechdel'] = bechdel_list[i]['rating']
        n += 1
    else:
        m['bechdel'] = 4

print(n) #192 among the 200 movies have Bechdel test result


def getMovie(movieID):
    """
    movieID is a movie's IMDB ID string
    get movie details from TMDB. It returns the movie info
    """
    movieURL = f"https://api.themoviedb.org/3/find/{movieID}?api_key={key1}&language=en-US&external_source=imdb_id"
    movie = requests.get(movieURL).json()['movie_results'][0]
    return movie
   
def getCrew(movie):
    movieID = movie['id']
    creditsURL = f"https://api.themoviedb.org/3/movie/{movieID}/credits?api_key={key1}"
    credits = requests.get(creditsURL).json()
    crew = credits['crew']
    return crew

def getDirector(crew):
    for p in crew:
        if p['job'] == 'Director':
            director = [p['name'], p['gender'], p['id']]
    return director

# get IMDB rating info from OMDB API
def getIMDB(movieID):
    url = f"http://www.omdbapi.com/?i={movieID}&apikey={key3}"
    movie = requests.get(url).json()
    rating = float(movie['imdbRating'])
    vote = int((movie['imdbVotes']).replace(',', ''))
    imdb = [rating, vote]
    return imdb

# add director, language, popularity and IMDB rating info to the movie dictionary
for m in movie_200:
    movieID = m['id']
    movie = getMovie(movieID)
    director = getDirector(getCrew(movie))
    m['director'] = director
    m['language'] = movie['original_language']
    m['popularity'] = movie['popularity']
    m['imdb'] = getIMDB(movieID)

# write movies into a new file
with open('movie.txt', 'w') as f:
    json.dump(movie_200, f)


