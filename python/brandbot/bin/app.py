#-----------------
# brandbot
# By: Adam Riggs
# v 0.1
# 6/10/2013
#-----------------


#-----------------
# imports
#-----------------

import praw
import MySQLdb
import time
from praw.helpers import flatten_tree
from random import randint
from time import sleep
from pprint import pprint

#-----------------
# main variables
#-----------------

user_agent='brandbot: looking for mentions of brand names'
subreddit_names=[]
search_words=[]
brands={
    'acura':[' type-s ',' tl ',' tsx ',' rl ',' zdx ',' tsx ',' mdx ',' ilx ',' rlx ',' acura '],
    'bmw': [' bmw ',' 128i ',' 135i ',' 135is ',' 320i ',' xdrive ',' 328d ',' 328i ',' 335i ',' activehybrid ',' 335is ',' 528i ',' 535i ',' 550i ',' 640i ',' 650i ',' 740i ',' 740li ',' 750i ',' 750li ',' alpina ',' b7 ',' x1 ',' sdrive28i ',' xdrive28i ',' xdrive35i ',' x3 ',' x5 ',' xdrive35d ',' xdrive50i ',' x6 ',' z4 ',' sdrive35i ',' sdrive35is ',' m3 ',' m5 ',' m6 '],
    'mercedes-benz': [' mercedes-benz ',' mercedes ',' e class ',' cl class ', ' c class ',' cls class ',' g class ',' gl class ',' glk class ',' m class ',' s class ',' sl class ',' slk class ',' sls class '],
    'lexus': [' lexus ',' es ',' gs ',' ls ', ' is c ', ' rx ', ' gx ',' lx ',' is f ',' ct '],
    'audi': [' audi ',' a4 ',' s4 ',' a6 ',' s6 ',' a7 ',' s7 ',' a8 ',' s8 ',' a8 l ',' w12 ',' allroad ',' q5 ',' q7 '],
    'infiniti': [' infiniti ',' m37 ',' m37x ',' m ',' m56 ',' m56x '],
    'lincoln': [' lincoln ',' navigator ',' mark lt ',' mkx ',' mkz ',' mks ',' mkt ',' town car '],
    'jaguar': [' jaguar ',' xf ',' xj ',' xk ',' xfr ',' xfr-s ',' xjl ',' xjr ',' xkr ',' xkr-s ']
}
has_word=False
my_name="brandbot"
sleep_time=1800
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="*****", # your username
                      passwd="*****", # your password
                      db="reddit") # name of the data base
cur=db.cursor()

#-----------------
# initializations
#-----------------

r = praw.Reddit(user_agent = user_agent)
#r.login(my_name,'*****')

#-----------------
# functions
#-----------------

# Database Functions
def connectDB():
    global db
    global cur
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                                             user="*****", # your username
                                              passwd="*****", # your password
                                              db="reddit") # name of the data base
    cur=db.cursor()

def closeDB():
    global db
    db.close()

def getSubreddits():
    global subreddit_names
    print "getSubreddits()"
    cur.execute("SELECT DISTINCT subreddit_name from subreddits_cars")
    mysql_rows = cur.fetchall()
    subreddit_names = [x for x, in mysql_rows]
    #subreddit_names = ['bmw']

def checkMsgId(id, brand):
    cur.execute("SELECT COUNT(1) FROM " + my_name + " WHERE msg_id = \'" + id + "\' and brand = \'" + brand + "\'")
    msgExists=cur.fetchone()
    if msgExists[0]:
        print "\nalready in database == true\n"
        return True
    else:
        print "\nalready in database == false\n"
        return False

def insertMsgInDb(msgType, brand, comment):
    print comment.body
    print "\n"
    #cur.execute("INSERT INTO " + my_name + " (time_posted,msg_type,brand,msg_id,subreddit,author,body,ups,downs) VALUES (\'" + str(comment.created) + "\', \'" + str(msgType) + "\', \'" + brand + "\', \'" + str(comment.id) + "\', \'" + str(comment.subreddit) + "\', \'" + str(comment.author) + "\', \'" + str(comment.body) + "\', \'" + str(comment.ups) + "\',\'" + str(comment.downs) + "\')")
    cur.execute("INSERT INTO " + my_name + " (time_posted,msg_type,brand,msg_id,subreddit,author,body,ups,downs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(comment.created),str(msgType),brand,str(comment.id),str(comment.subreddit),str(comment.author),str(comment.body),str(comment.ups),str(comment.downs)))
    db.commit()

# search text
def find_words(comment):
    has_word=False
    for brand,search_words in brands.iteritems():
        try:
            has_word=any(string in comment.body.lower() for string in search_words)
        except Exception as e:
            print "couldn't get comment body"
        if(has_word):
            print "\n*****\nHIT!\n*****" 
            msgCollected=checkMsgId(comment.id, brand)
            if(msgCollected==False and str(comment.author)!=my_name):
                try:
                    insertMsgInDb("comment", brand, comment)
                except praw.errors.RateLimitExceeded as e:
                     print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                except Exception as e:
                    print "\nunkown error\n"
                
    #print "number of replies=" + str(len(comment.replies))
    for reply in comment.replies:
        #print type(reply)
        if(type(reply)!=praw.objects.MoreComments):
            find_words(reply)

def searchSubs():
    for subreddit_name in subreddit_names:
        print "number of subreddits == " + str(len(subreddit_names))
        #subreddit_name='test'
        print "\n" + subreddit_name + "\n"
        subreddit = r.get_subreddit(subreddit_name)

        for submission in subreddit.get_hot(limit=20):
            print "*****submission.id==" + submission.id
            submission.replace_more_comments()
            has_word = False
            has_word = any(string in submission.selftext.lower() for string in search_words)
            has_word = any(string in submission.title.lower() for string in search_words)

            if(has_word):
                msgCollected=checkMsgId(submission.id)
                print "*" + str(submission.author) + "*"
                if(msgCollected==False and str(submission.author)!=my_name):
                    print submission.title
                    print submission.selftext
                    #submission.add_comment(standard_comment)
                    insertMsgInDb("submission", submission)
                has_word=False

            # I need to make this next part recursive
            sub=r.get_submission(submission_id=str(submission.id))
            print "*****number of comments=" + str(len(sub.comments))
            for comment in sub.comments:
                if(type(comment)!=praw.objects.MoreComments):
                 find_words(comment)
                

        

#-----------------
# main loop
#-----------------

closeDB()
while True:
    try:
        connectDB()
        getSubreddits()
        searchSubs()
        closeDB()
        #pprint(brands)
        print "\nSleeping...\n"
        sleep(sleep_time)
    except Exception as e:
        print "something went wrong in the main loop"
        print str(e)
        print "\nSleeping...\n"
        sleep(sleep_time)
