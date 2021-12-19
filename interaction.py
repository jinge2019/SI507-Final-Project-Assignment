import json
import pprint
from movie_filter import readFile, Node, filter

movie = readFile('movie.txt')


#########################################################################################################
# Users will filter movies after a series of questions
# all movies are from the top 200 box office movie list created in movie_filter.py
def answer(): 
    print(f"    How to play: Please answer yes or no to the question above to continue filter movies, \n    or type 'stop' to stop filtering and display all satisfied movies from the last step.")
    i = input()
    y = ['yes', 'Yes', 'YES', 'y', 'Y']
    n = ['no', 'No', 'NO', 'n', 'N']
    if i in y:
        return 'y'
    elif i in n:
        return 'n'
    elif i == 'stop':
        return 'd'
    else:
        return answer()

def isLeaf(node): 
    if node.yes == None and node.no == node.yes:
        return True
    else:
        return False

def movieList(m, ranks): 
    movieList = []
    for n in ranks:
        movieList.append(m[n-1])
    return movieList

def filterLeaf(node):
    return movieList(movie, node.question[1])

def filterMovie(node, q = []):
    print(node.question[0])
    if isLeaf(node):
        return [filterLeaf(node), q]
    else:
        a = answer()
        if a == 'y':
            q.append([node.question[0], 'Y'])
            return filterMovie(node.yes)
        elif a == 'n':
            q.append([node.question[0], 'N'])
            return filterMovie(node.no)
        elif a == 'd':
            return movieList(movie, node.question[1])


#########################################################################################################
# display filtered movie list in summary sentences or table, or sort the list by year or rating
def printQuestion(alist):
    n = 1
    for f in alist:
        print(f"{n}. {f[1]} - {f[0]}")
        n += 1

def printMovie(result):
    movies = result[0]
    question = result[1]
    if len(movies) < 1:
        print("No satisfied movie found")
    else:
        n = 1
        for m in movies:
            id = m['id']
            name = m['title']
            year = m['year']
            director = m['director'][0]
            print(f"{n}. <{name}> (IMDB ID: {id}) released in {year} directed by {director}")
            n += 1
    print(f"\nThe movies above all satisfied these requirements:")
    printQuestion(question)

def table(movies):
    array = []
    for m in movies:
        if m['bechdel'] == 3:
            bechdel = 'Pass'
        elif m['bechdel'] == 4:
            bechdel = 'No Data'
        else:
            bechdel = 'Fail'
        row = [m['title'], m['year'], m['director'][0], m['language'], str(m['imdb'][0]), str(bechdel), str(m['worldwideLifetimeGross'])]
        array.append(row)
    return array

def printTable(array):
    row_l = len(array[0])
    array = [['Name', 'Year', 'Director', 'Language', 'Rating', 'Bechdel', 'Box Office']] + array
    r = [max([len(row[n]) for row in array]) for n in range(row_l)]
    for row in array:
        row = "".join(row[n].ljust(r[n]+2) for n in range(row_l))
        print(row)

def sortByYear(array):
    rows = len(array)
    for r in range(rows-1):
        for n in range(rows-1-r):
            if int(array[n][1]) < int(array[n+1][1]):
                array[n], array[n+1] = array[n+1], array[n]
    return array

def sortByRating(array):
    rows = len(array)
    for r in range(rows-1):
        for n in range(rows-1-r):
            if float(array[n][4]) < float(array[n+1][4]):
                array[n], array[n+1] = array[n+1], array[n]
    return array
    

# movies = table(filterMovie(filter)[0])
# sortByRating(movies)
# printTable(movies)

#########################################################################################################
# In this part users will play with those movies that fail the Bechdel Test
noBechdel = [m for m in movie if m['bechdel']==4]

def printTable2(array):
    array = [['rank', 'Name', 'Bechdel Test', 'Fail Reason']] + array
    r = [max([len(row[n]) for row in array]) for n in range(4)]
    for row in array:
        row = "".join(row[n].ljust(r[n]+2) for n in range(4))
        print(row)

def printReason(movies):
    passM = []
    failM = []
    for m in movies:
        if m['bechdel'] == 0:
            failM.append([m['rank'], m['title'], "Fail", "Less than 2 women"])
        elif m['bechdel'] == 1:
            failM.append([m['rank'], m['title'], "Fail", "Women don't speak to each other"])
        elif m['bechdel'] == 2:
            failM.append([m['rank'], m['title'], "Fail", "Women only talk about men"])
        elif m['bechdel'] == 3:
            passM.append([m['rank'], m['title'], "Pass", "N/A"])
    print(f"\nHere are the movies that pass the Bechdel Test:")
    printTable2(passM)
    print(f"\nHere are the movies that fail the Bechdel Test:")
    printTable2(failM)

def printNoB(movies):
    if len(movies) < 1:
        print("No satisfied movie found")
    else:
        n = 1
        for m in movies:
            id = m['id']
            name = m['title']
            year = m['year']
            director = m['director'][0]
            print(f"{n}. <{name}> (IMDB ID: {id}) released in {year} directed by {director}")
            n += 1

def intVerification():
    print(f"\nPlease type any number between 1-8 to choose the corresponding movie in the list above")
    i = input()
    try:
        x  = int(i)
        if 0<x<9:
            return x
        else:
            return intVerification()
    except:
        return intVerification()

def yesOrNo(): 
    print(f"Please only answer yes or no")
    i = input()
    y = ['yes', 'Yes', 'YES', 'y', 'Y']
    n = ['no', 'No', 'NO', 'n', 'N']
    if i in y:
        return 'y'
    elif i in n:
        return 'n'
    else:
        return yesOrNo()

def bechdel():
    print(f"\nDoes the movie have at lease two named women in it?")
    a = yesOrNo()
    if a == 'y':
        print(f"Do the women speak to each other in the movie?")
        b = yesOrNo()
        if b == 'y':
            print(f"Do they only talk about men?")
            c = yesOrNo()
            if c == 'n':
                return 1
            else:
                return 2
        else:
            return 3
    else:
        return 0

def addBechdel():
    print(f"Which of the following movie do you know the Bechdel Test result of?\n")
    printNoB(noBechdel)
    num = intVerification()
    index = int(noBechdel[int(num)-1]['rank']) - 1
    result = bechdel()
    movie[index]['bechdel'] = result
    print(f"\n{movie[index]['title']} has been added to the list. \nHere's the new list:\n")
    printTable(table(movie))
    print(f"\n\nDo you want to add Bechdel Test result for another movie?")
    a = yesOrNo()
    if a == 'y':
        addBechdel()

    
#########################################################################################################
# put interactions together
def play():
    print(f"Part 1: Filter movies from the 200 top box office movie list")
    r = filterMovie(filter)
    movieList = r[0]
    q = r[1]

    printMovie(r)
    print(f"\nDo you want to know more details about these movies?")
    a1 = yesOrNo()
    if a1 == 'y':
        print("\n")
        printTable(table(movieList))

    print(f"\nDo you want to sort the movies by year?")
    a2 = yesOrNo()
    if a2 == 'y':
        sortByYear(table(movieList))
        printTable(table(movieList))  

    print(f"\nDo you want to sort the movies by rating?")
    a3 = yesOrNo()
    if a3 == 'y':
        sortByRating(table(movieList))
        printTable(table(movieList))
    
    print(f"\nDo you want to start over?")
    a4 = yesOrNo()
    if a4 == 'y':
        play()

def playBechdel():
    print(f"\n\n\nPart 2: Bechdel Test results of movies from the 200 top box office movie list")
    printReason(movie)
    print("\nWe found some of the movies in the top 200 box office movie list miss Bechdel Test data. They are:")
    printNoB(noBechdel)
    print(f"\nDo you want to add Bechdel Test result for one of those movies?")
    a5 = yesOrNo()
    if a5 == 'y':
        addBechdel()



play()
playBechdel()