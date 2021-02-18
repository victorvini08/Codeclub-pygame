#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pygame
import random
import os


black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)

font_name=pygame.font.match_font('arial')
fps=30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
score=0
game_folder=os.path.dirname(r"./")
img_folder=os.path.join(game_folder,"")

snd_folder=os.path.join(game_folder,"")
snd=os.path.join(snd_folder,"Apoxode_-_Electric_1.wav")
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,white)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)
    
    
def show_go_screen():
    screen.fill((135,206,250))
    
    draw_text(screen,"HELLO!",64,SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
    draw_text(screen,"Press any key to play",36,SCREEN_WIDTH/2,SCREEN_HEIGHT*3/4)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYUP:
                waiting=False
                
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join(img_folder,"player.png")).convert()
        
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.lives=3
        self.hidden=False
        self.hide_timer=pygame.time.get_ticks()
    
    def update(self, pressed_keys):
        
        if self.hidden and pygame.time.get_ticks()-self.hide_timer>1000:
            self.hidden=False
            self.rect.center=(10,SCREEN_HEIGHT)
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
          
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def hide(self):
        self.hidden=True
        self.hide_timer=pygame.time.get_ticks()
        self.rect.center=(0,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join(img_folder,"enemy.png")).convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
       
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

   
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            
            self.kill()
            



class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(img_folder,"cloud.png")).convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
       
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()



pygame.mixer.init()
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
game_over=True

while running:
    
    if game_over:
        show_go_screen()
        game_over=False
        player = Player()

        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
    
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(snd)
        pygame.mixer.music.play(-1)

    
    for event in pygame.event.get():
       
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                running = False

        
        elif event.type == pygame.QUIT:
            running = False

        
        elif event.type == ADDENEMY:
            
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        
        elif event.type == ADDCLOUD:
            
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    
    enemies.update()
    
    clouds.update()

    
    screen.fill((135, 206, 250))

    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if pygame.sprite.spritecollideany(player, enemies):
        
        
        player.kill()   
        game_over=True
    draw_text(screen,str(score),18,SCREEN_WIDTH/2,10)
    pygame.display.flip()
    
    clock.tick(30)


pygame.quit()


# In[ ]:





# In[ ]:



