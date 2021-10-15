import pygame
import os
pygame.font.init()
pygame.mixer.init()
current_path = os.path.dirname(__file__)
# Variables

HEALTH = 14
WIDTH, HEIGHT = 900, 500
FPS = 60
SPEED = 5
BULLET_SPEED = 7
MAX_BULLETS = 3

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join(current_path, 'Assets', 'Grenade+1.wav'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join(current_path, 'Assets', 'Gun+Silencer.wav'))
BULLET_FIRE_SOUND.set_volume(0.025)
BULLET_HIT_SOUND.set_volume(0.025)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Offline 2 Player game | Ayushman Pyne")

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join(current_path, 'Assets', 'space.png')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join(current_path, 'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join(current_path, 'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "HEALTH : " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "HEALTH : " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def draw_winner(text):
    draw_winner = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_winner, (WIDTH//2 - draw_winner.get_width() /
             2, HEIGHT//2-draw_winner.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - SPEED > 0:  # UP
        yellow.y -= SPEED
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + SPEED < HEIGHT - 15:  # DOWN
        yellow.y += SPEED
    if keys_pressed[pygame.K_a] and yellow.x - SPEED > 0:  # LEFT
        yellow.x -= SPEED
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + SPEED < BORDER.x:  # RIGHT
        yellow.x += SPEED


def red_move(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - SPEED > 0:  # UP
        red.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + SPEED < HEIGHT - 15:  # DOWN
        red.y += SPEED
    if keys_pressed[pygame.K_LEFT] and red.x - SPEED > BORDER.x + BORDER.width:  # LEFT
        red.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + SPEED < WIDTH:  # RIGHT
        red.x += SPEED


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    yellow = pygame.Rect(225, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(675, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    red_health = HEALTH
    yellow_health = HEALTH
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner = ""
        if red_health <= 0:
            winner = "YELLOW Wins!"
        if yellow_health <= 0:
            winner = "RED Wins!"
        if winner != "":
            draw_winner( winner)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_move(keys_pressed, yellow)
        red_move(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    yellow_health, red_health)
    
    pygame.quit()


if __name__ == "__main__":
    main()
