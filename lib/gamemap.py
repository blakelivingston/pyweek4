import gamesettings as gs
import player, random
from math import *
import pygame, enemyactor, bulletactor
import data
class GameMap:
    """Contains the representation of the game state"""
    def __init__(self):

        self.playerActor=player.Player(position=(10,350),map=self)
        #self.playerActor=player.Player(position=(115,5410),map=self)
        self.playerBullets=[]
        self.enemyActors=[]
        #seed = abs(random.gauss(25,50))
        self.initLevel1()
        
        
        self.enemyBullets=[]
        
        self.objects=[]
        self.blockMap=""
        self.blockMapWidth=0
        self.blockMapHeight=0
        self.loadBlockMap('lev1.png')
        #list of thinking objects
        self.thinklist=[[self.playerActor],
            self.enemyActors,
            self.enemyBullets,
            self.playerBullets,
            self.objects
            ]
    def loadBlockMap(self,mapname):
        levelMapSurface=pygame.image.load(data.load(mapname))
        self.blockMapWidth=levelMapSurface.get_width()
        self.blockMapHeight=levelMapSurface.get_height()
        #self.scaledMap=pygame.transform.scale(levelMapSurface,(self.mapWidth*blockSize,self.mapHeight*blockSize))
        self.blockMap=list(pygame.image.tostring(levelMapSurface,'P',0))
        
    def thinkAll(self):
        for actlist in self.thinklist:
            for actor in actlist:
                actor.think()
    
    def getBlockAtLoc(self,position):
        """returns the block structure at a given pixel position"""
        x,y=position
        return self.getBlockAtIndex((floor(x/gs.sideLen),floor(y/gs.sideLen)))

    def hitMap(self,position):
        x,y=position
        hit,type=self.getBlockAtIndex((floor(x/gs.sideLen),floor(y/gs.sideLen)))
        return hit
    
    def getBlockAtIndex(self,index):
        """returns the block structure at a given index, in tiles"""
        x,y=index
        y=self.blockMapHeight-y
        if x< 0 or y<0:
            return (False,-1)
        if x>=self.blockMapWidth or y>=self.blockMapHeight:
            return (False,-1)
        
        val=ord(self.blockMap[int(x)+int(y)*self.blockMapWidth])
        if val == 0:
            return (False,val)
        else:
            return (True,val)
    def getBlock(self,index):
        """returns the block structure at a given index, in tiles"""
        x,y=index
        y=self.blockMapHeight-y
        if x< 0 or y<0:
            return 0
        if x>=self.blockMapWidth or y>=self.blockMapHeight:
            return 0
        
        val=ord(self.blockMap[int(x)+int(y)*self.blockMapWidth])
        return val
    
    def addEnemy(self,enemy):
        enemy.map=self
        self.enemyActors.append(enemy)
        
    def addEnemyBullet(self,bullet):
        self.enemyBullets.append(bullet)
        bullet.map=self
    
    def addObject(self,object):
        self.objects.append(object)
        object.map=self
    
    def addPlayerBullet(self,bullet):
        self.playerBullets.append(bullet)
        bullet.map=self
        
    def destroyActor(self,act):
        if act in self.playerBullets:   
            self.playerBullets.remove(act)
        elif act in self.enemyBullets:
            self.enemyBullets.remove(act)
        elif act in self.enemyActors:
            self.enemyActors.remove(act)
        elif act in self.objects:
            self.objects.remove(act)
        
    def killPlayer(self):
        pass
        
    def collide(self,a,b):
        for obj in a:
            for obj2 in b:
                if obj.collideBounds.move(obj.position).colliderect(obj2.collideBounds.move(obj2.position)):
                    #print "collid!"
                    obj.collide(obj2)
                    obj2.collide(obj)
                    
    def doCollisions(self):
        self.collide([self.playerActor],self.enemyBullets)
        self.collide([self.playerActor],self.objects)
        self.collide(self.enemyActors,self.playerBullets)
        self.collide([self.playerActor],self.enemyActors)
    def initLevel1(self):
        pygame.mixer.music.load(data.filepath('lev1.ogg'))
        pygame.mixer.music.set_volume(.4)
        pygame.mixer.music.play(-1)
        
        en = enemyactor.EnemyActor(position=(680,650),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.Boss(position=(680,5600),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.EnemyActor(position=(820,550),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(456,236),pauseTime=150,mortarSpeed=16,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley)        
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(455,1170),pauseTime=165,
                                   shootMax=5, roundPauseTime=20,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targDirPlayer)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(1020,1170),pauseTime=100, mortarSpeed=10,
                                    cannonY = 1.5,
                                    volleyFunc=enemyactor.EnemyActor.singleVolley)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(350,1455),pauseTime=180,
                                    mortarSpeed=12.5,
                                    roundPauseTime=25,
                                    volleyFunc=enemyactor.EnemyActor.groupVolley)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(50,1425),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targDirPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(580,1745),pauseTime=150,
                                   shootMax=5, roundPauseTime=35,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(790,1745),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(683,2190),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(450,2189),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(103,2058),pauseTime=200,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(53,2346),pauseTime=130,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(535,2355),pauseTime=180, mortarSpeed=15,
                                    roundPauseTime=25, cannonY = 4,
                                    volleyFunc=enemyactor.EnemyActor.groupVolley)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(717,2634),pauseTime=250,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targDirPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(600,2830),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targDirPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(325,2830),pauseTime=200,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(822,2925),pauseTime=200,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(82,3021),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(305,3180),pauseTime=170,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(245,3468),pauseTime=130,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(742,3464),pauseTime=200,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(328,3622),pauseTime=130,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(534,3911),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(536,4109),pauseTime=110,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(817,4201),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(685,4395),pauseTime=180, mortarSpeed=13,
                                    roundPauseTime=25, cannonY=2.5,
                                    volleyFunc=enemyactor.EnemyActor.groupVolley)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(880,4395),pauseTime=140, mortarSpeed=13,
                                    roundPauseTime=35, cannonY=2.5,
                                    volleyFunc=enemyactor.EnemyActor.groupVolley)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(645,4612),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(290,4739),pauseTime=90,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(422,4838),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(228,4931),pauseTime=200,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(449,5031),pauseTime=170,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(226,5128),pauseTime=160,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(390,5219),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(416,5419),pauseTime=250,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(426,5414),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.singleVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        
        en = enemyactor.CannonActor(position=(185,5420),pauseTime=100,
                                    mortarSpeed=10, cannonY=3,
                                    volleyFunc=enemyactor.EnemyActor.singleVolley)
        self.addEnemy(en)
        
        en = enemyactor.EnemyActor(position=(531,751),pauseTime=125,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.EnemyActor(position=(554,2536),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.EnemyActor(position=(475,2635),pauseTime=100,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.EnemyActor(position=(388,2730),pauseTime=150,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
        en = enemyactor.EnemyActor(position=(752,4777),pauseTime=125,
                                   shootFunc=enemyactor.EnemyActor.shoot,
                                   volleyFunc=enemyactor.EnemyActor.groupVolley,
                                   targetFunc=enemyactor.EnemyActor.targetPlayer)
        self.addEnemy(en)
