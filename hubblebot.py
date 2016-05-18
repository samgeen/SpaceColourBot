'''
Fox dating bot
Sam Geen, February 2016
'''

import time

from secrets import twitter

import miximage

def tweet():
    imname = ""
    itry = 0
    # Try 10 times then give up
    #tweetid, apod = miximage.run()
    while itry < 10:
        try:
            tweetid, apod = miximage.run()
            time.sleep(1)
            itry = 100 # End this loop
        except:
            itry += 1 # Try one more time
        time.sleep(1) # Slow down the retries a bit
    im = open("output.jpg")
    print tweetid
    text = apod.mytitle+" "+apod.page+\
           " (https://twitter.com/colorschemez/status/"+str(tweetid)+")"
    print "Text to post:", text
    image_ids = twitter.upload_media(media=im)
    twitter.update_status(status=text,
                          media_ids=image_ids['media_id'])

    print "Done!"

def run():
    tweet()

if __name__=="__main__":
    run()
