#-----------------
# chatty_bot
# By: Adam Riggs
# v 0.1
# 5/27/2013
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
import eliza

#-----------------
# main variables
#-----------------
subreddit_names=[]
user_agent = 'chatty_bot: replies to a root level comment with a chatty question.  Answers all mail.'
sleep_time=3600
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="*****", # your username
                      passwd="*****", # your password
                      db="reddit") # name of the data base
cur=db.cursor()
therapist=eliza.eliza()
my_name="chatty_bot"

#-----------------
# initializations
#-----------------

r = praw.Reddit(user_agent = user_agent)
r.login('chatty_bot','ch4tty_b0t')

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
    cur.execute("SELECT DISTINCT subreddit_name from subreddits")
    mysql_rows = cur.fetchall()
    subreddit_names = [x for x, in mysql_rows]
    #print subreddit_names

def checkMsgId(id):
    global cur
    cur.execute("SELECT COUNT(1) FROM chatty_bot WHERE msg_id = \'" + id + "\'")
    msgExists=cur.fetchone()
    if msgExists[0]:
        print "\nalready in database == true\n"
        return True
    else:
        print "\nalready in database == false\n"
        return False

def insertMsgInDb(msgType, id, subreddit, author):
    cur.execute("INSERT INTO chatty_bot (msg_type,msg_id,subreddit,author) VALUES (\'" + str(msgType) + "\', \'" + str(id) + "\', \'" + str(subreddit) + "\', \'" + str(author) + "\')")

def searchSubs():
    for subreddit_name in subreddit_names:
        print "number of subreddits == " + str(len(subreddit_names))
        #subreddit_name='test'
        print "\n" + subreddit_name + "\n"
        subreddit = r.get_subreddit(subreddit_name)

        for submission in subreddit.get_hot(limit=5):
            #print "*****submission.id==" + submission.id

            sub=r.get_submission(submission_id=str(submission.id))
            #print "number of comments=" + str(len(sub.comments))
            for comment in sub.comments:
                msgReplied=checkMsgId(comment.id)
                if(msgReplied==False and str(comment.author)!=my_name):
                    try:
                        #comment.reply(standard_comment)
                        #insertMsgInDb("comment", comment.id, comment.subreddit, comment.author)
                        if(len(comment.body)<128):
                            print "comment: " + comment.body
                            print "response: " + therapist.respond(comment.body)
                            print "*****"
                    except praw.errors.RateLimitExceeded as e:
                         print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                    except Exception as e:
                         print "\n*something went wrong commenting*\n"
                    break
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
