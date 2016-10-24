#!/usr/bin/env python
import engine, pygame, buttonwidget, towerengine, glengine
from pygame.locals import *
import main, data
import sounds
from engine import *
bp=engine.Controls.buttonsPressed
btn=engine.Controls.buttons

class MenuEngine(engine.Engine):
    def __init__(self, **kw):
        engine.Engine.__init__(self)
        self.isMenu=True
        self.buttonlist = []
        self.screenColor = (158,160,200)
        self.bgimage = pygame.image.load(data.load("lametitle.png"))
        self.initMenu()
        self.frames=0
        self.firstFrame=True
        self.btlistnum = 1
    def initMenu(self):
        self.origx = self.screen.get_rect().x
        self.origy = self.screen.get_rect().y
        self.doMenu()
        
        crect = self.screen.get_rect()
        """
        centcoord = (crect.centerx, crect.centery)
        
        buttonTest = buttonwidget.ButtonWidget(name="Test Button", pos=centcoord, size=50)
        buttonTest.onMouseClick = self.printBang
        self.buttonlist.append(buttonTest)
        """
        exitcoord = (crect.centerx, crect.centery + 50)
        buttonExit = buttonwidget.ButtonWidget(name="Exit Button", pos=exitcoord, size=50)
        def quitme(events):
            pygame.event.post(pygame.event.Event(QUIT))
        buttonExit.onMouseClick = quitme
        self.buttonlist.append(buttonExit)
        
        gamecoord = (crect.centerx, crect.centery)
        buttonGame = buttonwidget.ButtonWidget(name="Play Game", pos=gamecoord, size=50)
        def switchEngine(events):
            main.newEngine = 'gl'
            #main.gameEngine = glengine.GlEngine()
        buttonGame.onMouseClick = switchEngine
        self.buttonlist.append(buttonGame)
        self.buttonlist[1].highlight = True
       
    def doMenu(self):
        self.screen.fill(self.screenColor)
        self.screen.blit(self.bgimage, (0,0))
        #self.eventhandler(events)
        for button in self.buttonlist:
            button.draw(self.screen)
        #self.updateMenu()

    def printBang(self, events):
        self.screenColor = (0,0,0)
        print "Bang"
        
    def eventhandler(self, events):
        #if events == None: return
        for event in events:
            if (event.type == pygame.MOUSEMOTION):
                for button in self.buttonlist:
                    button.highlight = button.rect.collidepoint(event.pos)
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                for button in self.buttonlist:
                    button.onMouseButtonDown(event)
            elif (event.type == pygame.MOUSEBUTTONUP):
                for button in self.buttonlist:
                    button.onMouseButtonUp(event)
            elif (event.type == buttonwidget.BUTTON_WIDGET_CLICK):
                print event.button_widget
                
        cl = len(self.buttonlist)
        if bp[up]:
            self.btlistnum = (self.btlistnum + 1) % cl
            self.buttonlist[self.btlistnum].highlight = True
            self.buttonlist[(self.btlistnum-1)%cl].highlight = False
        elif bp[down]:
            self.btlistnum = (self.btlistnum - 1) % cl
            self.buttonlist[self.btlistnum].highlight = True
            self.buttonlist[(self.btlistnum+1)%cl].highlight = False
        elif bp[a]:
            #or bp[b]:
            self.buttonlist[self.btlistnum].onMouseClick(events)
        
    def startFrame(self, events):
        self.doMenu()
        
        engine.Engine.startFrame(self, events)
        self.eventhandler(events)
        self.frames+=1
        if self.frames ==20:
            self.firstFrame=False
            mixer.music.load(data.filepath('title.ogg'))
            mixer.music.set_volume(1)
            mixer.music.play()
    def doFrame(self):
        engine.Engine.doFrame(self)
    
    
class ImageEngine(engine.Engine):
    def __init__(self,img,t):
        engine.Engine.__init__(self)
        self.img=pygame.image.load(data.load(img))
        self.endTime=main.globTick+t
    def doFrame(self):
        self.screen.blit(self.img,(0,0))
        engine.Engine.doFrame(self)
        if main.globTick > self.endTime:
            main.newEngine='menu'
