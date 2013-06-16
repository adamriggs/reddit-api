for comment in sub.comments:
    #print "comment.id==" + comment.id
    try:
        has_name=any(string in comment.body.lower() for string in search_words)
        if(has_name):
            print "comment includes name"
        else:
            print "comment does not include name"
    except Exception as e:
        print "couldn't get comment body"

    
    print "\n" + str(comment.author)
    print str(comment)
    msgReplied=checkMsgId(comment.id)
    if(msgReplied==False and str(comment.author)!=my_name):
        try:
            #comment.reply(standard_comment)
            i#nsertMsgInDb("comment", comment.id, comment.subreddit, comment.author)
        except praw.errors.RateLimitExceeded as e:
             print "Rate limited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
        except Exception as e:
            #insertMsgInDb("comment", comment.id, comment.subreddit, comment.author)
            print "unkown error replying (probably banned)\n"
    has_name=False