import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, settings, screen, ship):
        """飞船所处位置创建子弹对象"""
        super().__init__()
        self.screen = screen

        # （0，0）初创建子弹矩形
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 小数表示的子弹逻辑位置
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 逻辑位置
        self.y -= self.speed_factor
        # rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹
            使用self.color填充self.rect占据的screen部分"""
        pygame.draw.rect(self.screen, self.color, self.rect)
