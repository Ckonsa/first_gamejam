import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, frameCount, spriteName): 
        super(Player, self).__init__()
        self.images = []
        frameNum = 1
        for i in range(1, frameCount + 1):
            self.images.append(pygame.image.load('sprites\{name}\{name} ({x}).png'.format(x = frameNum, name = spriteName)))
            frameNum += 1
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]        

class Anim(pygame.sprite.Sprite):
    def __init__(self, x, y, frameCount, spriteName):
        super(Anim, self).__init__()
        self.images = []
        frameNum = 1
        for i in range(1, frameCount + 1):
            self.images.append(pygame.image.load('sprites\{name}\{name} ({x}).png'.format(x = frameNum, name = spriteName)))
            frameNum += 1
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                
    def draw(self, screen): 
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////^KLASSID/^FUNKTSIOONID

pygame.init()

#ekraani loomine/atribuudid
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('PARASIIT')

#mangija algatribuudid
score = 0
lives = 3
#jne

#menu teeb hiljem

running = True 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #screen.fill((255,0,0))

    pygame.display.flip()

pygame.quit()