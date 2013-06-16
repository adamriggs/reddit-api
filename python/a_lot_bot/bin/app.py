#-----------------
# a_lot_bot
# By: Adam Riggs
# v 0.1
# 5/19/2013
#-----------------


#-----------------
# imports
#-----------------

import praw
import MySQLdb
import time
from random import randint
from time import sleep
from pprint import pprint

#-----------------
# main variables
#-----------------

user_agent='a_lot_bot: a bot that checks for the word alot and comments with: a lot, FTFY'
subreddit_names=['games','conspiracy','skyrim','hockey','cringe','mylittlepony','LadyBoners','soccer','LifeProTips','Random_Acts_Of_Amazon','cats','nba','DotA2','woahdude','MakeupAddiction','MURICA','doctorwho','starcraft','gentlemanboners','fffffffuuuuuuuuuuuu','mildlyinteresting','circlejerk','4chan','minecraft','reactiongifs','cringepics','gifs','trees','leagueoflegends','pokemon','gameofthrones','adviceanimals','askreddit','todayilearned','technology','pics','atheism','funny','wtf','aww','science','music','movies','bestof','politics','gaming','videos']
standard_comment = ">alot\n\nIt's actually two words: [a lot](http://hyperboleandahalf.blogspot.com/2010/04/alot-is-better-than-you-at-everything.html)\n\n\n[^^Statistics ^^as ^^of ^^6/11/2013](http://i.imgur.com/DF3IjuU.png)"
search_words=[' alot ']
my_name="a_lot_bot"
sleep_time=1800
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="robot", # your username
                      passwd="r0b0t!", # your password
                      db="reddit") # name of the data base
cur=db.cursor()

#-----------------
# initializations
#-----------------

r = praw.Reddit(user_agent = user_agent)
r.login('*****','*****')

#-----------------
# functions
#-----------------

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
    cur.execute("SELECT DISTINCT subreddit_name from subreddits")
    mysql_rows = cur.fetchall()
    subreddit_names = [x for x, in mysql_rows]

def checkMsgId(id):
    cur.execute("SELECT COUNT(1) FROM a_lot_bot WHERE msg_id = \'" + id + "\'")
    msgExists=cur.fetchone()
    if msgExists[0]:
        print "\nalready in database == true\n"
        return True
    else:
        print "\nalready in database == false\n"
        return False

def insertMsgInDb(msgType, id, subreddit, author):
    cur.execute("INSERT INTO a_lot_bot (msg_type,msg_id,subreddit,author) VALUES (\'" + str(msgType) + "\', \'" + str(id) + "\', \'" + str(subreddit) + "\', \'" + str(author) + "\')")

def searchSubs():
    for subreddit_name in subreddit_names:
        print "number of subreddits == " + str(len(subreddit_names))
        #subreddit_name='test'
        print "\n" + subreddit_name + "\n"
        subreddit = r.get_subreddit(subreddit_name)

        for submission in subreddit.get_hot(limit=20):
            print "*****submission.id==" + submission.id
            has_alot=False
            has_alot = any(string in submission.selftext.lower() for string in search_words)

            if(has_alot):
                msgReplied=checkMsgId(submission.id)
                print "*" + str(submission.author) + "*"
                #if(msgReplied==False and str(submission.author)!=my_name):
                    #submission.add_comment(standard_comment)
                    #insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                has_alot=False

            # I need to make this next part recursive
            sub=r.get_submission(submission_id=str(submission.id))
            print "number of comments=" + str(len(sub.comments))
            for comment in sub.comments:
                #print "comment.id==" + comment.id
                has_alot=False
                try:
                    has_alot=any(string in comment.body.lower() for string in search_words)
                except Exception as e:
                    print "couldn't get comment body"

                if(has_alot): 
                    print "\n*****\nHIT!\n*****"  
                    print "\n" + str(comment.author)
                    print str(comment)
                    msgReplied=checkMsgId(comment.id)
                    if(msgReplied==False and str(comment.author)!=my_name):
                        try:
                            comment.reply(standard_comment)
                            insertMsgInDb("comment", comment.id, comment.subreddit, comment.author)
                        except praw.errors.RateLimitExceeded as e:
                             print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                        except Exception as e:
                            insertMsgInDb("comment", comment.id, comment.subreddit, comment.author)
                            print "unkown error replying (probably banned)\n"
                    has_alot=False

        db.commit()

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
        print "\nSleeping...\n"
        sleep(sleep_time)
    except Exception as e:
        print "something went wrong in the main loop"
        print str(e)
        print "\nSleeping...\n"
        sleep(sleep_time)
