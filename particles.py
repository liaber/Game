import pygame

particles = []

class Particle:
    def __init__(self,pos,velo,surface,size=10,color=(0,0,0),fade=True):
        self.pos = pos
        self.velo = velo
        self.surface = surface
        self.size = size
        self.color = color
        self.fade = fade

    def Draw(self):
        pygame.draw.circle(self.surface, self.color, self.pos, self.size)

    def Stimulate(self,gravity,drag):
        self.velo.y-=gravity
        self.pos.y-=self.velo.y
        self.velo.x*=drag
        self.pos.x+=self.velo.x
        if self.fade:
            self.size -= 0.5

def Draw():
    for particle in particles:
        particle.Stimulate(0,0.95)
        particle.Draw()
        if particle.size < 1:
            particles.remove(particle)
