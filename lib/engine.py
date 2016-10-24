#!/usr/bin/env python
import sys, pygame, main
import gamesettings as gs
from pygame import *
from main import *
up      =0
down    =1
left    =2
right   =3
a       =4
b       =5

keymap={
    K_UP:up,
    K_DOWN:down,
    K_LEFT:left,
    K_RIGHT:right,
    K_LCTRL:a,
    K_LALT:b
    }
    
class Controls:
    #buttons that are down (these are globally updated in every Controls instance)
    buttons=[False]*6
    buttonsPressed=[False]*6
    
    def clearPressed(self): #clear keys that were pressed last frame
        for i in xrange(len(Controls.buttonsPressed)):
            Controls.buttonsPressed[i]=False
        
    def update(self,events):
        self.clearPressed()
        for event in events:
            setting=False
            if event.type == KEYDOWN:
                setting=True
            elif event.type == KEYUP:
                setting=False
            if event.type == KEYDOWN or event.type == KEYUP:
                button=keymap.get(event.key)
                if button != None:
                    Controls.buttons[button]=setting
                    Controls.buttonsPressed[button]=setting
            #joystick input checking here...
        #print Controls.buttonsPressed
        
class Engine:
    isFullScreen=False
    
    def __init__(self, **kw):
        pygame.init()
        
        self.screenSize=(gs.xres,gs.yres)
        self.screenWidth= self.screenSize[0]
        self.screenHeight= self.screenSize[1]
        #self.screen=pygame.display.set_mode(self.screenSize)
        self.modeFlags=0
        pygame.display.set_caption("Power Hour at the Rocket Tower")
        self.screen = pygame.display.set_mode(self.screenSize,
                        (FULLSCREEN * Engine.isFullScreen)
            |self.modeFlags,32)
        
        pygame.mouse.set_visible(True)
        self.controls=Controls()
        self.__dict__.update(kw)
        
    def switchFullscreen(self):
        print "swatchfulscrn"
        print Engine.isFullScreen
        if  Engine.isFullScreen:
            self.screen = pygame.display.set_mode(self.screenSize,self.modeFlags,32)
            Engine.isFullScreen=False
        else:
            self.screen = pygame.display.set_mode(self.screenSize,self.modeFlags |FULLSCREEN,32)
            #pygame.mouse.set_visible(False)
            Engine.isFullScreen=True
        print Engine.isFullScreen
            

    def startFrame(self,events):
        self.updateControls(events)
        
    def doFrame(self):
        pygame.display.flip()
    
    def updateControls(self, events):
        self.controls.update(events)
        #print self.controls.buttonsPressed
            
