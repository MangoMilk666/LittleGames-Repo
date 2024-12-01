import pygame
class Doodler:
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        self.image_right = pygame.image.load("images/doodler_right.png")
        self.image_left = pygame.image.load("images/doodler_left.png")
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start doodler at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.jump_speed = self.settings.initial_jumping_speed

    def update(self):
        """更新小人位置坐标"""
        # Horizontal movement
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.doodler_moving_speed_factor
            self.image = self.image_right
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.doodler_moving_speed_factor
            self.image = self.image_left
        # update self.rect position
        self.rect.centerx = self.centerx

        # Vertical jump movement
        if self.jumping:
            self.jumpUp()
        else:
            self.fallDown()
        # update self.rect position
        self.rect.bottom = self.bottom

    def jumpAgain(self):
        """Initiate jumping only if the doodler isn't already in the air, but alrady at ground/platform."""
        if not self.jumping:
            self.jumping = True
            self.jump_speed = self.settings.initial_jumping_speed

    def blitme(self, rect=None):
        if rect: # rect != None
            self.screen.blit(self.image, rect)  # 使用传入的矩形位置
        else:
            self.screen.blit(self.image, self.rect)  # 使用原始矩形位置

    def jumpUp(self):
        # y坐标 < 0, and y不断减小
        # 默认self.jump_speed <= 0
        self.bottom += self.jump_speed
        # 受加速度影响，营造减速效果
        self.jump_speed += self.settings.gravity
        if self.jump_speed >= 0:
            self.jump_speed = 0
            self.jumping = False



    def fallDown(self):
        # y坐标 >= 0, and y不断增大
        # self.jump_speed >= 0
        self.bottom += self.jump_speed
        # 加速度，营造加速下落效果
        self.jump_speed += self.settings.gravity
        if self.bottom >= self.screen_rect.bottom:
            self.bottom = self.screen_rect.bottom




