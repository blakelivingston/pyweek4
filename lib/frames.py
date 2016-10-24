from vecops import *
from pygame import *
from engine import up,down,left,right,a,b,Controls
from OpenGL.GL import *
import OpenGL.GLU
from math import *
import math
from math import *
import data


frameMap={}
def loadAnim(frameList):
    texture=glGenTextures(1)
    frames=[image.load(data.load(f))\
        for f in frameList]
    [f.set_colorkey((255,0,255)) for f in frames]
    frames=[f.convert_alpha(display.get_surface()) for f in frames]
    
    w,h,n=frames[0].get_width(),frames[0].get_height(),len(frames)

    height=int(2**(ceil(log(h)/log(2))))
    width=int(2**(ceil(log(w*n)/log(2))))
    texWidth=float(w)/width #the portional width of a frame
    texHeight=float(h)/height#the portional height of a frame
    imgRect=frames[0].get_rect()
    imgRect.move_ip((-imgRect.width/2,0))
    glBindTexture(GL_TEXTURE_2D,texture)
    glPixelStorei( GL_PACK_ALIGNMENT  , 1 )
    glPixelStorei( GL_UNPACK_ALIGNMENT  , 1 )
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA8,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,'\x00\x00\x00\x00'*4*width*height)
    x=0
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    
    for img in frames:
        glTexSubImage2D(GL_TEXTURE_2D,0,x*w,0,w,h,GL_RGBA,GL_UNSIGNED_BYTE,image.tostring(img,'RGBA'))
        x+=1
    return texture,n,texWidth,texHeight,imgRect

def loadAnimations():
    global frameMap
    frameMap["player"]=loadAnim([
                "player0000.png",
                "player0001.png"
                ])
    frameMap["augenfnord"]=loadAnim([
                "augenfnord.png"
                ])
    frameMap["bubblebullet"]=loadAnim([
                "bullet0000.png",
                "bullet0001.png"
                ])
    frameMap["walls"]=loadAnim([
                "tile1.png",
                "block1.png",
                "block2.png"
                ])
    frameMap["nocanfnord"]=loadAnim([
                "nocanfnord0000.png",
                "nocanfnord0001.png",
                "nocanfnord0002.png"
                ])
    frameMap["nocanbullet"]=loadAnim([
                "nocanbullet0000.png",
                "nocanbullet0001.png",
                "nocanbullet0002.png",
                "nocanbullet0003.png",
                "nocanbullet0004.png",
                "nocanbullet0005.png",
                "nocanbullet0006.png",
                "nocanbullet0007.png"
                ])
    frameMap["mediumpop"]=loadAnim([
                "mediumpop0000.png",
                "mediumpop0001.png",
                "mediumpop0002.png"
                ])
    frameMap["cat"]=loadAnim([
                "cat.png"
                ])
    frameMap["health"]=loadAnim([
                "health.png"
                ])
                