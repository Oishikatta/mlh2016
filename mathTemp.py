# Returns the average of a given list
def mean(x):
    if(len(x) == 0):
        return 1
    quot = len(x)
    suma = 0
    for i in x:
        suma = suma + i
    suma = suma / quot
    return suma

def prePercent():
    pass

# return the percentage of
def percent(personal):
    if(len(personal) == 0):
        return 1
    listValues = 0
    dictsum = 0
    for key, val in personal.iteritems():
        listValues = listValues + mean(val)
        dictsum = dictsum + 1
    return listValues / dictsum

def numGames(games):
    sum = 0
    for i in games:
        sum += 1
    return sum

def score(numGames, percent, avHours):
    final = numGames * (10 * avHours)
    percent = 1 - percent
    if percent < 1:
        final = final / 1
    else:
        final = final / percent
    return final

def test():
    lista = {'waffles':[0,0,0,0,0,0,0], 'tacos':[5,3,65,3,2,5]}
    print score(30, percent(lista), 90)

test()
