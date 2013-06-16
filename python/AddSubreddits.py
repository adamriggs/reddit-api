#import praw
import MySQLdb

subreddits=['car','cars','autos','cartalk','usercars','projectcar','autodetailing','carporn','spotted','exoticspotted','acura','lexus','bmw','audi','mercedes_benz','cevrolet_cars','dodge','automotivetraining','honda','honda_performance','integra','carfails','carfaps','cargifs','carmusic','carpics','carpictures','carporn','carreviews','carspotting','citycars','coolcars','gearhead','gearheads','letstalkcars','mechanicadvice','mitsubishi','supercarporn','topgear','topgearamerica','usedcars']

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="*****", # your username
                      passwd="*****", # your password
                      db="reddit") # name of the data base
cur=db.cursor()

#r = praw.Reddit(user_agent = "scraping subreddits")

for subreddit in subreddits:
    #print "INSERT INTO subreddits (subreddit_name) VALUES (\'" + subreddit + "\')"
    #print "insert subreddit: " + subreddit
    cur.execute("INSERT INTO subreddits_cars (subreddit_name) VALUES (\'" + subreddit + "\')")


db.commit()
