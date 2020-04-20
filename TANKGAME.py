import pygame
from enum import Enum   

pygame.init()
screen = pygame.display.set_mode((1200, 600))
background_image=pygame.image.load('background_image.bmp')
gameover_image=pygame.image.load('gameover_image.bmp')
utu = pygame.mixer.Sound('s1.wav')
atu = pygame.mixer.Sound('s2.wav')

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self,name ,u, x, y, speed, color,lives,d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.u = u
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.lives = 3
        self.name = name
        self.KEY  = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)
        
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)
            
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)
           
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)
    

    def change_direction(self, direction):
        self.direction = direction
    def move(self):
            if self.direction == Direction.LEFT:
                if self.x + self.width < 0:
                    self.x = 1200 
                else:
                    self.x - = self.speed
            if self.direction == Direction.RIGHT:
                if self.x> 1200:
                    self.x = 0
                else:
                    self.x + = self.speed
            if self.direction == Direction.UP:
                if self.y<0-self.width:
                    self.y=600
                else:
                    self.y -= self.speed
            if self.direction == Direction.DOWN:
                if self.y > 600:
                    self.y = 0-self.width
                else:
                    self.y + = self.speed
            self.draw()
    def chances(self):
        font = pygame.font.SysFont("Calibri", 30)
        score = font.render("L I V E S: " + str(self.lives), True, (self.color))
        screen.blit(score, (1050, self.u))
    def dead(self):
            font = pygame.font.SysFont("Calibri", 30)
            text = font.render(str(self.name) + ' is looser... ', True, (0,0,0))
            screen.blit(text, (760,350))
class Bullet:
    def __init__(self,x,y,color,drop):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 1
        self.radius = 5
        self.dx, self.dy =0 ,0
        self.drop = False
    def draw(self):
        pygame.draw.circle(screen, self.color,(self.x,self.y),self.radius)
    def start(self,x,y):
        if self.drop==True:
            self.x+ =self.dx
            self.y+ =self.dy
            self.draw()
    def shoot(self,Tank):
        atu.play()
        if Tank.direction==Direction.RIGHT:
            self.x,self.y=Tank.x + int(Tank.width / 2), Tank.y + int(Tank.width / 2)
            self.dx,self.dy=15, 0
        if Tank.direction==Direction.LEFT:
            self.x,self.y=Tank.x + int(Tank.width / 2), Tank.y + int(Tank.width / 2)
            self.dx,self.dy=- 15, 0
        if Tank.direction==Direction.UP:
            self.x,self.y=Tank.x + int(Tank.width / 2), Tank.y + int(Tank.width / 2)
            self.dx,self.dy= 0, -15
        if Tank.direction==Direction.DOWN:
            self.x,self.y=Tank.x + int(Tank.width / 2), Tank.y + int(Tank.width / 2)
            self.dx,self.dy= 0, 15
    def out(self): #for bullets that are already out of walls
        if self.x >=1200 or self.x <=0 or self.y> =600 or self.y <=0:
            return True
        return False
    def colission(self,Tank):  #checking if tank bullet colission
        
        if Tank.direction==Direction.RIGHT and self.drop==True:
            if (self.x>Tank.x and self.x<Tank.x+60) and (self.y>Tank.y and self.y<Tank.y+40):
                return True
        if Tank.direction==Direction.LEFT and self.drop==True:
            if (self.x>Tank.x-20 and self.x<Tank.x+40)and (self.y>Tank.y and self.y<Tank.y+40):
                return True
        if Tank.direction==Direction.UP and self.drop==True:
            if (self.y>Tank.y-20 and self.y<Tank.y+40) and (self.x>Tank.y and self.x<Tank.x+40):
                return True
        if Tank.direction==Direction.DOWN and self.drop==True:
            if (self.y>Tank.y and self.y<Tank.y+60) and (self.x>Tank.x and self.x<Tank.x+40):
                return True 
mainloop = True
tank1 = Tank('PLAYER 1',15,300, 300, 5, (255, 0, 0),3)
tank2 = Tank('PLAYER 2',50,100, 100, 5, (0, 0, 255),3, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
bullet1=Bullet(tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2),(255, 123, 100),False)
bullet2=Bullet(tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2),(0,120,255),False)
tanks = [tank1,tank2]
bullets=[bullet1,bullet2]

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if event.key==pygame.K_RETURN:
                if bullet1.drop==False:
                    bullet1.drop=True
                    bullet1.shoot(tank1)
            if event.key==pygame.K_SPACE:
                if bullet2.drop == False:
                    bullet2.drop = True
                    bullet2.shoot (tank2)  
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])
    if bullet1.colission(tank2)==True:
        utu.play()
        tank2.lives-=1
        bullet1.drop=False
        bullet1.x, bullet1.y = tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2)
    if bullet2.colission(tank1)==True:
        utu.play()
        tank1.lives- = 1
        bullet2.drop=False
        bullet2.x, bullet2.y=tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2)
    for bullet in bullets:
        if bullet.out()==True:
            bullet.drop=False
    
                
    screen.blit(background_image, (0, 0))

    for tank in tanks:
        tank.move()
        tank.chances()
        if tank.lives==0:
            background_image=gameover_image
            tank.dead()
            tank1.speed,tank2.speed=0,0
            tank1.width,tank2.width=1,1
    bullet2.start(tank2.x + int(tank2.width / 2), tank2.y + int(tank2.width / 2))    
    bullet1.start(tank1.x + int(tank1.width / 2), tank1.y + int(tank1.width / 2))
    pygame.display.flip()

pygame.quit()