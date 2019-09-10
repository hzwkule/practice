import pygame
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

center_x = center_y = 300
arrow_key_status = [0,0,0,0]
clock = pygame.time.Clock()



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.Surface((5,10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.y -= 10

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.w)
        self.vx = random.randint(-2,2)
        self.vy = random.randint(2,10)
        
    def update(self):
        self.rect.x = self.vx
        self.rect.y = self.vy

class Player(pygame.sprite.Sprite):    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.bottom = SCREEN_HEIGHT
        
    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.rect.x -= 5
        if key_state[pygame.K_LEFT]:
            self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left =  0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.centery)
        bullets.add(bullet)

def player_input(event_list):
    global arrow_key_status
    for event in event_list:
        if event.type == pygame.QUIT:
            game_over = True
            return game_over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
                return game_over
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.KEYDOWN:
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

def player_move():
    global center_x
    global center_y
    if arrow_key_status[0]:
        center_y -=1
    if arrow_key_status[1]:
        center_y +=1
    if arrow_key_status[2]:
        center_x -=1
    if arrow_key_status[3]:
        center_x +=1

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Space Shooter')

    player = Player()
    enemys = pygame.sprite.Group()
    for i in range(10):
        enemy = Enemy()
        enemys.add(enemy)
    bullets = pygame.sprite.Group()
    
    game_over = False
    while not game_over:
        clock.tick(60)
        event_list = pygame.event.get()
        game_over = player_input(event_list)
        player_move()
        
        screen.fill(WHITE)

        player.update()
        enemys.update()
        bullets.update()

        hits = pygame.sprite.spritecollide(player, enemys, False)
        if hits:
            game_over = True
        pygame.sprite.groupcollide(enemys, bullets, True, True)
        
        screen.blit(player.image,player.rect)
        enemys.draw(screen)
        bullets.draw(screen)
        
        pygame.display.flip()
        if game_over == True:
            pygame.display.quit()

if __name__ == '__main__':
    main()
