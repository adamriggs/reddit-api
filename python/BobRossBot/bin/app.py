#-----------------
# ShittyWatercolorBot
# By: Adam Riggs
# v 0.1
# 5/19/2013
#-----------------


#-----------------
# imports
#-----------------

import praw
import MySQLdb
from random import randint
import time
from time import sleep
from pprint import pprint
from pgmagick import Image
from imgfx import ImgFX
import urllib2
import urllib
import json
from base64 import b64encode
import re

#-----------------
# main variables
#-----------------

user_agent='HappyLittleBot: makes it look like Bob Ross is painting the image that op posted.'
subreddit_names=[]
bob_ross_quotes=['We don\'t make mistakes, we just have happy accidents.','Any time ya learn, ya gain.','Any way you want it to be, that\'s just right.','Be sure to use odorless paint-thinner. If it\'s not odorless, you\'ll find yourself working alone very, very quick.','I like to beat the brush.','Tender as a mothers love... And with my mother, that was certainly true.','People look at me like I\'m a little strange, when I go around talking to squirrels and rabbits and stuff. That\'s ok. Thaaaat\'s just ok.','People might look at you a bit funny, but it\'s okay. Artists are allowed to be a bit different.','Shwooop. Hehe. You have to make those little noises, or it just doesn\'t work.','We tell people sometimes: we\'re like drug dealers, come into town and get everybody absolutely addicted to painting. It doesn\'t take much to get you addicted.','We want happy paintings. Happy paintings. If you want sad things, watch the news.','We\'re gonna make some big decisions in our little world.','When I was teaching my son Steve to paint, I used to tell him, just pretend he was a whisper, and he floated right across the mountain, that easy, gentle, make love to it, caress it.','You can do anything you want to do. This is your world.','Even if you\'ve never painted before, this one you can do.','And just go straight in like your going to stab it. And barely touch it...barely touch it.']
my_name="HappyLittleBot"
output_file="output.png"
has_name=False
sleep_time=1800

#-----------------
# initializations
#-----------------

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="*****", # your username
                      passwd="*****", # your password
                      db="reddit") # name of the data base
cur = db.cursor()
fx = ImgFX()
r = praw.Reddit(user_agent = user_agent)
r.login(my_name,'*****')

#-----------------
# functions
#-----------------

#//-----Database

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
    subreddit_names=['pics']

def checkMsgId(id):
    cur.execute("SELECT COUNT(1) FROM " + my_name + " WHERE msg_id = \'" + id + "\'")
    msgExists=cur.fetchone()
    if msgExists[0]:
        print "\nalready in database == true\n"
        return True
    else:
        print "\nalready in database == false\n"
        return False

def insertMsgInDb(msgType, id, subreddit, author):
    cur.execute("INSERT INTO " + my_name + " (msg_type,msg_id,subreddit,author) VALUES (\'" + str(msgType) + "\', \'" + str(id) + "\', \'" + str(subreddit) + "\', \'" + str(author) + "\')")
    db.commit()

#//-----Image

def makeWatercolor(img_name,output_name):
    print "makeWatercolor()"
    img=fx.bobross(img_name)
    img.write(output_name)

def sideLoad(filepath):
    req = urllib2.Request('https://api.imgur.com/3/image', 'image=' + urllib.quote(b64encode(open(filepath,'rb').read())))
    req.add_header('Authorization', 'Client-ID ' + '89861848efdc33c')
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    return str(response[u'data'][u'link'])

def randomComment():
    print "randomComment()"
    return bob_ross_quotes[randint(0,len(bob_ross_quotes)-1)]

def comment(url):
    output="[" + randomComment() + "](" + url + ")\n\n\n^I'm ^a ^bot!  ^This ^image ^was ^generated ^automatically."
    return output

#//-----Main Loop

def searchSubs():
    for subreddit_name in subreddit_names:
        print "number of subreddits == " + str(len(subreddit_names))
        print "\n" + subreddit_name + "\n"
        subreddit = r.get_subreddit(subreddit_name)

        for submission in subreddit.get_hot(limit=5):
            print "\n*****submission.id==" + submission.id

            
            #print str(submission.title)
            if(submission.is_self!="false"):
                msgReplied=checkMsgId(submission.id)
                print "replied: " + str(msgReplied)
                print submission.url
                if(msgReplied==False and str(submission.author)!=my_name and any(string in submission.url for string in 'imgur')):
                    urlstr=str(submission.url)
                    #print urlstr[-4:]
                    if((urlstr[-4:]=='.jpg' or urlstr[-4:]=='.png')==False):
                        urlstr=urlstr + ".jpg"
                    print "urlstr==" + urlstr
                    try:
                        makeWatercolor(urlstr,output_file)
                        #print randomComment()
                        submission.add_comment(comment(sideLoad(output_file)))
                        insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                    except praw.errors.RateLimitExceeded as e:
                        print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                        print "Sleeping..."
                        sleep(e.sleep_time)
                        submission.add_comment(comment(sideLoad(output_file)))
                        insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                    except Exception as e:
                        #insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                        print "unkown error replying (probably an album)\n"
                    
            else:
                print "self post"
            
            

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
