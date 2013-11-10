__author__ = 'Eladio'
from pydelicious import get_popular, get_userposts,get_urlposts
import time
import random
import recommendations

def initializeUserDictionary(tag,count=5):
    user_dict={}
    #get the top count popular posts
    for p1 in get_popular(tag=tag)[0:count]:
        #find all users that posted this
        for p2 in get_urlposts(p1['url']):
            user=p2['user']
            user_dict[user]={}
    return user_dict

def fillItems(user_dict):
    all_items={}
    #Find links posted by all users
    for user in user_dict:
        for i in range(3):
            try:
                posts=get_userposts(user)
                break
            except:
                print "Failed user "+ user + ", retrying"
                time.sleep(4)
        for post in posts:
            url=post['url']
            user_dict[user][url]=1.0
            all_items[url]=1

    #Fill in missing items with 0
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item]=0.0



dictionary_users = initializeUserDictionary(tag="programming")
print fillItems(dictionary_users)
#This gives me any user at random. Dictionary.Keys gives me all the users.
user=dictionary_users.keys()[random.randint(0,len(dictionary_users)-1)]

print user

print recommendations.topMatches(dictionary_users,user,n=5,similarity=recommendations.sim_distance)
print recommendations.getRecommendations(dictionary_users,user,similarity=recommendations.sim_distance)[0:10]

