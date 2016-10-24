#!/usr/bin/env python

import gamesettings as gs

from vecops import *
from pygame import *
from engine import up,down,left,right,a,b,Controls
from OpenGL.GL import *
import OpenGL.GLU
from math import *
import math
from math import *
import data
fallRate=1.0
solidBlocks=[1]
jumpThroughBlocks=[2]
import frames

""" Base-class for both the player and the on screen enemies. """
class floorCollide:
    def __init__(self,tl,tr,ml,mr,bl,br,center,ground,left,right,ceiling):
        self.tl=tl
        self.tr=tr
        self.bl=bl
        self.br=br
        self.ml=ml
        self.mr=mr
        self.centerBottom=center
        self.groundHit=ground
        self.leftHit=left
        self.rightHit=right
        self.ceilingHit=ceiling
        
    def __repr__(self):
        return [self.tl,self.tr,self.ml,self.mr,self.bl,self.br,self.centerBottom].__repr__()
class Actor:
    def __init__(self,**kw):
        self.position=(0,0)
        #self.map=None
        self.name="Actor"
        self.collideBounds=Rect(-8,0,16,45) #bounding rectangle relative to object center.
        #basic sprite. contains a surface, and the point(in sprite surface coords) that
        #corresponds to the actor center point
        self.sprite=(None,(5,5))
        self.maxVelocity=19
        #update class with keyword args
        self.isBullet=False
        self.__dict__.update(kw)
        self.tick = 0
        self.texture=-1
        self.frame=0
        self.nframes=0
        self.playerDir=1
        self.text=None
        self.isBoss=False
        if self.__dict__.has_key('frameList'):
            self.texture,self.nframes,\
            self.texWidth,self.texHeight,\
            self.imgRect=frames.frameMap[self.frameList]
            
    def getTexCoords(self,frm):
        w=self.texWidth
        h=self.texHeight
        return ((frm*w,h),((frm+1)*w,h),((frm+1)*w,0),(frm*w,0))
    def draw(self):
        #glLoadIdentity()
        
        if self.texture != -1:
            glEnable(GL_TEXTURE_2D)
            rec=self.imgRect
            glColor4f(1,1,1,1)
            tcs=self.getTexCoords(self.frame)
            if self.playerDir ==-1:
                tcs=(tcs[1],tcs[0],tcs[3],tcs[2])
            glBindTexture(GL_TEXTURE_2D,self.texture)
            glBegin(GL_QUADS)
            glTexCoord2fv(tcs[0])
            glVertex2fv(rec.topleft)
            glTexCoord2fv(tcs[1])
            glVertex2fv(rec.topright)
            glTexCoord2fv(tcs[2])
            glVertex2fv(rec.bottomright)
            glTexCoord2fv(tcs[3])
            glVertex2fv(rec.bottomleft)
            glEnd() 
        else:
            glDisable(GL_TEXTURE_2D)
            rec=self.collideBounds
            glColor4f(1,0,0,1)
            glBegin(GL_QUADS)
            glVertex2fv(rec.topleft)
            glVertex2fv(rec.topright)
            glVertex2fv(rec.bottomright)
            glVertex2fv(rec.bottomleft)
            glEnd()
    
    def drawBounds(self,pos,surface):
        
        if not self.text:
            f = font.Font(None,15)
            self.text = f.render(self.position.__repr__()+
                                 self.__class__.__name__, False, (255,255,0))
        rec=self.collideBounds.move(pos)
        rec.height=-rec.height
        draw.rect(surface,(255,0,0),rec)
        surface.blit(self.text,pos)
        
    def think(self):
        self.tick +=1
    
    def die(self):
        self.map.destroyActor(self)
    
    def isOffScreen(self):
        return False
    
    def collide(self,other):
        print other

    def bumpPositionToFloor(self):
        x,y=self.position
        y=(1+int(y/gs.sideLen))*gs.sideLen -1
        self.position=(x,y)
    
    
    def checkBlockIntersect(self):
        newPos=self.position#addv(self.position,self.velocity)
        rectInMap=self.collideBounds.move(newPos)
        tops=[rectInMap.bottomleft,rectInMap.bottomright,rectInMap.midleft,rectInMap.midright,rectInMap.midbottom]
        bottoms=[rectInMap.topleft,rectInMap.topright,newPos]

        topHits=[self.map.getBlockAtLoc(loc) for loc in tops]
        bottomHits=[self.map.getBlockAtLoc(loc) for loc in bottoms]
        
        hitGround=False
        if self.velocity[1]<=0:  #we're moving downward 
            if bottomHits[2][0]:hitGround=True
            elif bottomHits[0][0] and not (topHits[2][0] and topHits[2][1] in solidBlocks):
                hitGround=True
            elif bottomHits[1][0] and not (topHits[3][0] and topHits[3][1] in solidBlocks):
                hitGround=True
        
        leftWall=False
        rightWall=False
        if topHits[2][1] in solidBlocks:
            leftWall=True
        elif topHits[0][1] in solidBlocks:
            leftWall=True
        if topHits[1][1] in solidBlocks:
            rightWall=True
        elif topHits[3][1] in solidBlocks:
            rightWall=True
        ceiling=False
        
        if (topHits[0][1] in solidBlocks or topHits[1][1] in solidBlocks) and topHits[4][1] in solidBlocks and self.velocity[1]>=0:
            ceiling=True
        #print hitGround
        tl,tr,ml,mr,mt=topHits
        bl,br,center=bottomHits
        return floorCollide(tl,tr,ml,mr,bl,br,center,hitGround,leftWall,rightWall,ceiling)
        
    def moveTo(self, newPosition):
        """Overwriting this function should be done very
        carefully as this implements moving in the rotating
        background in a nice way."""
        x,y=newPosition
        self.position=(x%gs.gameWidth,y)
        
    def move(self,delta):
        """Overwriting this function should be done very
        carefully as this implements moving in the rotating
        background in a nice way."""
        x,y=addv(self.position,delta)
        self.position=(x%gs.gameWidth,y)
    
    def limitVelocity(self):
        x,y=self.velocity
        if abs(x)>self.maxVelocity:
            x=sign(x)*self.maxVelocity
        if abs(y)>self.maxVelocity:
            y=sign(y)*self.maxVelocity
        self.velocity=(x,y)    
