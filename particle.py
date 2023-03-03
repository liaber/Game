import pygame, sys, random
from pygame.math import Vector2

pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self,pos,velo,size=10,color=(0,0,0),fade=True):
        self.pos = pos
        self.velo = velo
        self.size = size
        self.color = color
        self.fade = fade

    def Draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def Stimulate(self,gravity,drag):
        self.velo.y-=gravity
        self.pos.y-=self.velo.y
        self.velo.x*=drag
        self.pos.x+=self.velo.x
        if self.fade:
            self.size -= 0.5

while True:
    mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
    if pygame.mouse.get_pressed()[0]:
        for i in range(10):
            particles.append(Particle(Vector2(mx,my),Vector2(random.randint(0,16)-8,random.randint(0,20)-8),color=(255,255,255)))
    if pygame.mouse.get_pressed()[2]:
        print(particles)

    screen.fill((0,0,0))
    for particle in particles:
        particle.Stimulate(1,0.95)
        particle.Draw()
        if particle.size < 1:
            particles.remove(particle)


    clock.tick(60)
    pygame.display.update()