from math import *
import random
from gamesettings import gameWidth
def max(a,b):
    if a>b:
        return a
    else: return b
    
def randz():
    return 2*(random.random()-.5)
def rand():
    return random.random()

def addv(a,b):
    x,y=a
    xx,yy=b
    return(x+xx,y+yy)

def subv(a,b):
    """a-b"""
    x,y=a
    xx,yy=b
    return(x-xx,y-yy)

def mulv(a,b):
    x,y=a
    return (x*b,y*b)

def mulv2(a,b):
    x1,y1=a
    x2,y2=b
    return (x1*x2,y1*y2)

def magv(a):
    x,y=a
    return hypot(x,y)

def normv(a):
    x,y=a
    m=hypot(x,y)
    return (x/m,y/m)

def distv(a,b):
    return magv(subv(a,b))
def sign(x):
    if x==0: return 0
    elif x>0: return 1
    else: return -1

def circv(a,b):
    """unit direction vector from a-b with wrapping"""
    ax,ay=a
    bx,by=b
    dx=bx-ax
    if abs(dx)<(gameWidth/2):
        return dirv(a,b)
    else:
        dx = sign(dx)*(abs(dx) - gameWidth)
        #print dx
        dy=by-ay
        mag=1/hypot(dx,dy)
        return(dx*mag,dy*mag)
    
def dirv(a,b):
    """unit direction vector from a-b"""
    xa,ya=a
    xb,yb=b
    xd=xb-xa
    yd=yb-ya
    mag=1/hypot(xd,yd)
    return(xd*mag,yd*mag)

def dirvmag(a,b):
    """unit direction vector from a-b"""
    xa,ya=a
    xb,yb=b
    xd=xb-xa
    yd=yb-ya
    mag=hypot(xd,yd)
    return (xd/mag,yd/mag),mag
