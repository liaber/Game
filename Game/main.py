import pygame,sys,random
from pygame.math import Vector2

pygame.init()
WIDTH,HEIGHT = 400,225
screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
pygame.display.set_caption("Ghost")
icon = pygame.image.load("Game/player-0-0.png").convert_alpha()
pygame.display.set_icon(icon)
displaySurf = pygame.Surface((WIDTH,HEIGHT))
clock = pygame.time.Clock()

gameObjects = []
particles = []

class GameObject:
    def __init__(self,pos,size,name,velo=Vector2(0,0),color=(0,0,0)):
        self.pos = pos
        self.velo = velo
        self.size = size
        self.name = name
        self.color = color
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.size[0],self.size[1])
        gameObjects.append(self)
        if type(self.color) == str:
            self.image = pygame.image.load(f'Game/{self.color}').convert_alpha()

    def DisplayObject(self,camx,camy):
        if type(self.color) == tuple:
            self.rect = pygame.Rect(self.pos.x-int(camx),self.pos.y-int(camy),self.size[0],self.size[1])
            pygame.draw.rect(displaySurf,self.color,self.rect)
        if type(self.color) == str:
            self.rect = pygame.Rect(self.pos.x,self.pos.y,self.size[0],self.size[1])
            displaySurf.blit(self.image,(self.pos.x-int(camx),self.pos.y-int(camy)))

    def GetNewRect(self):
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.size[0],self.size[1])

    def Physics(self,friction,gravity):
        self.pos.x += self.velo.x
        self.velo.x*=friction
        self.GetNewRect()
        for gameObject in gameObjects:
            if gameObject != self:
                if self.rect.colliderect(gameObject.rect):
                    if self.velo.x>0:
                        self.pos.x = gameObject.pos.x - self.size[0]
                    elif self.velo.x<0:
                        self.pos.x = gameObject.pos.x + gameObject.size[0]
                    self.velo.x = 0

        self.pos.y -= self.velo.y
        if self.velo.y > -20:
            self.velo.y -= gravity
        self.GetNewRect()
        for gameObject in gameObjects:
            if gameObject != self:
                if self.rect.colliderect(gameObject.rect):
                    if self.velo.y>0:
                        #self.rect.top = gameObject.rect.bottom
                        self.pos.y = gameObject.pos.y+gameObject.size[1]
                        self.velo.y=0
                    if self.velo.y<0:
                        #self.rect.bottom = gameObject.rect.top
                        self.pos.y = gameObject.pos.y-self.size[1]
                        self.velo.y=0
        
    def Visible(self,camrect,camx,camy):
        return pygame.Rect(self.pos.x-camx,self.pos.y-camy,self.size[0],self.size[1]).colliderect(camrect)

class Player(GameObject):
    def __init__(self,pos,size,name,velo=Vector2(0,0),color=(0,0,0),animations=[],health=100):
        super().__init__(pos,size,name,velo,color)
        self.animations = animations
        self.currentAnimation = 0
        self.currentFrame = 0
        self.health = health

    def NewAnimation(self,frames):
        self.animations.append(frames)

    def SetAnimation(self,animation):
        self.currentAnimation = animation

    def NextAnimationFrame(self):
        self.currentFrame+=1
        if self.currentFrame >= len(self.animations[self.currentAnimation]):
            self.currentFrame = 0
        #self.color = f'Game/{self.name}-{self.currentAnimation}-{self.currentFrame}.png'
        self.color = f'Game/{self.animations[self.currentAnimation][self.currentFrame]}'
        self.image = pygame.image.load(self.color).convert_alpha()
        if self.velo.x > 0:
            self.image = pygame.transform.flip(self.image, False, False)
        if self.velo.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def IsGrounded(self):
        grounded = False
        self.pos.y += 1
        self.GetNewRect()
        for gameObject in gameObjects:
            if gameObject != self:
                if self.rect.colliderect(gameObject.rect):
                    grounded = True
        self.pos.y -= 1
        self.GetNewRect()
        return grounded

class Camera:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0,0,WIDTH,HEIGHT)

class Particle:
    def __init__(self,pos,velo,size=10,color=(0,0,0),fade=True,fadeSpeed=0.5):
        self.pos = pos
        self.velo = velo
        self.size = size
        self.color = color
        self.fade = fade
        self.fadeSpeed = fadeSpeed

    def Draw(self,camx=0,camy=0):
        pygame.draw.circle(displaySurf, self.color, (self.pos.x-camx,self.pos.y-camy), self.size)

    def Stimulate(self,gravity,drag):
        self.velo.y-=gravity
        self.pos.y-=self.velo.y
        self.velo.x*=drag
        self.pos.x+=self.velo.x
        if self.fade:
            self.size -= self.fadeSpeed

def DisplayObjects():
    for gameObject in gameObjects:
        #if gameObject.rect.colliderect(camera.rect):
        if gameObject.Visible(camera.rect,camera.x,camera.y):
            gameObject.DisplayObject(camera.x,camera.y)

def AddGameObject(pos,size,name,color=(0,0,0)):
    gameObjects.append(GameObject(pos,size,name,color=color))

def LoadMap(path):
    f = open(f'Game/{path}','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gameMap = []
    for row in data:
        gameMap.append(list(row))
    return gameMap

def CreateMap(map):
    y=0
    for row in map:
        x=0
        for tile in row:
            if tile == "1":
                AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock.png")
            elif tile == "2":
                AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-top.png")
            elif tile == "3":
                AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-corner-1.png")
            elif tile == "4":
                AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-corner-2.png")
            elif tile == "5":
              AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-corner-3.png")
            elif tile == "6":
                AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-corner-4.png")
            elif tile == "7":
              AddGameObject(Vector2(x*16,y*16),(16,16),"rock",color="rock-bottom.png")
            elif tile == "-":
                player.pos = Vector2(x*16,y*16)
            x+=1
        y+=1

def Lerp(a,b,t):
    return a + (b - a) * t

def Clamp(min,max,var):
  if var > max:
    var = max
  if var < min:
    var = min
  return var
  
frameIncrement = 0
player = Player(Vector2(400,0),(13,16),"player")
player.NewAnimation(("player-0-0.png","player-0-1.png","player-0-2.png","player-0-3.png"))
player.NewAnimation(("player-1-0.png","player-1-1.png","player-1-2.png","player-1-3.png","player-2-0.png","player-3-0.png"))
player.NewAnimation(("player-2-0.png","player-2-0.png"))
player.NewAnimation(("player-3-0.png","player-3-0.png"))


#floor = GameObject(Vector2(0,400),(800,50))
#wall = GameObject(Vector2(400,350),(50,50))

CreateMap(LoadMap("map.txt"))

camera = Camera(0,0)

while True:
    targetx = (camera.x+(player.pos.x-camera.x-(WIDTH/2)))
    targety = (camera.y+(player.pos.y-camera.y-(HEIGHT/2)))
    camera.x = Lerp(camera.x,targetx,0.8)
    camera.y = Lerp(camera.y,targety,0.8)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            particles.append(Particle(Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),Vector2(random.randint(-8,8),random.randint(-4,4))))
    
    if not player.IsGrounded():
        if abs(player.velo.x)<1:
            player.SetAnimation(2)
        if abs(player.velo.x)>1:
            player.SetAnimation(3)
    elif player.IsGrounded():
        if abs(player.velo.x)<1:
            player.SetAnimation(0)
        if abs(player.velo.x)>1:
            player.SetAnimation(1)
            #if player.velo.x > 0:
                #particles.append(Particle(Vector2(player.pos.x+8,player.pos.y+player.size[1]),Vector2(-3,random.randint(2,5)),color=(0,220,0),size=2,fadeSpeed=0.1))
            #if player.velo.x < 0:
                #particles.append(Particle(Vector2(player.pos.x+player.size[0]-8,player.pos.y+player.size[1]),Vector2(3,random.randint(2,5)),color=(0,220,0),size=2,fadeSpeed=0.1))
    
    if (frameIncrement % 5) == 0:
        player.NextAnimationFrame()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.velo.x = 4
    if keys[pygame.K_LEFT]:
        player.velo.x = -4
    if keys[pygame.K_UP]:
        if player.IsGrounded():
            player.velo.y = 8

    mx,my = pygame.mouse.get_pos()[0]/2,pygame.mouse.get_pos()[1]/2
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        pass

    player.Physics(0.65,1)

    displaySurf.fill((28, 33, 46))
    for particle in particles:
                particle.Stimulate(1,0.95)
                particle.Draw(camx=camera.x,camy=camera.y)
                if particle.size < 1:
                    particles.remove(particle)

    DisplayObjects()
    pygame.draw.rect(displaySurf,(0,200,0),pygame.Rect(10,10,player.health,30))
    player.health-=1
    player.health = Clamp(0,100,player.health)
  
    screen.blit(pygame.transform.scale2x(displaySurf),(0,0))
    pygame.display.update()
    clock.tick(30)
    frameIncrement += 1
