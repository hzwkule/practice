import pygame
import random
from os import path

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
NEW_ENEMY_GENERATE_INTERVAL = 500

center_x = center_y = 300
arrow_key_status = [0,0,0,0]

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(explosion_animation[0], (72,70))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 30:
            if self.frame < len(explosion_animation):
                self.image = pygame.transform.scale(explosion_animation[self.frame], (72,70))
                self.image.set_colorkey((0,0,0))
                self.frame += 1
                self.last_time = now
            else:
                self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.y -= 10

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_width = random.randint(20,120)
        self.image = pygame.transform.scale(enemy_img, (img_width, img_width))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.radius = 35
        #pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.w)

        self.vx = random.randint(-2,2)
        self.vy = random.randint(2,6)
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class Player(pygame.sprite.Sprite):    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(player_img,False,True)
        self.image = pygame.transform.scale(self.image, (53,40))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.bottom = SCREEN_HEIGHT
        self.radius = 20
        
    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= 5
        if key_state[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left =  0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        bullets.add(bullet)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
#now = pygame.time.ticks()

img_dir = path.join(path.dirname(__file__),'img')
background_dir = path.join(img_dir, 'background.png')
background_img = pygame.image.load(background_dir).convert()
background_rect = background_img.get_rect()
player_dir = path.join(img_dir, 'spaceShips_001.png')
player_img = pygame.image.load(player_dir).convert()
enemy_dir = path.join(img_dir, 'spaceMeteors_001.png')
enemy_img = pygame.image.load(enemy_dir).convert()
bullet_dir = path.join(img_dir, 'spaceMissiles_027.png')
bullet_img = pygame.image.load(bullet_dir).convert()

explosion_animation = []
for i in range(9):
    explosion_dir = path.join(img_dir, 'regularExplosion0{}.png'.format(i))
    explosion_img = pygame.image.load(explosion_dir).convert()
    explosion_animation.append(explosion_img)

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

last_enemy_generate_time = 0

game_over = False
while not game_over:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_UP:
                arrow_key_status[0] = 1
            elif event.key == pygame.K_DOWN:
                arrow_key_status[1] = 1
            elif event.key == pygame.K_LEFT:
                arrow_key_status[2] = 1
            elif event.key == pygame.K_RIGHT:
                arrow_key_status[3] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                arrow_key_status[0] = 0
            elif event.key == pygame.K_DOWN:
                arrow_key_status[1] = 0
            elif event.key == pygame.K_LEFT:
                arrow_key_status[2] = 0
            elif event.key == pygame.K_RIGHT:
                arrow_key_status[3] = 0

    now = pygame.time.get_ticks()
    if now - last_enemy_generate_time > NEW_ENEMY_GENERATE_INTERVAL:
        enemy = Enemy()
        enemies.add(enemy)
        last_enemy_generate_time = now
    
    if arrow_key_status[0]:
        center_y -=1
    if arrow_key_status[1]:
        center_y +=1
    if arrow_key_status[2]:
        center_x -=1
    if arrow_key_status[3]:
        center_x +=1

    player.update()
    enemies.update()
    bullets.update()
    explosions.update()

    #hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprtie.collide_rect_ratio(0.7))
    hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
    if hits:
        game_over = True
##    if pygame.sprite.groupcollide(enemies, bullets, True, True):
##        for i in range(2):
##            enemy = Enemy()
##            enemies.add(enemy)
##        enemies.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        explosion = Explosion(hit.rect.center)
        explosions.add(explosion)
    
    screen.blit(background_img,background_rect)
    screen.blit(player.image,player.rect)
    enemies.draw(screen)
    bullets.draw(screen)
    explosions.draw(screen)
    
    pygame.display.flip()

