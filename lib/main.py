#!/usr/bin/env python
'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''

import data, pygame, sys
import menuengine, towerengine, glengine
from pygame import *
from engine import *
import traceback
try:
    import psyco
    psyco.full()
except:
    pass

"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
"""
Engine.isFullScreen = False
global gameEngine
gameEngine = menuengine.MenuEngine()
#gameEngine = glengine.GlEngine()
global globTick
globTick = 0
gameTitle="Kid Bandyhoot's Crazy Adventure in Cylindrical Coordinate Space"
newEngine=None
currentEngine=None
def setEngine():
    global newEngine
    global gameEngine
    global currentEngine  
    if newEngine == "menu":
        gameEngine= menuengine.MenuEngine()
        currentEngine = "menu"
    if newEngine == "tower":
        gameEngine= towerengine.TowerEngine()
        currentEngine = "tower"
    if newEngine == "gl":
        gameEngine= glengine.GlEngine()
        currentEngine = "gl"
    if newEngine == "gameover":
        gameEngine= menuengine.ImageEngine("lose.png",120)
        currentEngine = "gameover"
    if newEngine == "victory":
        gameEngine= menuengine.ImageEngine("victory.png",120)
        currentEngine = "victory"
    newEngine=None
    
    
def main():
    running = True
    #global gameEngine
    #gameEngine = menuengine.MenuEngine()
    
    clock = pygame.time.Clock()
    
    while running:
        events=pygame.event.get()
        if len(events):
            pass
            #print events
        for ev in events:
            if ev.type == QUIT:
                running= False
                
            if ev.type==KEYDOWN:
                if ev.key == K_ESCAPE:
                    running = False
                elif ev.key == K_RETURN and (pygame.key.get_mods()&(KMOD_LALT|KMOD_RALT))!=0:

                    gameEngine.switchFullscreen()
  
        gameEngine.startFrame(events)
        gameEngine.doFrame()
        setEngine()
        clock.tick(50)
        global globTick
        globTick += 1
        if globTick % 60 ==0:
            pygame.display.set_caption(gameTitle+"  FPS:"+str(clock.get_fps()))
        #print Controls.buttonsPressed
    pygame.quit()
