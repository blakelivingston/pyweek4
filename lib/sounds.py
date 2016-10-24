from pygame import *
import data
sounds={}
init()
sounds['pshot']="shooting.ogg"
sounds['pdeath']="player_death.ogg"
sounds['pinjure']="playerinjured.ogg"
sounds['fs1']='footstep1.ogg'
sounds['fs2']='footstep2.ogg'
sounds['cannon']='foop.ogg'
sounds['title']='title.ogg'
for w in sounds:
    sounds[w]=mixer.Sound(data.load(sounds[w]))

