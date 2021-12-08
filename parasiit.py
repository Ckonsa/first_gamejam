import os
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, frameCount, spriteName):
        super(Player, self).__init__()
        self.images = []
        frameNum = 1
        for i in range(1, frameCount + 1):
            self.images.append(pygame.image.load(
                '{name}\{name} ({x}).png'.format(x=frameNum, name=spriteName)))
            frameNum += 1
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animation_state(self):
        self.index += 0.005  # seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        # KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

    # nupuvajutamisele reageerimine ehk üles alla asi
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
    def __init__(self, type):
        super().__init__()
        # SIIA IF JA ELIF LAUSETE SISSE TULEVAD ERINEVAD VAENLASTE PILDID
        if type == 'xxx':
            xxx_frame1 = pygame.image.load(
                os.path.join("XXX1.png")).convert_alpha()
            xxx_frame2 = pygame.image.load(
                os.path.join("XXX2.png")).convert_alpha()
            self.frames = [xxx_frame1, xxx_frame2]
        elif type == 'xx':
            xx_frame1 = pygame.image.load(
                os.path.join("XX1.png")).convert_alpha()
            xx_frame2 = pygame.image.load(
                os.path.join("XX2.png")).convert_alpha()
            self.frames = [xx_frame1, xx_frame2]  # PILTIDE LIST

        self.animation_index = 0
        # VÕTAB ESIALGSEKS PILDIKS ESIMESE PILDI LISTIST
        self.image = self.frames[self.animation_index]
        # KUHU ENEMY SPAWNIB esimene on x ja teine y koordinaat
        self.rect = self.image.get_rect(
            midbottom=(randint(0, 1), randint(0, 1)))
        # need koorinaadid tuleks panna suuremad, kui ekraanisuurus, sest enemy spawnib kaugemal ja liigub sealt ekraanile, mitte ei popupi järsku ekraanil

    def animation_state(self):
        # seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        self.animation_index += 0.1
        # KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5  # KUI KIIRESTI ENEMY LIIGUB EKRAANIL
        self.destroy()  # KONTROLLIB, KAS VAJA HÄVITADA ENNAST

    def destroy(self):
        if self.rect.x <= -100:  # see nr näitab mitu px ta ekraanilt väljas
            self.kill()  # HÄVITAB ENNAST, KUI EKRAANILT VÄLJAS, muidu kui liiga palju siis jookseb mäng kokku

# fn, et kui mäng läbi, siis enemy_group tehakse tühjaks, muidu spawniks uues mängus keset ekraani midagi
# fn, kui mängija puudutab vaenlast, siis elu kaob ja fn sees peaks kontrollima kas elusid on piisavalt, et mäng edasi läheks


class Verelible(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "verelible":
            verelible_frame1 = pygame.image.load(
                os.path.join("verelible.png")).convert_alpha()
            verelible_frame2 = pygame.image.load(
                os.path.join("verelible.png")).convert_alpha()
            self.frames = [verelible_frame1, verelible_frame2]

        self.animation_index = 0
        # VÕTAB ESIALGSEKS PILDIKS ESIMESE PILDI LISTIST
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1400), randint(
            100, 450)))  # KUHU ENEMY SPAWNIB esimene on x ja teine y koordinaat
        # need koorinaadid tuleks panna suuremad, kui ekraanisuurus, sest enemy spawnib kaugemal ja liigub sealt ekraanile, mitte ei popupi järsku ekraanil

    def animation_state(self):
        # seda nrit saab mudida, et animation ilusam ja sujuvam oleks
        self.animation_index += 0.1
        # KUI animation_index on suurem kui piltide arv listis, siis alustab uuesti esimesest pildist listist
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 0.3  # KUI KIIRESTI ENEMY LIIGUB EKRAANIL
        self.destroy()  # KONTROLLIB, KAS VAJA HÄVITADA ENNAST

    def destroy(self):
        if self.rect.left == 0:  # see nr näitab mitu px ta ekraanilt väljas
            self.kill()  # HÄVITAB ENNAST, KUI EKRAANILT VÄLJAS, muidu kui liiga palju siis jookseb mäng kokku


def pikk_tekst(ekraan, font, x_algus, x_lopp, y_algus, tekst):
    x = x_algus
    y = y_algus
    sonad = tekst.split(' ')

    for sona in sonad:
        sona_r = font.render(sona, True, (255, 255, 255))
        if sona_r.get_width() + x <= x_lopp:
            ekraan.blit(sona_r, (x, y))
            x += sona_r.get_width() + 4
        else:
            y += sona_r.get_height() + 6
            x = x_algus
            ekraan.blit(sona_r, (x, y))
            x += sona_r.get_width() + 2


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////^KLASSID/^FUNKTSIOONID

pygame.init()

# ekraani loomine/atribuudid
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PARASIIT')
txt = pygame.font.SysFont('leelawadeeui', 25, bold=True)

clock = pygame.time.Clock()

# mangija algatribuudid
score = 0
lives = 3
# jne

ussike = pygame.sprite.GroupSingle()
ussike.add(Player(160, 100, 4, 'ussike'))
# vaenlane
enemy_group = pygame.sprite.Group()
enemy_timer = pygame.USEREVENT + 0
pygame.time.set_timer(enemy_timer, 1000)  # kui tihti enemy spawnib

# taust
background = pygame.image.load(os.path.join("aluminetaust.png")).convert()
bg_x_pos = 0
background_2 = pygame.image.load(os.path.join("taust.png")).convert()
heart = pygame.image.load('heart.png')

# verelibled
verelible_group = pygame.sprite.Group()
verelible_timer = pygame.USEREVENT + 1
pygame.time.set_timer(verelible_timer, 1400)

# menu teeb hiljem

running = True
clock = pygame.time.Clock()

taust = pygame.image.load('pilt.png')
intro = True
close = False

while intro:
    juhend = False
    tegijad = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
            close = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 450 <= mouse[0] <= 550 and 140 <= mouse[1] <= 180:
                intro = False
            if 450 <= mouse[0] <= 550 and 190 <= mouse[1] <= 230:
                juhend = True

                while juhend:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            intro = False
                            close = True
                            juhend = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if 280 <= mouse[0] <= 340 and 285 <= mouse[1] <= 315:
                                juhend = False

                    pygame.draw.rect(screen, (37, 88, 107), [150, 120, 300, 200])

                    mouse = pygame.mouse.get_pos()

                    if 280 <= mouse[0] <= 340 and 285 <= mouse[1] <= 315:
                        pygame.draw.rect(screen, (52, 119, 144), [280, 285, 60, 30])
                    else:
                        pygame.draw.rect(screen, (37, 88, 107), [280, 285, 60, 30])

                    sulgeTekst = txt.render('Sulge', True, (255, 255, 255))
                    tekst = 'A  -  basic attack    S  -  spell attack       F  -  healing'
                    pikk_tekst(screen, txt, 160, 300, 150, tekst)
                    screen.blit(sulgeTekst, (290, 290))

                    pygame.display.update()

            if 450 <= mouse[0] <= 550 and 240 <= mouse[1] <= 280:
                tegijad = True

                while tegijad:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            intro = False
                            tegijad = False
                            close = True

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if 280 <= mouse[0] <= 340 and 285 <= mouse[1] <= 315:
                                tegijad = False

                    pygame.draw.rect(screen, (37, 88, 107), [150, 120, 300, 200])

                    mouse = pygame.mouse.get_pos()

                    if 280 <= mouse[0] <= 340 and 285 <= mouse[1] <= 315:
                        pygame.draw.rect(screen, (52, 119, 144), [
                                             280, 285, 60, 30])
                    else:
                        pygame.draw.rect(screen, (37, 88, 107), [280, 285, 60, 30])

                    sulgeTekst = txt.render('Sulge', True, (255, 255, 255))
                    aasta = txt.render('2021', True, (255, 255, 255))
                    tekst = 'Mängu on Teieni toonud              Erik Ivar Haav                    Charleen Konsa'
                    pikk_tekst(screen, txt, 210, 400, 150, tekst)
                    screen.blit(sulgeTekst, (290, 290))
                    screen.blit(aasta, (290, 240))

                    pygame.display.update()

    screen.blit(taust,(0,0))

    mouse = pygame.mouse.get_pos()

    if 350 <= mouse[0] <= 650 and 240 <= mouse[1] <= 320:
        pygame.draw.rect(screen, (233,76,129), [350, 240,300,80])
    else:
        pygame.draw.rect(screen, (108,15,22), [350, 240,300,80])

    if 350 <= mouse[0] <= 650 and 340 <= mouse[1] <= 420:
        pygame.draw.rect(screen, (233,76,129), [350, 340,300,80])
    else:
        pygame.draw.rect(screen, (108,15,22), [350, 340,300,80])

    if 350 <= mouse[0] <= 650 and 440 <= mouse[1] <= 520:
        pygame.draw.rect(screen, (233,76,129), [350, 440,300,80])
    else:
        pygame.draw.rect(screen, (108,15,22), [350, 440,300,80])

    pealkiri = txt.render('PARASIIT', True, (255,255,255))
    startTekst = txt.render('Start', True, (255,255,255))
    juhendTekst = txt.render('Juhend', True, (255,255,255))
    creditsTekst = txt.render('Credits', True, (255,255,255))
    screen.blit(pealkiri, (450, 100))
    screen.blit(startTekst, (275, 150))
    screen.blit(juhendTekst, (270, 200))
    screen.blit(creditsTekst, (270, 250))

    pygame.display.update()

if close:
    running = False

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

    screen.blit(background_2, (0, 0))
    bg_x_muut = bg_x_pos % background.get_rect().width
    screen.blit(background, (bg_x_muut - background.get_rect().width, 461))
    if bg_x_muut < width:
        screen.blit(background, (bg_x_muut, 461))
    bg_x_pos -= 0.3

    if pygame.sprite.spritecollide(ussike.sprite, verelible_group, True):
        score += 100

    score += start_time*0.000001
    score_txt = str(int(score))

    while len(score_txt) != 11:
        score_txt = '0' + score_txt

    for i in range(lives):
        screen.blit(heart, (8 + i*50, 30))

    screen.blit(txt.render(score_txt, True, (255, 255, 255)),(5,0))

    ussike.draw(screen)
    ussike.update()
    verelible_group.draw(screen)
    verelible_group.update()

    pygame.display.update()

pygame.quit()
