# --- Imports ----
import pygame
from paddle import Paddle
from ball import Ball

# Initialize all imported pygame modules
pygame.init()


# --- Window ----

# Dimensions
window_width = 700
window_height = 500
widow_size = (window_width, window_height)

# Open
window = pygame.display.set_mode(widow_size)
pygame.display.set_caption("Pong")


# Dictionary of colors
colors = {'black': (0, 0, 0), 'white': (255, 255, 255)}

# --- Scores ----
score_player_one = 0
score_player_two = 0


# --- Paddle ----

# Dimensions
paddle_width = 15
paddle_height = 75

paddle_one = Paddle(colors['white'], paddle_width, paddle_height)
paddle_one.rect.x = 20
paddle_one.rect.y = 200

paddle_two = Paddle(colors['white'], paddle_width, paddle_height)
paddle_two.rect.x = 670
paddle_two.rect.y = 200


# --- Ball ----

# Dimensions
ball_width = 15
ball_height = 15

ball = Ball(colors['white'], ball_width, ball_height)
ball.rect.x = 345
ball.rect.y = 195


# --- List of Sprites ----
sprite_list = pygame.sprite.Group()

sprite_list.add(paddle_one)
sprite_list.add(paddle_two)
sprite_list.add(ball)


# --- Game Loop ----
is_running = True
clock = pygame.time.Clock()  # Used to adjust screen updates


while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                is_running = False

    # --- User Input ----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_one.rect.y > 0:
        paddle_one.up(5)
    if keys[pygame.K_s] and paddle_one.rect.y < window_height - paddle_height:
        paddle_one.down(5)
    if keys[pygame.K_UP] and paddle_two.rect.y > 0:
        paddle_two.up(5)
    if keys[pygame.K_DOWN] and paddle_two.rect.y < window_height - paddle_height:
        paddle_two.down(5)

    # --- Game Logic ----
    sprite_list.update()

    # Ball Collision
    if ball.rect.x >= window_width - 10:
        score_player_one += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        score_player_two += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > window_height - 10:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    # Detect when paddle collides with ball
    if pygame.sprite.collide_mask(ball, paddle_one) or pygame.sprite.collide_mask(ball, paddle_two):
        ball.bounce()

    # --- Screen updates ----

    # Clear content to only black BG
    window.fill(colors['black'])

    # Draw Net
    pygame.draw.line(window, colors['white'], [(window_width / 2), 0], [(window_width / 2), window_height], 5)
    sprite_list.draw(window)  # Draw sprites

    # Display scores:s
    font = pygame.font.Font(None, 74)
    text = font.render(str(score_player_one), 1, colors['white'])
    window.blit(text, ((window_width / 2) - 75, 10))
    text = font.render(str(score_player_two), 1, colors['white'])
    window.blit(text, ((window_width / 2) + 50, 10))

    pygame.display.flip()  # Update screen with draw calls
    clock.tick(60)         # Set FPS

# Exit program on loop exit
pygame.quit()
