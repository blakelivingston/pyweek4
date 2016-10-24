import actor
from actor import *
from engine import *
from vecops import *
import actor
from bulletactor import BulletActor
from sounds import *
#playerWidth=128
#playerHeight=128
playerWidth=10
playerHeight=45
bp=Controls.buttonsPressed
btn=Controls.buttons
walkVel=4
maxVel=19
jumpVel=13

falling=1
onground=2
walking=3
jumping=4
bulletSpeed=8
walkFrameDelay=6
class Player(actor.Actor):
    def __init__(self,**kw):
        self.velocity=(0,0)
        self.playerDir=1
        self.health=10
        self.jumping=False
        self.state=falling
        self.invincible=False
        self.invincibleTime=0
        self.nextWalkFrameTick=0
        actor.Actor.__init__(self, frameList="player",**kw)
        self.collideBounds=Rect(-playerWidth,0,playerWidth*2,playerHeight)
    def draw(self):
        if self.invincible and (self.tick/2)%2 ==0:
            return
        actor.Actor.draw(self)
    def think(self):
        #print self.position
        hits=self.checkBlockIntersect()
        if self.state == falling:
            if hits.groundHit:
                self.state=onground
                self.velocity=mulv2(self.velocity,(1,0))
                self.bumpPositionToFloor()
            else:
                self.velocity=addv(self.velocity,(0,-fallRate))
            if self.velocity[1]>0 and hits.ceilingHit:
                self.velocity=self.velocity[0],self.velocity[1]*-.8
        
        if self.state == onground and bp[a]: #jump
            self.state=falling
            self.velocity=addv(self.velocity,(0,jumpVel))
        
        if self.state == falling or self.state == onground:
            if btn[right] and not hits.rightHit:self.velocity=(walkVel,self.velocity[1]);self.playerDir=1
            elif btn[left] and not hits.leftHit:self.velocity=(-walkVel,self.velocity[1]);self.playerDir=-1
            else: self.velocity=(0,self.velocity[1])
        if self.state == falling:
            self.frame=1
        if self.state == onground:
            if magv(self.velocity)==0:
                self.frame=0
            else:
                if self.tick>self.nextWalkFrameTick:
                    self.frame+=1
                    self.frame%=2
                    self.nextWalkFrameTick=self.tick+walkFrameDelay
            if not hits.groundHit:
                self.state=falling
            
        self.limitVelocity()
        
        self.move(self.velocity)
        if bp[b]:
            sounds['pshot'].play(0,100)
            shDir=normv((self.playerDir,btn[up] - btn[down]))
            gunPos=(6*self.playerDir,23)
            bullet=BulletActor(Rect(-2,-2,2,2),
                               addv(self.position,gunPos),
                               mulv(shDir,bulletSpeed)
                              )
            self.map.addPlayerBullet(bullet)
            
        if self.tick>=self.invincibleTime:
            self.invincible=False
        Actor.think(self)
    def collide(self,other):
        if not self.invincible:
           
            self.health-=1
            if self.health==0:
                sounds['pdeath'].play()
                mixer.music.fadeout(1000)
                main.newEngine='gameover'
            else:
                sounds['pinjure'].play()
            self.invincible=True
            self.invincibleTime=self.tick+60
    
