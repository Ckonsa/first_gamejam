import os
import pygame
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, frameCount, spriteName): 
        super(Player, self).__init__()
        self.images = []
        frameNum = 1
        for i in range(1, frameCount + 1):
            self.images.append(pygame.image.load('{name}\{name} ({x}).png'.format(x = frameNum, name = spriteName)))
            frameNum += 1
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animation_state(self):
        self.index += 0.005#seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        if self.index >= len(self.images):#KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
            self.index = 0
        self.image = self.images[int(self.index)]
    
    #nupuvajutamisele reageerimine ehk üles alla asi
    def player_input(self):
        keys = pygame.key.get_pressed()
        speed = 1
        if keys[pygame.K_DOWN] and self.rect.bottom <= 480:
            self.rect.y += speed
        if keys[pygame.K_UP] and self.rect.y >= -30:
            self.rect.y -= speed
   
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.animation_state()
        self.player_input()
           
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        #SIIA IF JA ELIF LAUSETE SISSE TULEVAD ERINEVAD VAENLASTE PILDID
        if type == 'xxx':
            xxx_frame1 = pygame.image.load(os.path.join("XXX1.png")).convert_alpha()
            xxx_frame2 = pygame.image.load(os.path.join("XXX2.png")).convert_alpha()
            self.frames = [xxx_frame1,xxx_frame2]
        elif type == 'xx':
            xx_frame1 = pygame.image.load(os.path.join("XX1.png")).convert_alpha()
            xx_frame2 = pygame.image.load(os.path.join("XX2.png")).convert_alpha()
            self.frames=[xx_frame1,xx_frame2]#PILTIDE LIST
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]#VÕTAB ESIALGSEKS PILDIKS ESIMESE PILDI LISTIST
        self.rect = self.image.get_rect(midbottom=(randint(0,1),randint(0,1)))#KUHU ENEMY SPAWNIB esimene on x ja teine y koordinaat
        #need koorinaadid tuleks panna suuremad, kui ekraanisuurus, sest enemy spawnib kaugemal ja liigub sealt ekraanile, mitte ei popupi järsku ekraanil
    
    def animation_state(self):
        self.animation_index += 0.1#seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        if self.animation_index >= len(self.frames):#KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 5#KUI KIIRESTI ENEMY LIIGUB EKRAANIL
        self.destroy()#KONTROLLIB, KAS VAJA HÄVITADA ENNAST
    
    def destroy(self):
        if self.rect.x <= -100:#see nr näitab mitu px ta ekraanilt väljas
            self.kill()#HÄVITAB ENNAST, KUI EKRAANILT VÄLJAS, muidu kui liiga palju siis jookseb mäng kokku

#fn, et kui mäng läbi, siis enemy_group tehakse tühjaks, muidu spawniks uues mängus keset ekraani midagi
#fn, kui mängija puudutab vaenlast, siis elu kaob ja fn sees peaks kontrollima kas elusid on piisavalt, et mäng edasi läheks

class Verelible(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type=="verelible":
            verelible_frame1 = pygame.image.load(os.path.join("verelible.png")).convert_alpha()
            verelible_frame2 = pygame.image.load(os.path.join("verelible.png")).convert_alpha()
            self.frames = [verelible_frame1,verelible_frame2]
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]#VÕTAB ESIALGSEKS PILDIKS ESIMESE PILDI LISTIST
        self.rect = self.image.get_rect(midbottom=(randint(1100,1400),randint(100,450)))#KUHU ENEMY SPAWNIB esimene on x ja teine y koordinaat
        #need koorinaadid tuleks panna suuremad, kui ekraanisuurus, sest enemy spawnib kaugemal ja liigub sealt ekraanile, mitte ei popupi järsku ekraanil
    
    def animation_state(self):
        self.animation_index += 0.1#seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        if self.animation_index >= len(self.frames):#KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 0.3#KUI KIIRESTI ENEMY LIIGUB EKRAANIL
        self.destroy()#KONTROLLIB, KAS VAJA HÄVITADA ENNAST
    
    def destroy(self):
        if self.rect.left == 0:#see nr näitab mitu px ta ekraanilt väljas
            self.kill()#HÄVITAB ENNAST, KUI EKRAANILT VÄLJAS, muidu kui liiga palju siis jookseb mäng kokku



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////^KLASSID/^FUNKTSIOONID

pygame.init()

#ekraani loomine/atribuudid
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('PARASIIT')
txt = pygame.font.Font('manaspace.regular.ttf',25)

clock = pygame.time.Clock()

#mangija algatribuudid
score = 0
lives = 3
#jne

ussike = pygame.sprite.GroupSingle()
ussike.add(Player(160, 100, 4, 'ussike'))
#vaenlane
enemy_group = pygame.sprite.Group()
enemy_timer = pygame.USEREVENT + 0
pygame.time.set_timer(enemy_timer,1000)#kui tihti enemy spawnib

#taust
background = pygame.image.load(os.path.join("aluminetaust.png")).convert()
bg_x_pos = 0
background_2 = pygame.image.load(os.path.join("taust.png")).convert()
heart = pygame.image.load('heart.png')

#verelibled
verelible_group = pygame.sprite.Group()
verelible_timer = pygame.USEREVENT + 1
pygame.time.set_timer(verelible_timer,1400)

#menu teeb hiljem

running = True 
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == verelible_timer:
            verelible_group.add(Verelible('verelible'))
            verelible_group.add(Verelible('verelible'))
#         ////Kui enemy_timeri aeg on käes, siis valib randomilt vaenlase
#         if event.type == enemy_timer:
#             enemy_group.add(Enemy(choice(['xxx','xx']))) /////siia tulevad vaenlase nimed vms
#         enemy_group.draw(screen)
#         enemy_group.update()

    start_time = pygame.time.get_ticks()

    screen.blit(background_2,(0,0))
    bg_x_muut = bg_x_pos % background.get_rect().width
    screen.blit(background,(bg_x_muut - background.get_rect().width, 461))
    if bg_x_muut < width:
        screen.blit(background, (bg_x_muut, 461))
    bg_x_pos -= 0.3
    
    if pygame.sprite.spritecollide(ussike.sprite,verelible_group, True):
        score += 100

    score += start_time*0.000001
    score_txt = str(int(score))

    while len(score_txt) != 11:
        score_txt = '0' + score_txt

    for i in range(lives):
        screen.blit(heart, (8 + i*50, 30))

    screen.blit(txt.render(score_txt, True, (0,0,0)),(5,0))
    
    ussike.draw(screen)
    ussike.update()
    verelible_group.draw(screen)
    verelible_group.update()

    pygame.display.update()

pygame.quit()
