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

user_agent='ShittyWatercolorBot: a tribute to shitty_watercolour ...and python'
subreddit_names=[]
search_words=[' shittywatercolor ', ' shittywatercolour ', ' shittywatercolorbot ', 'shittywatercolourbot', ' shitty_watercolor ', ' shitty_watercolour ', ' shitty_watercolor_bot ', ' shitty_watercolour_bot ']
my_name="ShittyWatercolorBot"
output_file="watercolor-output.png"
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
r.login('*****','*****')

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
    cur.execute("SELECT COUNT(1) FROM ShittyWatercolorBot WHERE msg_id = \'" + id + "\'")
    msgExists=cur.fetchone()
    if msgExists[0]:
        print "\nalready in database == true\n"
        return True
    else:
        print "\nalready in database == false\n"
        return False

def insertMsgInDb(msgType, id, subreddit, author):
    cur.execute("INSERT INTO ShittyWatercolorBot (msg_type,msg_id,subreddit,author) VALUES (\'" + str(msgType) + "\', \'" + str(id) + "\', \'" + str(subreddit) + "\', \'" + str(author) + "\')")
    db.commit()

#//-----Image

def makeWatercolor(img_name,output_name):
    img=fx.watercolor(img_name)
    img.write(output_name)

def sideLoad(filepath):
    req = urllib2.Request('https://api.imgur.com/3/image', 'image=' + urllib.quote(b64encode(open(filepath,'rb').read())))
    req.add_header('Authorization', 'Client-ID ' + '89861848efdc33c')
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    return str(response[u'data'][u'link'])

def standardComment(url):
    output="[Watercolored!](" + url + ")\n\n\n^I'm ^a ^bot ^written ^in ^[python](http://www.python.org)!  ^I ^use ^[pgmagick](https://pypi.python.org/pypi/pgmagick/) ^to ^automatically ^generate ^these ^images."
    return output

#//-----Main Loop

def searchSubs():
    for subreddit_name in subreddit_names:
        print "number of subreddits == " + str(len(subreddit_names))
        print "\n" + subreddit_name + "\n"
        subreddit = r.get_subreddit(subreddit_name)

        for submission in subreddit.get_hot(limit=50):
            print "\n*****submission.id==" + submission.id

            
            #print str(submission.title)
            if(submission.is_self!="false"):
                msgReplied=checkMsgId(submission.id)
                print "replied: " + str(msgReplied)
                print submission.url
                if(msgReplied==False and str(submission.author)!=my_name and any(string in submission.url for string in 'imgur')):
                    urlstr=str(submission.url)
                    print urlstr[-4:]
                    if((urlstr[-4:]=='.jpg' or urlstr[-4:]=='.png')==False):
                        urlstr=urlstr + ".jpg"
                    print "urlstr==" + urlstr
                    try:
                        makeWatercolor(urlstr,output_file)
                        submission.add_comment(standardComment(sideLoad(output_file)))
                        insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                    except praw.errors.RateLimitExceeded as e:
                        print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                        print "Sleeping..."
                        sleep(e.sleep_time)
                        submission.add_comment(standardComment(sideLoad(output_file)))
                        insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
                    except Exception as e:
                        insertMsgInDb("submission", submission.id, submission.subreddit, submission.author)
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
