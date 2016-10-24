from engine import *
from gamemap import *
from vecops import *
import gamesettings as gs
from gamesettings import *
from pygame import *
import towerengine
from OpenGL.GL import *
import OpenGL.GLU
from math import *
import math
import main
import frames

solidBlocks=[1]
jumpThroughBlocks=[2]

ang=2*pi/gs.gameWidth
angd=360.0/gs.gameWidth

blockColor={
 0:(1,1,1),
 1:(1,1,1),
 2:(1,1,1)
}

scrollCentering=sideLen*5
class GlEngine(towerengine.TowerEngine):
    def __init__(self,**kw):
        self.screenSize=(gs.xres,gs.yres)
        self.screenWidth= self.screenSize[0]
        self.screenHeight= self.screenSize[1]
        self.modeFlags=OPENGL|pygame.DOUBLEBUF |pygame.HWSURFACE
        
        #stupid VISTA requires this extra mode change.
        self.screen=display.set_mode((gs.xres,gs.yres),pygame.DOUBLEBUF)
        self.screen=display.set_mode((gs.xres,gs.yres),(FULLSCREEN * Engine.isFullScreen)|self.modeFlags)
        mouse.set_visible(False)
        frames.loadAnimations()
        pygame.display.set_caption("Power Hour at the Rocket Tower")
        self.modeFlags=0
        self.controls=Controls()
        self.__dict__.update(kw)
        self.gameMap=GameMap()
        self.scrollPos=(0,0)
        self.isMenu=False
        self.gameMap.engine=self
        self.drawList=[self.gameMap.playerBullets, self.gameMap.enemyBullets,[self.gameMap.playerActor], self.gameMap.enemyActors ]
        self.setupProjection()
        self.setupState()
        self.setupLights()
        self.towerRad=sideLen/(2*sin(pi/numSides))-3
    def switchFullscreen(self):
        pass
    def setupProjection(self):
        glViewport(0,0,self.screenWidth,self.screenHeight)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.screenWidth/2,self.screenWidth/2,0,self.screenHeight,-800,800)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def setupState(self):
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_CULL_FACE)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)
        #glEnable(GL_TEXTURE_2D)
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE ) ;
        glEnable ( GL_COLOR_MATERIAL ) ;
        self.texture,self.nframes,\
            self.texWidth,self.texHeight,\
            self.imgRect=frames.frameMap["walls"]
    
    def getTexCoords(self,frm):
        w=self.texWidth
        h=self.texHeight
        return ((frm*w,h),((frm+1)*w,h),((frm+1)*w,0),(frm*w,0))
    
    def setupLights(self):
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0,GL_POSITION,(400,60,500,1))
        glLightfv(GL_LIGHT0,GL_DIFFUSE,(.7,.7,.7))
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1,GL_POSITION,(-300,700,0,1))
        glLightfv(GL_LIGHT1,GL_DIFFUSE,(.6,.6,1))
        
    def doFrame(self):
        #self.screen.fill((0,0,0))
        glEnable(GL_TEXTURE_2D)
        glDepthMask(True)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        self.gameMap.doCollisions()
        self.gameMap.thinkAll()
        self.scrollPos=(self.gameMap.playerActor.position[0],self.gameMap.playerActor.position[1]-scrollCentering)
        glEnable(GL_LIGHTING)
        self.drawMap(self.screen)
        
        glDisable(GL_LIGHTING)
        glDepthMask(False)
        for l in self.drawList:
            for ent in l:
                tx,ty,tz=self.mapToScreen(ent.position)
                if ent.isBoss:
                    tx*=2
                    tz*=2
                glLoadIdentity()
                glTranslate(tx,ty,tz)
                ent.draw()
        self.drawPlayerHealth()
        glFinish()
        Engine.doFrame(self)

    def drawPlayerHealth(self):
        health=self.gameMap.playerActor.health
        texture,nframes,\
            texWidth,texHeight,\
            imgRect=frames.frameMap['health']
        w=imgRect.width
        h=imgRect.height
        glEnable(GL_TEXTURE_2D)
        glColor4f(1,1,1,1)
        glBindTexture(GL_TEXTURE_2D,texture)
        glLoadIdentity()
        glTranslatef(-300,460,750)
        for x in range(health):
            glBegin(GL_QUADS)
            glTexCoord2fv((0,0))
            glVertex2f(0,0)
            glTexCoord2fv((1,0))
            glVertex2f(w,0)
            glTexCoord2fv((1,1))
            glVertex2f(w,h)
            glTexCoord2fv((0,1))
            glVertex2f(0,h)
            glEnd()
            glTranslatef(18,0,0)
    def mapToScreen(self,pos):
        tr=self.towerRad
        x,y=pos
        sx,sy=self.scrollPos
        tx=(tr+gs.towerOffset)*sin(ang*(x-sx))
        ty=y-sy
        tz=(tr+gs.towerOffset)*cos(ang*(x-sx))
        return tx,ty,tz
    
    def drawMap(self,screen):
        sx,sy=self.scrollPos
        glMatrixMode(GL_MODELVIEW)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        glLoadIdentity()
        glTranslate(0,-(sy%sideLen),0)
        self.setupLights()
        sideAngle=360.0/numSides#
        sl2=sideLen/2.0
        glRotate(-(sx-sl2)*angd,0,1,0)
        towerRad=self.towerRad
        ang=math.radians(sideAngle/2.0)
        nx=sin(ang)
        nz=cos(ang)
        offs=int((sy)/sideLen)-1
        outBlock=towerRad+towerOffset*3
        jumpBlock=towerRad+towerOffset*.95
        type=-1
        for x in xrange(numSides):
            glMatrixMode(GL_TEXTURE)
            glLoadIdentity()
            glScalef(self.texWidth,1,1)
            glMatrixMode(GL_MODELVIEW)
            glBegin(GL_QUADS)
            for y in xrange(self.screenHeight/sideLen +3):
                ntype=self.gameMap.getBlock((x,y+offs))
                if ntype != type:
                    type=ntype
                    lt,lb,rb,rt=(type,0),(type,1),(type+1,1),(type+1,0)
                    #glMatrixMode(GL_TEXTURE)
                    #glLoadIdentity()
                    #glScalef(self.texWidth,1,1)
                    #glTranslatef(type,0,0)
                    #glColor3fv(blockColor[type])
                if type in solidBlocks :
                    glTexCoord2fv(lt)
                    glNormal(-1,0,0)
                    glVertex3f(-sl2,y*sideLen,towerRad)
                    glVertex3f(-sl2,y*sideLen-sideLen,towerRad)
                    glVertex3f(-sl2,y*sideLen-sideLen,outBlock)
                    glVertex3f(-sl2,y*sideLen,outBlock)
                    glNormal(1,0,0)
                    glVertex3f(sl2,y*sideLen,towerRad)
                    glVertex3f(sl2,y*sideLen,outBlock)
                    glVertex3f(sl2,y*sideLen-sideLen,outBlock)
                    glVertex3f(sl2,y*sideLen-sideLen,towerRad)

                    glNormal(-nx,0,nz)
                    glTexCoord2fv(lt)
                    glVertex3f(-sl2,y*sideLen,outBlock)
                    glTexCoord2fv(lb)
                    glVertex3f(-sl2,y*sideLen-sideLen,outBlock)
                    glNormal(nx,0,nz)
                    glTexCoord2fv(rb)
                    glVertex3f(sl2,y*sideLen-sideLen,outBlock)
                    glTexCoord2fv(rt)
                    glVertex3f(sl2,y*sideLen,outBlock)
                elif type in jumpThroughBlocks:
                    glTexCoord2fv(lt)
                    glNormal(-1,0,0)
                    glVertex3f(-sl2,y*sideLen,towerRad)
                    glVertex3f(-sl2,y*sideLen-sideLen,towerRad)
                    glVertex3f(-sl2,y*sideLen-sideLen,towerRad)
                    glVertex3f(-sl2,y*sideLen,jumpBlock)
                    glNormal(1,0,0)
                    glVertex3f(sl2,y*sideLen,towerRad)
                    glVertex3f(sl2,y*sideLen,jumpBlock)
                    glVertex3f(sl2,y*sideLen-sideLen,towerRad)
                    glVertex3f(sl2,y*sideLen-sideLen,towerRad)

                    glNormal(-nx,-2,nz)
                    glTexCoord2fv(lt)
                    glVertex3f(-sl2,y*sideLen,jumpBlock)
                    glTexCoord2fv(lb)
                    glVertex3f(-sl2,y*sideLen-sideLen,towerRad)
                    glNormal(nx,-2,nz)
                    glTexCoord2fv(rb)
                    glVertex3f(sl2,y*sideLen-sideLen,towerRad)
                    glTexCoord2fv(rt)
                    glVertex3f(sl2,y*sideLen,jumpBlock)
                else:
                    glNormal(-nx,0,nz)
                    glTexCoord2fv(lt)
                    glVertex3f(-sl2,y*sideLen,towerRad)
                    glTexCoord2fv(lb)
                    glVertex3f(-sl2,y*sideLen-sideLen,towerRad)
                    glNormal(nx,0,nz)
                    glTexCoord2fv(rb)
                    glVertex3f(sl2,y*sideLen-sideLen,towerRad)
                    glTexCoord2fv(rt)
                    glVertex3f(sl2,y*sideLen,towerRad)
   
            glEnd()
            
            glRotate(sideAngle,0,1,0)
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
    
