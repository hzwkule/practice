import pygame

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

center_x = center_y = 300
arrow_key_status = [0,0,0,0]

def player_input(event_list):
    global arrow_key_status
    for event in event_list:
        if event.type == pygame.QUIT:
            game_over = True
            return game_over
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

    game_over = False
    while not game_over:        
        event_list = pygame.event.get()
        game_over = player_input(event_list)
        player_move()
        
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED,(100,100,50,80))
        pygame.draw.circle(screen, GREEN,(center_x,center_y),50)
        pygame.draw.ellipse(screen, BLUE, (100,100,50,80))
        pygame.display.flip()
        if game_over == True:
            pygame.display.quit()

if __name__ == '__main__':
    main()
