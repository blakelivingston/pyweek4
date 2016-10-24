from engine import *
from gamemap import *
from vecops import *
import gamesettings as gs
from pygame import *
import frames

blockColor={
 0:(255,255,255),
 1:(0,0,255),
 2:(128,128,128)
}

class TowerEngine(Engine):
    def __init__(self):
        gs.xres=gs.gameWidth
        frames.loadAnimations()
        self.gameMap=GameMap()
        self.scrollPos=(0,0)
        self.isMenu=False
        self.gameMap.engine=self
        Engine.__init__(self)
        self.clicklog = open('clicklog.txt','w')
        self.drawList=[[self.gameMap.playerActor], self.gameMap.enemyActors, self.gameMap.playerBullets, self.gameMap.enemyBullets]
    
    def startFrame(self,events):
        if main.currentEngine == 'tower':
            for e in events:
                if e.type == MOUSEBUTTONDOWN:
                    if e.button==1:
                        print "MapPos",self.screenToMap(e.pos)
                        #print "MapIdx",mulv(self.screenToMap(e.pos),1.0/gs.sideLen)
                        #print "PlayerPos",self.gameMap.playerActor.position
                        line = """en = enemyactor.EnemyActor(position=(%f,%f))\n
    self.addEnemy(en)\n"""%self.screenToMap(e.pos)
                        self.clicklog.write(line)
                    
        Engine.startFrame(self,events)
    def doFrame(self):
        self.screen.fill((0,0,0))
        self.gameMap.doCollisions()
        self.gameMap.thinkAll()
        self.drawMap(self.screen)
        self.scrollPos=(0,int(-self.gameMap.playerActor.position[1]/gs.sideLen)*gs.sideLen +10*gs.sideLen)
        for l in self.drawList:
            for ent in l:
                pos=self.mapToScreen(ent.position)
                ent.drawBounds(pos,self.screen)
        Engine.doFrame(self)
    
    def drawMap(self,screen):
        sl=gs.sideLen
        scx,scy=self.scrollPos
        r=Rect(0,0,sl,sl)
        for y in range(int(self.screenHeight/sl)):
            for x in range(gs.numSides):
                bExist,bType=self.gameMap.getBlockAtIndex((x-scx/gs.sideLen,y-scy/gs.sideLen -1))
                if bExist:
                    draw.rect(self.screen,blockColor[bType],r.move((x*sl,(-y*sl)+self.screenHeight)))
    
    def mapToScreen(self,mpos):
        scx,scy=self.scrollPos
        mx,my=mpos
        sx=mx 
        sy=-my+self.screenHeight - scy
        return (sx,sy)
    
    def screenToMap(self,spos):
        scx,scy=self.scrollPos
        sx,sy=spos
        mx=sx
        my=-sy+self.screenHeight-scy
        return(mx,my)