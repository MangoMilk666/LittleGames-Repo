import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game with Splash Screen")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("noteworthy", 74)  # choose default/system font with size 74


def show_splash_screen():
    """Show a splash screen for 3 seconds before the game starts."""
    start_time = pygame.time.get_ticks()  # Get the starting time

    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # Time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Render splash screen
        screen.fill(BLACK)
        text = font.render("Get Ready!", True, WHITE)
        countdown = font.render(f"{3 - int(elapsed_time)}", True, WHITE)  # Countdown timer
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(countdown, (screen_width // 2 - countdown.get_width() // 2, screen_height // 2))

        pygame.display.flip()

        # Wait for 3 seconds
        if elapsed_time >= 3:
            break

        clock.tick(60)  # Limit frame rate to 60 FPS


def main_game_loop():
    """Main game loop."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic here

        # Render the game screen
        screen.fill(BLACK)
        text = font.render("Game Running!", True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# # Main execution flow
# show_splash_screen()  # Show the splash screen
# main_game_loop()      # Start the game

def show_available_fonts():
    print(pygame.font.get_fonts())  # List all available system font names

if __name__ == "__main__":
    show_splash_screen()  # Show the splash screen
    main_game_loop()