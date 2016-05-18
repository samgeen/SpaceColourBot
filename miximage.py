'''
Mixes a Hubble image with new channels from online colour table
Sam Geen, May 2016
'''

from PIL import Image

import numpy as np
import scipy.misc

import ripimage, riptable
import random

def reconstructtable(r,g,b):
    # Make jpg of colour table to debug it
    N = 100
    a = np.zeros((N,3*N,3))
    a[0:N,0:N,:] += r
    a[0:N,N+1:2*N,:] += g
    a[0:N,2*N+1:3*N,:] += b
    scipy.misc.imsave('testtable.jpg', a)

def optimumscaling(r,g,b):
    # Optimise the scaling so that r+g+b ~ (1,1,1)
    r /= np.max(r)
    g /= np.max(g)
    b /= np.max(b)
    target = np.zeros((3))+1.0
    # Loop over a few iterations of Monte Carlo sampling
    # Zoom in around best mix
    srange = 0.5
    spos = np.array([0.5,0.5,0.5])
    oldspos = spos
    for i in range(0,5):
        bestspread = 1e30 # Not good to start with
        for j in range(0,10000):
            sr,sg,sb = np.random.random(3)*srange + oldspos
            spread = sr*r + sg*g + sb*b - target
            spread = np.sum(spread*spread)
            if spread < bestspread:
                bestspread = spread
                spos = np.array([sr,sg,sb])
        srange *= 0.3
        oldspos = spos
    print "Optimal spread gives white as:", sr*r + sg*g + sb*b
    return spos

def run():
    cr, cg, cb, tweetid = riptable.run()
    # Test, set colours to just RGB
    #cr = [1,0,0]
    #cg = [0,1,0]
    #cb = [0,0,1]
    # Scale colours to same lightness
    cr = np.array(cr,dtype='float')
    cg = np.array(cg,dtype='float')
    cb = np.array(cb,dtype='float')
    reconstructtable(cr,cg,cb)
    #scaler, scaleg, scaleb = optimumscaling(cr,cg,cb)
    #scaler = 0.0
    #scaleg = 0.0
    #scaleb = 0.0
    scaler = 1.0/np.sum(cr)
    scaleg = 1.0/np.sum(cg)
    scaleb = 1.0/np.sum(cb)
    #cr *= scaler
    #cg *= scaleg
    #cb *= scaleb
    # Open NASA APOD image
    apod = ripimage.run()
    im = np.array(apod.image,dtype='float32')
    #m = np.zeros((300,400,3))+255.0
    # Save
    scipy.misc.imsave('testin.jpg', im)
    r, g, b = im[:,:,0],im[:,:,1],im[:,:,2]
    newim = im*0.0
    # R
    newim[:,:,0] += r*cr[0]
    newim[:,:,1] += r*cr[1]
    newim[:,:,2] += r*cr[2]
    # G
    newim[:,:,0] += g*cg[0]
    newim[:,:,1] += g*cg[1]
    newim[:,:,2] += g*cg[2]
    # B
    newim[:,:,0] += b*cb[0]
    newim[:,:,1] += b*cb[1]
    newim[:,:,2] += b*cb[2]
    # Scale image and output
    newim *= 1.0/newim.max()
    print newim.max(), newim.min()
    # Save
    scipy.misc.imsave('output.jpg', newim)
    return tweetid, apod

if __name__=="__main__":
    run()
