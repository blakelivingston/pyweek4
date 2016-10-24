#!/usr/bin/env python

import actor, pygame, explosionactor
from vecops import *
from actor import *
import gamemap

class BulletActor(actor.Actor):
    def __init__(self, bounds, pos, vel, **kw):
        
        self.life = 0
        self.damage = 1
        self.health = 1
        self.frameList="bubblebullet"
        self.__dict__.update(kw)
        
        self.lifeSpan=120
        actor.Actor.__init__(self,isBullet=True,
                             collideBounds=pygame.Rect(bounds),
                             position=pos,velocity=vel, **kw)
        self.imgRect=self.imgRect.move((0,-self.imgRect.height/2))
    def hitSolidBlock(self):
        bl,type=self.map.getBlockAtLoc(self.position)
        return type in actor.solidBlocks
    
    def think(self):
        self.frame=(self.tick)%(self.nframes+1)
        self.move(self.velocity)
        if self.tick > self.lifeSpan:
            self.die()
        if self.hitSolidBlock():
            self.die()
        actor.Actor.think(self)
        
    def collide(self,other):
        self.die()
        
class MortarActor(BulletActor):
    def __init__(self, bounds, pos, vel, **kw):
        self.bouncesLeft = 3
        self.fallRate = fallRate/2
        self.maxVelocity=15
        BulletActor.__init__(self, bounds, pos, vel,
                             frameList="nocanbullet",**kw)
        
    def think(self):
        hits = self.checkBlockIntersect()
        if hits.groundHit:
            self.velocity=mulv2(self.velocity, (0.75, -0.95))
            self.bouncesLeft -= 1
        else:
            self.velocity=addv(self.velocity,(0,-self.fallRate))
            self.limitVelocity()
        
        if self.bouncesLeft <= 0:
            """pop = explosionactor.ExplosionActor(self.position,collideBounds=self.collideBounds,
                                                frameList="mediumpop")
            self.map.addEnemyBullet(pop)"""
            self.die()
        BulletActor.think(self)
        
    def die(self):
        #popbounds=(0,0,16,16)
        pop = ExplosionActor((0,0,16,16), self.position, frameList="mediumpop")
        self.map.addEnemyBullet(pop)
        actor.Actor.die(self)
        
class ExplosionActor(BulletActor):
        def __init__(self, bounds, pos, **kw):
            BulletActor.__init__(self,bounds,pos,(0,0), lifeSpan=6, damage=0, **kw)

                                
        def think(self):
            BulletActor.think(self)