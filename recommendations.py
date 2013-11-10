__author__ = 'Eladio'
from math import sqrt

critics={'Lisa':{'Lady':2.5,'Snakes':3.5, 'Luck':3.0, 'SuperMan':1.5, 'Dupree':2.5, 'Night':3.0},
         'Gene':{'Lady':3.5,'Snakes':4.5, 'Luck':2.0, 'SuperMan':2.5, 'Dupree':1.5},
         'Michael':{'Lady':4.5, 'Luck':3.0, 'SuperMan':5.0, 'Night':3.0},
         'Claudia':{'Snakes':1.5, 'SuperMan':3.5, 'Dupree':2.5, 'Night':3.0},
         'Mick':{'Snakes':2.0, 'Luck':3.0, 'SuperMan':2.5, 'Dupree':2.5},
         'Jack':{'Lady':2.0,'Snakes':3.0, 'Luck':3.0, 'SuperMan':0.5, 'Dupree':2.5, 'Night':1.0},
         'Toby':{'Lady':3.0,'Snakes':3.0, 'Luck':3.0, 'Night':4.0}
}

#Returns Euclidean Distance Similarity

def sim_distance(preferences, person1, person2):
    #Get the list of the shared items.
    shared_items={}
    for item in preferences[person1]:
        if item in preferences[person2]:
            shared_items[item]=1

    #if they have no ratings in common, return 0
    if(len(shared_items)==0):
        return 0
    #Gets the Euclidean Distance formula. Para cada pelicula en comun, restela y eleve a la 2
    sum_of_squares=0
    sum_of_squares=sum(pow(preferences[person1][item]-preferences[person2][item],2) for item in shared_items)
    return 1/sqrt(sum_of_squares)

#Returns Pearson Correlation index

def sim_pearson(preferences, person1, person2):
    #Get the list of mutual items. Gives 1 if they're mutual
    shared_items={}
    for item in preferences[person1]:
        if item in preferences[person2]:
            shared_items[item]=1

    n=len(shared_items)

    #if they have no ratings in common, return 0
    if(n==0):return 0

    #add up all the ratings
    sum1=sum([preferences[person1][it] for it in shared_items])
    sum2=sum([preferences[person2][it] for it in shared_items])

    #Sum up the squares.
    sum1Sq=sum([pow(preferences[person1][it],2) for it in shared_items])
    sum2Sq=sum([pow(preferences[person2][it],2) for it in shared_items])

    #Sum up the products
    pSum=sum([preferences[person1][it]*preferences[person1][it] for it in shared_items])

    #Calculate the pearson score
    num=pSum - (sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0:
        return 0
    return num/den

#Returns the best matches for person from the preferences dictionary.
#number of results and similarity function are optional parameters

def topMatches(preferences, person, n=5,similarity=sim_pearson):
    scores=[(similarity(preferences,person,other),other)
                    for other in preferences if other!=person]
    #Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

#gets recommendations for a person by using a weighted average
#of every other user's rankings

def getRecommendations(preferences,person,similarity=sim_pearson):
    totals={}
    similaritiesSum={}
    for other in preferences:
        #don't compare me to myself
        if other==person:continue
        sim=similarity(preferences,person, other)

        if sim <=0:continue
        for item in preferences[other]:
            #only score movies I haven't seen yet or I didn't score yet.
            if item not in preferences[person] or preferences[person][item]==0:
            #Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=preferences[other][item]*sim
                #Sum of similarities
                similaritiesSum.setdefault(item,0)
                similaritiesSum[item]+=sim

    rankings=[(total/similaritiesSum[item],item)for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

#Transform person:product:rating into product:person:rating
def transformPreferences(preferences):
    result={}
    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item,{})
            #FLip item and person
            result[item][person]=preferences[person][item]
    return result
