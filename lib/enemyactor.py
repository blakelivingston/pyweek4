#!/usr/bin/env python
import actor, bulletactor, random
from vecops import *
from actor import *
import pygame
import main
import sounds

enemyWalkVel = -2
enemyBulletSpeed = 2.5

class EnemyActor(actor.Actor):
    def __init__(self, **kw):
        self.shootMax=3
        self.pauseTime=200
        self.roundPauseTime=15
        self.bulletBounds=(0,0,8,4)
        self.volleyFunc = EnemyActor.nullShootFunc
        self.shootFunc = EnemyActor.nullShootFunc
        self.targetFunc = EnemyActor.nullTargetFunc
        self.frameList = "augenfnord"
        self.__dict__.update(kw)
        self.nextVolley=self.pauseTime
        self.nextShot=self.nextVolley
        self.vShotsLeft=self.shootMax
        self.isEnemy=True
        self.bulletOffset=(0,20)
        
        self.velocity = (enemyWalkVel,0)
        actor.Actor.__init__(self,health=5,**kw)
        
    def think(self):
        if abs(self.position[1] - self.map.playerActor.position[1])>gs.yres*.7:
            actor.Actor.think(self)
            return
        hits = self.checkBlockIntersect()
        if not hits.groundHit:
            self.velocity=addv(self.velocity,(0,-fallRate))
            falling=True
        elif self.velocity[1] < 0: #stop falling if we're moving downward but not if we're jumping up
            self.velocity=(self.velocity[0],0) #cancel falling if on ground
            falling=False
            self.bumpPositionToFloor()
        
        if hits.rightHit or hits.leftHit:
            self.velocity = mulv2(self.velocity,(-1,1))
        if hits.br[0] or hits.bl[0]:
            if not hits.br[0] or not hits.bl[0]:
                self.velocity = mulv2(self.velocity,(-1,1))
        
        self.limitVelocity()
        self.playerDir=sign(self.velocity[0])
        #print self.playerDir
        self.move(self.velocity)
        self.volleyFunc(self)
        """
        self.shootFunc=self.shoot
        self.groupVolley(self.targetPlayer())
        """
        actor.Actor.think(self)
    
    def targetPlayer(self):
        targv = addv(self.map.playerActor.position, (random.gauss(0,25),random.gauss(0,25)))
        return circv(self.position, targv)
    
    def targDirPlayer(self):
        if self.position != self.map.playerActor.position:
            playerDir = sign(circv(self.position,
                                   self.map.playerActor.position)[0])
        else:
            playerDir = 0
        return (playerDir, 0)
    
    def nullTargetFunc(self):
        pass
 
    def nullShootFunc(self):
        print "Bang!"
        #pass
    
    def nullVolleyFunc(self):
        pass

    def shoot(self, bVec):
        #self.bulletBounds
        bulVec = mulv(bVec, enemyBulletSpeed)
        bulSpawnPoint = addv(self.position, self.bulletOffset)
        bul = bulletactor.BulletActor(self.bulletBounds,bulSpawnPoint,bulVec)
        self.map.addEnemyBullet(bul)
    
    def shootTest(self, bVect):
        print bVect
        print "Bang"
   
    def collide(self,other):
        if other.isBullet:
            self.health-=other.damage
            if self.health<=0:
                self.die()
            
    def singleVolley(self):  
        if self.tick >= self.nextShot:
            self.shootFunc(self,self.targetFunc(self))
            self.nextShot = self.tick+self.pauseTime
            
    def groupVolley(self):
        if (self.tick >= self.nextVolley) and (self.vShotsLeft == 0):
            self.vShotsLeft = self.shootMax
            self.nextShot = self.nextShot
        if self.tick >= self.nextShot-6:
            self.nextFrame=self.tick+1
        if self.tick >= self.nextShot:
            if self.vShotsLeft > 0:
                self.shootFunc(self,self.targetFunc(self))
                self.vShotsLeft -= 1
                self.nextShot = self.tick+self.roundPauseTime
        else:
            self.nextVolley = self.tick+self.pauseTime
            
class CannonActor(EnemyActor):
    def __init__(self, **kw):
        #frameList = "nocanfnord"
        
        EnemyActor.__init__(self,frameList = "nocanfnord",
                            shootFunc=CannonActor.cannonShootFunc,
                            targetFunc=CannonActor.cannonTargetFunc,
                            **kw)
        self.shootMax=3
        self.pauseTime=200
        self.roundPauseTime=50
        self.mortarSpeed=15
        self.cannonY = 3
        self.__dict__.update(kw)
        self.bulletBounds = (0,0,8,8)
        self.nextFrame=0
        
    def think(self):
        if self.tick==self.nextFrame:
            if self.frame==2:
                self.frame=0
            elif self.frame==0:
                self.frame=1
                #self.nextFrame=self.tick+5
            
        if abs(self.position[1] - self.map.playerActor.position[1])>gs.yres*.7:
            actor.Actor.think(self)
            return
        hits = self.checkBlockIntersect()
        if not hits.groundHit:
            self.velocity=addv(self.velocity,(0,-fallRate))
            falling=True
            self.move(self.velocity)
        elif self.velocity[1] < 0: #stop falling if we're moving downward but not if we're jumping up
            self.velocity=(self.velocity[0],0) #cancel falling if on ground
            falling=False
            self.bumpPositionToFloor()   
        #self.move(self.velocity)
        self.volleyFunc(self)
        actor.Actor.think(self)
        
    def cannonShootFunc(self, bVec):
        #print self.tick
        #print "A cannon says bang!"
        sounds.sounds['cannon'].play()
        self.frame=2
        self.nextFrame=self.tick+5
        bulVec = mulv(bVec, self.mortarSpeed)
        bul = bulletactor.MortarActor(self.bulletBounds,self.position,bulVec)
        self.map.addEnemyBullet(bul)
    
    def cannonTargetFunc(self):
        if self.position != self.map.playerActor.position:
            vec = circv(self.position, self.map.playerActor.position)
        else:
            vec = (0,0)
        return normv((vec[0],self.cannonY))
        
chasing=0
running=1

class Boss(EnemyActor):
    def __init__(self,**kw):
        EnemyActor.__init__(self,frameList = "cat")
        self.shootMax=8
        self.pauseTime=100
        self.roundPauseTime=2
        self.mortarSpeed=15
        self.cannonY = 3
        self.health=99
        self.__dict__.update(kw)
        self.bulletBounds = (0,0,8,8)
        self.isBoss=True
        self.collideBounds=Rect(-30,30,40,400)
        self.sleeping=True
        self.mode=chasing
        self.speed=2
        self.bulletOffset=(-30,90)
    def draw(self):
        #glTranslatef(0,0,30)
        actor.Actor.draw(self)
   
    def think(self):
        if abs(self.position[1] - self.map.playerActor.position[1])>gs.yres*.7:
            actor.Actor.think(self)
            return
        if self.position[1]-self.map.playerActor.position[1]<= 30 and self.sleeping:
            self.sleeping=False
            mixer.music.load(data.filepath('boss.ogg'))
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        
        if self.sleeping:
            actor.Actor.think(self)
            self.moveTo((self.map.playerActor.position[0]+gs.gameWidth/2,self.position[1]))
            return
        if self.mode==chasing:
            playerDir=circv(self.position,self.map.playerActor.position)
            dir=sign(circv(self.position, addv(self.map.playerActor.position,(-70,0)))[0])
            self.move(mulv((dir,0),self.speed))
           # self.position=(self.position[0],8*cos(self.tick/10.0)+self.map.playerActor.position[1]+30)
            self.groupVolley()
            if self.health%20 ==0:
                self.mode=running
                self.runTime=self.tick+200
                self.health-=1
                self.spawnStuff()
        if self.mode==running:
            if self.tick>=self.runTime:
                self.mode=chasing
            playerDir=circv(self.position,self.map.playerActor.position)
            dir=sign(circv(self.position, addv(self.map.playerActor.position,(gs.gameWidth/2,0)))[0])
            self.move(mulv((dir*3,0),self.speed))
            #if self.tick % 5==0:
                
        self.position=(self.position[0],8*cos(self.tick/10.0)+self.map.playerActor.position[1]+30)
        actor.Actor.think(self)
    def die(self):
        mixer.music.load(data.filepath('victory.ogg'))
        mixer.music.set_volume(1)
        mixer.music.play()
        main.newEngine='victory'
        EnemyActor.die(self)
    def spawnStuff(self):
        en=EnemyActor(position=addv(self.position,self.bulletOffset),pauseTime=150,
                                   shootFunc=EnemyActor.shoot,
                                   volleyFunc=EnemyActor.groupVolley,
                                   targetFunc=EnemyActor.targetPlayer)
        en.velocity=(-4,15)
        self.map.addEnemy(en)
        en=EnemyActor(position=addv(self.position,self.bulletOffset),pauseTime=150,
                                   shootFunc=EnemyActor.shoot,
                                   volleyFunc=EnemyActor.groupVolley,
                                   targetFunc=EnemyActor.targetPlayer)
        en.velocity=(0,15)
        self.map.addEnemy(en)
        en=EnemyActor(position=addv(self.position,self.bulletOffset),pauseTime=150,
                                   shootFunc=EnemyActor.shoot,
                                   volleyFunc=EnemyActor.groupVolley,
                                   targetFunc=EnemyActor.targetPlayer)
        en.velocity=(4,15)
        self.map.addEnemy(en)
        
