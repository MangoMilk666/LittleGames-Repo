# test draft for game logics
import sys
import pygame
import random

pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Doodler settings
DOODLER_WIDTH, DOODLER_HEIGHT = 50, 50
DOODLER_START_X, DOODLER_START_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
doodler_moving_right = False
doodler_moving_left = False

# Platform settings
PLATFORM_WIDTH, PLATFORM_HEIGHT = 70, 15
PLATFORM_COUNT = 10

# Game variables
doodler_x = DOODLER_START_X
doodler_y = DOODLER_START_Y
doodler_velocity_y = 0
doodler_speed_x = 10
gravity = 0.3  # Adjusted gravity
jump_strength = -12  # Adjusted jump strength

# Camera offset
camera_offset_y = 0
max_camera_speed = 10  # Limit scrolling speed

# Score and difficulty adjustment
score = 0
difficulty_increment = 0.001  # Gradual difficulty increase

# Platforms
platforms = [
    pygame.Rect(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT) for _ in range(PLATFORM_COUNT)
]

# Font for Game Over
font = pygame.font.Font(None, 74)

# Clock
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                doodler_moving_right = True
            elif event.key == pygame.K_LEFT:
                doodler_moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                doodler_moving_right = False
            elif event.key == pygame.K_LEFT:
                doodler_moving_left = False

    # Apply gravity and speed
    doodler_velocity_y += gravity
    doodler_y += doodler_velocity_y
    if doodler_moving_right and doodler_x < SCREEN_WIDTH - DOODLER_WIDTH:
        doodler_x += doodler_speed_x
    if doodler_moving_left and doodler_x > 0:
        doodler_x -= doodler_speed_x

    # Check if Doodler falls below the screen
    if doodler_y > SCREEN_HEIGHT:
        screen.fill(RED)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Show the message for 2 seconds
        pygame.quit()
        sys.exit()

    # Jump when landing on a platform
    if doodler_velocity_y > 0:
        for platform in platforms:
            # Check for collision with platforms
            if doodler_velocity_y > 0 and doodler_x + DOODLER_WIDTH > platform.x and doodler_x < platform.x + PLATFORM_WIDTH and doodler_y + DOODLER_HEIGHT >= platform.y and doodler_y + DOODLER_HEIGHT <= platform.y + PLATFORM_HEIGHT:
                doodler_velocity_y = jump_strength

    # Camera logic with speed cap
    if doodler_y < SCREEN_HEIGHT // 3:  # If Doodler moves above 1/3rd of the screen
        offset = (SCREEN_HEIGHT // 3 - doodler_y)
        camera_offset_y += min(offset, max_camera_speed)  # Limit camera movement
        doodler_y = SCREEN_HEIGHT // 3  # Reset Doodler's position to the threshold

    # Move platforms and remove off-screen ones
    for platform in platforms:
        platform.y += camera_offset_y  # Apply camera offset

    platforms = [platform for platform in platforms if platform.y < SCREEN_HEIGHT]  # Keep only visible platforms

    # Add new platforms at the top
    while len(platforms) < PLATFORM_COUNT:
        platforms.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),
                                     random.randint(-150, -50),  # Increased spacing
                                     PLATFORM_WIDTH,
                                     PLATFORM_HEIGHT))

    # Gradually increase difficulty
    score += 1
    gravity += difficulty_increment
    max_camera_speed += difficulty_increment

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Draw Doodler
    pygame.draw.rect(screen, BLUE, (doodler_x, doodler_y, DOODLER_WIDTH, DOODLER_HEIGHT))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
