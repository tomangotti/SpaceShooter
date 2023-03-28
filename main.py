import pygame
import random
import sys
import os
import asyncio
from post import post_score



def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.font.init()
pygame.init()



WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MotherShip")

# fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10)


# stats
FPS = 60
VEL = 5
BULLET_VEL = 7
ENEMY_BULLET_VEL = 4
ENEMY_VEL = 1
# MAX_ENEMIES = 5
MAX_USER_BULLETS = 5
# MAX_ENEMY_BULLETS = 10
METEOR_VEL = 1
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
METEOR_WIDTH, METEOR_HEIGHT = 90, 90

# events
ENEMY_HIT = pygame.USEREVENT + 1
USER_HIT = pygame.USEREVENT + 2
METEOR_HIT = pygame.USEREVENT + 3


# assests
SPACE = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(resource_path('Assests/space.png')), 90), (WIDTH, HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(resource_path('Assests/spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)
RED_SPACESHIP_IMAGE = pygame.image.load(resource_path('Assests/spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
METEOR_IMAGE = pygame.image.load(resource_path('Assests/meteor.png'))
METEOR = pygame.transform.scale(METEOR_IMAGE, (METEOR_WIDTH, METEOR_HEIGHT))


# displaying on the window
def draw_window(user, enemies, user_bullets, enemy_bullets, USER_HEALTH, SCORE, meteors):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    WIN.blit(RED_SPACESHIP, (user.x, user.y))
    for enemy in enemies:
        WIN.blit(YELLOW_SPACESHIP, (enemy.x, enemy.y))

    user_health_text = HEALTH_FONT.render("Health: " + str(USER_HEALTH), 1, WHITE)
    score_text = SCORE_FONT.render("SCORE: " + str(SCORE), 1, WHITE)
    WIN.blit(user_health_text, (WIDTH - user_health_text.get_width() - 10, HEIGHT - 25))
    WIN.blit(score_text, (10, HEIGHT - 25))

    for bullet in user_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for meteor in meteors:
        WIN.blit(METEOR, (meteor.x, meteor.y))

    pygame.display.update()




# enemy movement
def handle_enemy_movement(enemies, user, MAX_Y):
    DISTANCE_MOVED = random.randint(1, MAX_Y)
    
    for enemy in enemies:
        if enemy.y < DISTANCE_MOVED:
            enemy.y += ENEMY_VEL
        if enemy.x < 0:
            enemy.x += 1
        if enemy.x > WIDTH - 50:
            enemy.x -= 1
        

# user movement map


def user_handle_movement(keys_pressed, user):
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and user.x - VEL > 0:  # left
        user.x -= VEL
    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and user.x + VEL + user.width < WIDTH:  # right
        user.x += VEL
    if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and user.y > BORDER.y + 10:  # up
        user.y -= VEL
    if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and user.y + VEL + user.height < HEIGHT:  # down
        user.y += VEL

# handle_meteor


def handle_meteor(meteors, user, user_bullets, enemy_bullets):
    for meteor in meteors:
        meteor.x += METEOR_VEL

        if user.colliderect(meteor):
            pygame.event.post(pygame.event.Event(METEOR_HIT))
            if meteor in meteors:
                meteors.remove(meteor)
        for bullet in user_bullets:
            if bullet.colliderect(meteor):
                if bullet in user_bullets:
                    user_bullets.remove(bullet)
        for bullet in enemy_bullets:
            if bullet.colliderect(meteor):
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)

        if meteor.x >= WIDTH:
            meteors.remove(meteor)

# bullet movements


def handle_bullets(user_bullets, enemy_bullets, user, enemies):
    for bullet in user_bullets:
        bullet.y -= BULLET_VEL
        for enemy in enemies:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                if bullet in user_bullets:
                    user_bullets.remove(bullet)
        if bullet.y < 0:
            if bullet in user_bullets:
                user_bullets.remove(bullet)

    for bullet in enemy_bullets:
        bullet.y += ENEMY_BULLET_VEL
        if user.colliderect(bullet):
            enemy_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(USER_HIT))
        if bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)

# winner Sscore


def draw_winner(text, SCORE):
    draw_text = WINNER_FONT.render(text + str(SCORE), 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    # pygame.display.update()
    # pygame.time.wait(1000)

    

    
    


async def main():
    user = pygame.Rect(250, 700, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    enemies = []
    meteors = []
    user_bullets = []
    enemy_bullets = []
    SCORE = 0
    USER_HEALTH = 10
    MAX_ENEMIES = 5
    MAX_ENEMY_BULLETS = 12
    MAX_METEORS = 1
    
    MAX_Y = 75

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        if SCORE >= 50:
            MAX_ENEMIES = 6
            MAX_ENEMY_BULLETS = 17
            MAX_Y = 100
            if BORDER.y < 450:
                BORDER.y += 1
        if SCORE >= 75:
            MAX_METEORS = 2
            
            if BORDER.y < 500:
                BORDER.y += 1
        if SCORE >= 100:
            MAX_Y = 150
            MAX_ENEMIES = 7
            MAX_ENEMY_BULLETS = 22
            if BORDER.y < 550:
                BORDER.y += 1
        if SCORE >= 150:
            MAX_METEORS = 3
        if SCORE >= 200:
            MAX_Y = 250
            MAX_ENEMIES = 10
            MAX_ENEMY_BULLETS = 30
            if BORDER.y < 600:
                BORDER.y += 1

                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if len(enemies) < MAX_ENEMIES:
                    yellow = pygame.Rect(random.randint(user.x - 150, user.x + 150), 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                    enemies.append(yellow)

                for enemy in enemies:
                    if len(enemy_bullets) < MAX_ENEMY_BULLETS:
                        bullet = pygame.Rect(enemy.x + enemy.width//2 - 2, enemy.y - enemy.height//2, 5, 10)
                        enemy_bullets.append(bullet)

                if event.key == pygame.K_SPACE and len(user_bullets) < MAX_USER_BULLETS:
                    bullet = pygame.Rect(user.x + user.width//2 - 2, user.y - user.height//2, 5, 10)
                    user_bullets.append(bullet)

                if len(meteors) < MAX_METEORS:
                    meteor = pygame.Rect(-500, random.randint(user.y -40, user.y + 10) ,  METEOR_WIDTH, METEOR_HEIGHT)
                    meteors.append(meteor)

            if event.type == USER_HIT:
                USER_HEALTH -= 1

            if event.type == ENEMY_HIT:
                SCORE += 1

            if event.type == METEOR_HIT:
                USER_HEALTH -= 3

        winner_text = ""
        if USER_HEALTH <= 0:
            winner_text = "GAME OVER! SCORE: "

        if winner_text != "":
            draw_winner(winner_text, SCORE)
            break

        keys_pressed = pygame.key.get_pressed()
        user_handle_movement(keys_pressed, user)
        handle_meteor(meteors, user, user_bullets, enemy_bullets)
        handle_bullets(user_bullets, enemy_bullets, user, enemies)
        handle_enemy_movement(enemies, user, MAX_Y)
        draw_window(user, enemies, user_bullets, enemy_bullets, USER_HEALTH, SCORE, meteors)
    
        await asyncio.sleep(0)
    asyncio.run(main())


asyncio.run(main())

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
