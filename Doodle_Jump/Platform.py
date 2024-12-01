import pygame
from pygame.sprite import Sprite
import random as rd
class Platform(Sprite):
    def __init__(self, doodler, settings, screen, camera, category):
        super(Platform, self).__init__()
        """设置起始位置？"""
        self.screen = screen
        self.setting = settings
        self.category = category
        self.doodler = doodler


        #加载平台图像，设置rect属性
        if self.category == 'green':
            self.image = pygame.image.load('images/green_platform.png')
            self.rect = self.image.get_rect()
            # self.rect.x = rd.randint(0, 700)
            # 左右水平位置摆动
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            # self.rect.y = rd.randint(0, 500)
            min_y = max(0, doodler.rect.bottom - 200)  # Ensure platform is not too low
            max_y = max(50, doodler.rect.top - 300)  # Ensure platform is above doodler's top
            # Ensure min_y <= max_y
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        if self.category == 'broken':
            self.image = pygame.image.load('images/broken_platform.png')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, 700)
            self.rect.y = rd.randint(0, 800)

        #用小数储存平台的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制平台"""
        self.screen.blit(self.image, self.rect)

    # #管理平台的位置
    def update(self):
        """随机在空中出现各类平台"""
        pass





