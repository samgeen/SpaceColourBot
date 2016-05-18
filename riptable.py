'''
Get colours for colour table
Sam Geen, May 2016
'''

import urllib, shutil
from secrets import twitter

import numpy as np
from PIL import Image

def downloadtable():
    try:
        user_timeline = twitter.get_user_timeline(screen_name='colorschemez', 
                                                  count=1)
    except TwythonError as e:
        print e

    tweet = user_timeline[0]
    tweetid = tweet["id"]
    imurl = tweet["entities"]["media"][0]["media_url_https"]
    im = urllib.urlretrieve(imurl)
    shutil.copy2(im[0],"./currtable.jpg")
    return tweetid

def run():
    tweetid = downloadtable()
    im = Image.open("currtable.jpg")
    # Resample to limit jpg errors
    arr = np.array(im)
    arr /= 5
    arr *= 5
    im = Image.fromarray(arr)
    #colours = im.convert('RGB').getcolors()
    cols = []
    nums = []
    for col in im.getcolors():
        n, c = col
        cols.append(c)
        nums.append(n)
    inds = np.argsort(nums)
    touse = inds[::-1][0:3]
    # Assign colours to RGB space
    c0 = np.array(cols[touse[0]])
    c1 = np.array(cols[touse[1]])
    c2 = np.array(cols[touse[2]])
    # Pick red and blue as the "most different" colours
    diff01 = np.sum((c0-c1)**2)
    diff12 = np.sum((c1-c2)**2)
    diff20 = np.sum((c2-c0)**2)
    maxdiff = np.max([diff01,diff12,diff20])
    if maxdiff == diff01:
        r, g, b = (c0,c2,c1)
    elif maxdiff == diff12:
        r, g, b = (c1,c0,c2)
    elif maxdiff == diff20:
        r, g, b = (c2,c1,c0)
    else:
        print "REALLY SHOULDN'T BE HERE!!! CHECK OUT riptable.py"
        r, g, b = (c0,c1,c2)
    return (r,g,b,tweetid)

if __name__=="__main__":
    print run()
