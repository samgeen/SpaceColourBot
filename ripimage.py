'''
Rip an image from the Hubble gallery
Sam Geen, May 2016
'''

import random
import urllib,urllib2, shutil
import os
from nasa import apod

def findlinks(html):
    tmp = html+""
    thumb = "http://cdn.spacetelescope.org/archives/images/thumb300y"
    # Find all links
    loc = tmp.find(thumb)
    linklocs = []
    oldloc = 0
    while loc > -1:
        linklocs.append(loc)
        loc = tmp.find(thumb,loc+1)
    # Read links and return full image versions
    links = []
    for loc in linklocs:
        link = tmp[loc:tmp.find(".jpg",loc)+4]
        link = link.replace("thumb300y","screen")
        links.append(link)
    return links
    
def runOLD():
    # Get gallery page link
    prefix = "http://www.spacetelescope.org/images/viewall/page/"
    page = str(random.randint(1,17))
    link = prefix+page+"/"
    # Open page
    opener = urllib2.urlopen(link)
    html = opener.read()
    links = findlinks(html)
    # Download an image
    link = random.choice(links)
    im = urllib.urlretrieve(link)
    shutil.copy2(im[0],"./image.jpg")

def makedate():
    # Pick a date from recent past (better images?)
    year = random.randint(2009,2015)
    month = random.randint(1,12)
    # Alas for the Jacobin calendar
    # Thanks a bunch, Greg
    maxdate = 31
    # THIRTY DAYS HATH SEPTEMBER YES I REMEMBERED THIS
    if month in [9,4,7,11]:
        maxdate = 30
    # AND THE POEM ENDS WITH "EXCEPT FEBRUARY, WHICH IS MESSED UP"
    if month == 2:
        if year % 4 == 0:
            maxdate = 29
        else:
            maxdate = 28
    day = random.randint(1,maxdate)
    # Format as "YYYY-MM-DD"
    return str(year).zfill(2)+"-"+\
        str(month).zfill(2)+"-"+\
        str(day).zfill(2)

def maketitle(apodim):
    txt = apodim.explanation
    words = txt.split(" ")
    title = ""
    iword = 0
    while iword < 3:
        word = random.choice(words)
        if len(word) > 4:
            if word[0].islower():
                title += word + " "
                iword += 1
    return title
        

def run():
    # Set up NASA API key (I know, it's dead now)
    os.environ["NASA_API_KEY"] = "K3JpH7ViIRRNcajPKb3LtMxIszuhHkL9DyhVvnuW"
    # Takes images from apod
    date = makedate()
    pagedate = date[2:4]+date[5:7]+date[8:10]
    page = "http://apod.nasa.gov/apod/ap"+pagedate+".html"
    apodim = apod.apod(date)
    apodim.page = page
    apodim.mytitle = maketitle(apodim)
    print apodim.mytitle
    return apodim

if __name__=="__main__":
    run()
