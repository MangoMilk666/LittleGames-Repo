import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.setting = settings

        # load image and set rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 初始位置：屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 逻辑位置（小数，准确）
        self.x = float(self.rect.x)

    def blitme(self):
        """指定位置绘制"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """检查（单个）外星人是否撞到屏幕边缘。
        若位于屏幕边缘，返回True"""
        # 检查碰撞用rect位置
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        """向左/向右移动"""
        # 逻辑位置，向右增大，向左减小
        self.x += (self.setting.alien_speed_factor * self.setting.fleet_direction)
        # rect位置
        self.rect.x = self.x




