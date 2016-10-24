#!/usr/bin/env python
import pygame
from pygame.locals import *

BUTTON_WIDGET_CLICK = pygame.locals.USEREVENT + 1

class ButtonWidget:
    def __init__(self, **kw):
        self.name = "Button"
        self.color = (0,255,255)
        self.hlcolor = (255,0,0)
        self.pos = (100,100)
        self.size = 17
        self.__dict__.update(kw)

        #create label
        font = pygame.font.Font(None, self.size)
        self.normtext = font.render(self.name, True, self.color)
        self.hltext = font.render(self.name, True, self.hlcolor)
        self.rect = self.normtext.get_rect()
        (self.rect.centerx, self.rect.centery) = self.pos
        self.tracking = False
        self.highlight = False
        self.update()
                
    def update(self):
        pass
    
    def draw(self, screen):
        if self.highlight:
            screen.blit(self.hltext,self.rect)
        else:
            screen.blit(self.normtext, self.rect)
    
    def onMouseButtonDown(self, event):
        self.tracking = False
        if (self.rect.collidepoint(event.pos)):
            self.tracking =  True
            
    def onMouseButtonUp(self, event):
        #if self.tracking and (self.rect.collidepoint(event.pos)):
        if (self.rect.collidepoint(event.pos)):
            self.tracking = False
            self.onMouseClick(event)
    
    def onMouseClick(self, event):
        event_attrib = {}
        event_attrib["button"] = event.button
        event_attrib["pos"] = event.pos
        event_attrib["button_widget"] = self
        e = pygame.event.Event(BUTTON_WIDGET_CLICK, event_attrib)
        pygame.event.post(e)
"""  
def isPointInRect(p, rect):
    pass

def pRelToLine(p, line):
    (px, py) = p
    (lax, lay) = line[0]
    (lbx, lby) = line[1]
    return (py - lay) - ((lby - lay) / (lbx - lby)) * (px - lax)

point = (1,9)
linex = [(1,10),(9,50)]
print pRelToLine(point, linex)
"""