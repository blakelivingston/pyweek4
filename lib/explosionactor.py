#!/usr/bin/env python
import actor, pygame

class ExplosionActor(actor.Actor):
	def __init__(self, bounds, pos, **kw):
		self.frameList="mediumpop"
		self.__dict__.update(kw)
		
		actor.Actor.__init__(self,isBullet=True,
				     collideBounds=pygame.Rect(bounds),
				     position=pos,velocity=(0,0), **kw)
	
	def think(self):
		self.frame=(self.tick)%(self.nframes+1)
		