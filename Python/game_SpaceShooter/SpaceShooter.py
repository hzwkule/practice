import pygame
import random
from os import path

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
NEW_ENEMY_GENERATE_INTERVAL = 500
MISSILE_LIFETIME = 10000
MISSILE_INTERVAL = 500

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

center_x = center_y = 300
arrow_key_status = [0,0,0,0]


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()        
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

class Missile(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        self.rect.y -= 5

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        random_num = random.random()
        if random_num <0.5:
            self.type = 'add_hp'
        elif random_num < 0.8:
            self.type = 'add_missile'
        else:
            self.type = 'add_life'
        self.image = powerup_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rect.y += 4

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
        self.image_origin = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.radius = img_width // 2
        #pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.w)

        self.vx = random.randint(-2,2)
        self.vy = random.randint(2,6)

        self.last_time = pygame.time.get_ticks()
        self.rotate_speed = random.randint(-5,5)
        self.rotate_angle = 0
        

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 30:
            old_center = self.rect.center
            self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
            self.image =  pygame.transform.rotate(self.image_origin, self.rotate_angle)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.last_time = now
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.rotate()

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

        self.hp = 100
        self.lives = 3
        self.score = 0
        self.is_god = False
        self.god_time = 0

        self.is_missile_firing = False
        self.start_missile_time = 0#pygame.time.get_ticks()
        self.last_missile_time = 0
    
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

        now = pygame.time.get_ticks()
        if self.is_god and now - self.god_time > 3000:
            self.is_god = False

        if self.is_missile_firing:
            if now - self.start_missile_time < MISSILE_LIFETIME:
                if now - self.last_missile_time > MISSILE_INTERVAL:
                    
                    missile = Missile(self.rect.center)
                    missiles.add(missile)
                    self.last_missile_time = now
            else:
                self.is_missile_firing = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        bullets.add(bullet)
        shoot_sound.play()

    def god(self):
        self.is_god = True
        self.hide_time = pygame.time.get_ticks()

    def fire_missile(self):
        self.is_missile_firing = True
        self.start_missile_time = pygame.time.get_ticks()
        

def draw_ui():
    pygame.draw.rect(screen, GREEN, (10,10,player.hp,15))
    pygame.draw.rect(screen, WHITE, (10,10,100,15), 2)
    draw_text(player.score, SCREEN_WIDTH/2, 10, screen)
    #draw_text(f'score:{player.score}', SCREEN_WIDTH/2, 10)
    img_rect = player_img_small.get_rect()
    img_rect.right = SCREEN_WIDTH - 10
    img_rect.top = 10
    for _ in range(player.lives):
        screen.blit(player_img_small, img_rect)
        img_rect.x -= img_rect.width + 10

def draw_text(text, x, y, surface=screen, color=WHITE, font_size=20):
    font_name = pygame.font.match_font('arial')
    # font can be downloaded and import through font_name as path
    font = pygame.font.Font(font_name, font_size)
    #font = pygame.fon.Font('./slafla.ttf', font_size)
    text_surface = font.render(str(text),True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_menu():
    global game_state, screen, game_over
    screen.blit(background_img, background_rect)

    draw_text('Space Shooter', SCREEN_WIDTH/2, 100, font_size = 40)
    draw_text('Press Space to Start', SCREEN_WIDTH/2, 300, font_size = 20)
    draw_text('Press Esc to Exit', SCREEN_WIDTH/2, 350, font_size = 20)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
                game_over = True
            elif event.key == pygame.K_SPACE:
                game_state = 1

img_dir = path.join(path.dirname(__file__),'img')
background_dir = path.join(img_dir, 'background.png')
background_img = pygame.image.load(background_dir).convert()
background_rect = background_img.get_rect()
player_dir = path.join(img_dir, 'spaceShips_001.png')
player_img = pygame.image.load(player_dir).convert()
player_img_small = pygame.transform.scale(player_img, (26, 20))
player_img_small.set_colorkey((0,0,0))
enemy_dir = path.join(img_dir, 'spaceMeteors_001.png')
enemy_img = pygame.image.load(enemy_dir).convert()
bullet_dir = path.join(img_dir, 'spaceMissiles_027.png')
bullet_img = pygame.image.load(bullet_dir).convert()

powerup_imgs = {}
powerup_add_hp_dir = path.join(img_dir, 'gem_red.png')
powerup_imgs['add_hp'] = pygame.image.load(powerup_add_hp_dir).convert()
powerup_add_life_dir = path.join(img_dir, 'heartFull.png')
powerup_imgs['add_life'] = pygame.image.load(powerup_add_life_dir).convert()
powerup_add_missile_dir = path.join(img_dir, 'gem_yellow.png')
powerup_imgs['add_missile'] = pygame.image.load(powerup_add_missile_dir).convert()
missile_dir = path.join(img_dir, 'spaceMissiles_040.png')
missile_img = pygame.image.load(missile_dir).convert()

sound_dir = path.join(path.dirname(__file__), 'sound')
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'shoot.wav'))
shoot_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(path.join(sound_dir, 'explosion.wav'))
explosion_sound.set_volume(0.5)
pygame.mixer.music.load(path.join(sound_dir, 'AMemoryAway.ogg'))
hurt_sound = pygame.mixer.Sound(path.join(sound_dir, 'hurt.wav'))

explosion_animation = []
for i in range(9):
    explosion_dir = path.join(img_dir, 'regularExplosion0{}.png'.format(i))
    explosion_img = pygame.image.load(explosion_dir).convert()
    explosion_animation.append(explosion_img)

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
powerups = pygame.sprite.Group()
missiles = pygame.sprite.Group()

last_enemy_generate_time = 0

game_over = False
game_state = 0
pygame.mixer.music.play(loops=-1)
while not game_over:
    clock.tick(60)
    if game_state == 0:
        show_menu()
    elif game_state == 1:
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
        powerups.update()
        missiles.update()

        #hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprtie.collide_rect_ratio(0.7))
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        for hit in hits:
            if not player.is_god:
                hurt_sound.play()
                player.hp -= hit.radius
            if player.hp <= 0:
                player.god()
                player.lives -= 1
                player.hp = 100
                if player.lives == 0:
                    game_over = True
            
    ##    if pygame.sprite.groupcollide(enemies, bullets, True, True):
    ##        for i in range(2):
    ##            enemy = Enemy()
    ##            enemies.add(enemy)
    ##        enemies.update()

        hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
        for hit in hits:
            if hit.type == 'add_hp':            
                player.hp += 50
                if player.hp > 100:
                    player.hp = 100
            elif hit.type == 'add_life':
                player.lives += 1
                if player.lives > 3:
                    player.lives = 3
            else:
                player.fire_missile()

        bullet_hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        missile_hits = pygame.sprite.groupcollide(enemies, missiles, True, True)
        hits = {}
        hits.update(bullet_hits)
        hits.update(missile_hits)
        for hit in hits:
            explosion = Explosion(hit.rect.center)
            explosions.add(explosion)
            explosion_sound.play()
            player.score += (100 - hit.radius)
            if random.random() > 0.5:
                powerup = PowerUp(hit.rect.center)
                powerups.add(powerup)
        
        screen.blit(background_img,background_rect)
        screen.blit(player.image,player.rect)
        enemies.draw(screen)
        bullets.draw(screen)
        explosions.draw(screen)
        powerups.draw(screen)
        missiles.draw(screen)

        draw_ui()
        
    pygame.display.flip()

