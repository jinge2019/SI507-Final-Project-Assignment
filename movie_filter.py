import json
import pprint

def readFile(file):
    with open(file, 'r') as f:
        data=f.read()
    obj = json.loads(data)
    return obj

movie = readFile('movie.txt')

# find mean value and save them in five variables for future use
popularity = []
rating = []
votes = []
domesticG = []
foreignG = []

for m in movie:
    popularity.append(m['popularity'])
    rating.append(m['imdb'][0])
    votes.append(m['imdb'][1])
    domesticG.append(m['domesticLifetimeGross'])
    foreignG.append(m['foreignLifetimeGross'])

popularity.sort()
rating.sort()
votes.sort()
domesticG.sort()
foreignG.sort()

mid = len(movie)//2

mid_popularity = popularity[mid]
mid_rating = rating[mid]
mid_votes = votes[mid]
mid_domesticG = domesticG[mid]
mid_foreignG = foreignG[mid]

# the root contains the rank number of all movies
all = [n for n in range(1,len(movie)+1)]

passB = [n for n in all if movie[n-1]['bechdel'] == 3]
failB = [n for n in all if movie[n-1]['bechdel'] != 3]

male = [n for n in passB if movie[n-1]['director'][1] == 2]
nonmale = [n for n in passB if movie[n-1]['director'][1] != 2]

after2000 = [n for n in male if int(movie[n-1]['year']) >= 2000]
before2000 = [n for n in male if int(movie[n-1]['year']) < 2000]

after2010 = [n for n in after2000 if int(movie[n-1]['year']) >= 2010]
before2010 = [n for n in after2000 if int(movie[n-1]['year']) < 2010]

highR = [n for n in failB if movie[n-1]['imdb'][0] > mid_rating]
lowR = [n for n in failB if movie[n-1]['imdb'][0] <= mid_rating]

highV = [n for n in highR if movie[n-1]['imdb'][1] > mid_votes]
lowV = [n for n in highR if movie[n-1]['imdb'][1] <= mid_votes]

highP = [n for n in highV if movie[n-1]['popularity'] > mid_popularity]
lowP = [n for n in highV if movie[n-1]['popularity'] <= mid_popularity]

highD = [n for n in lowR if movie[n-1]['domesticLifetimeGross'] > mid_domesticG]
lowD = [n for n in lowR if movie[n-1]['domesticLifetimeGross'] <= mid_domesticG]

highF = [n for n in lowD if movie[n-1]['foreignLifetimeGross'] > mid_foreignG]
lowF = [n for n in lowD if movie[n-1]['foreignLifetimeGross'] <= mid_foreignG]

higherD = [n for n in highD if movie[n-1]['foreignLifetimeGross'] > movie[n-1]['domesticLifetimeGross']]
lowerD = [n for n in highD if movie[n-1]['foreignLifetimeGross'] <= movie[n-1]['domesticLifetimeGross']]

higherF = [n for n in highF if movie[n-1]['domesticLifetimeGross'] > movie[n-1]['foreignLifetimeGross']]
lowerF = [n for n in highF if movie[n-1]['domesticLifetimeGross'] <= movie[n-1]['foreignLifetimeGross']]


# each node is a filter question
class Node:
    def __init__(self, val):
        self.question = val[0]
        self.yes = val[1]
        self.no = val[2]

# leaf nodes
note= f"This is the last question of the filter. \nHere are the satisfied movies:\n"

# construct the nodes with questions
decade = Node([["Were the movies released after 2010?", after2000], Node([[note,after2010], None, None]), Node([[note,before2010], None, None])])
popularity = Node([["Are the movies very popular?", highV], Node([[note,highP], None, None]), Node([[note,lowP], None, None])])
time = Node([["Were the movies produced in the 21th century?", male], decade, Node([[note,before2000], None, None])])
votes = Node([["Do the movies get enough votes?", highR], popularity, Node([[note,lowV], None, None])])

higherDomestic = Node([["Are the movies domestic box office revenue higher than foreign revenue?", highD], Node([[note,higherD], None, None]), Node([[note,lowerD], None, None])])
higherForeign = Node([["Are the movies foreign box office revenue higher than domestic revenue?", highF], Node([[note,higherF], None, None]), Node([[note,lowerF], None, None])])
highForeign = Node([["Are the movies' foreign box office high?", lowD], higherForeign, Node([[note,lowF], None, None])])
highDomestic = Node([["Are the movies' demostic box office high?", lowR], higherDomestic, highForeign])

director = Node([["Is the movie director male?", passB], time, Node([[note,nonmale], None, None])])
rating = Node([["Are the movies IMDB rating high?", failB], votes, highDomestic])
filter = Node([["Do the movies pass the Bechdel Test?", all], director, rating])


def isLeaf(node): 
    if node.yes == None and node.no == node.yes:
        return True
    else:
        return False

def saveList(tree):
    f = []
    if isLeaf(tree):
        f = [tree.question, tree.yes, tree.no]
    else:
        f1 = saveList(tree.yes)
        f2 = saveList(tree.no)
        f.append(tree.question)
        f.append(f1)
        f.append(f2)
    return f

tree = saveList(filter)

with open('tree.json', 'w') as f:
    json.dump(tree, f)








