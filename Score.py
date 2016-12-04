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

# Calculates average hours for a given dictionary
def dHours(dicta):
    if(len(dicta)==0):
        return 1
    ave = 0
    num = 0
    for key, val in personal.iteritems():
        ave = ave + mean(lHours)
        num = num + 1
    return ave / num

def getNumHours(dicta):
    suma = 0
    for key, val in dicta.iteritems():
        suma = suma + val
    return suma

# Return the percentage of
def percent(personal, total):
    if(len(personal) == 0):
        return 1
    listValues = 0
    dictsum = 0
    for key, val in total.iteritems():
        dictsum = dictsum + val
    for key, val in personal.iteritems():
        listValues = listValues + mean(val)
    return listValues / dictsum

# Calculates final score using given objects
def score(numGames, percent, avHours):
    final = numGames * (10 * avHours)
    percent = 1 - percent
    if percent < 1:
        final = final / 1
    else:
        final = final / percent
    return final

# test function
def test():
    lista = {'waffles':[5,0,0], 'tacos':[10,29]}
    print getNumHours(lista)
