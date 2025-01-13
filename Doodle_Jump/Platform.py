import time

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
        # platform.rect.bottom - platform.rect.top == 28
        self.horizontal_move = 0 # 仅作用于blue platform, 0:静止, 1:右侧的平台向左, 2:向右; -1:左侧的平台向左, -2:左侧的平台向右
        self.state = "static"

        self.vertical_move = 0 # 仅作用于yellow platform. 0: 静止, -1:向上， 1:向下


        #加载平台图像，设置rect属性
        if self.category == 'green':
            self.image = pygame.image.load('images/green_platform.png')
            self.rect = self.image.get_rect()
            # self.rect.x = rd.randint(0, 700)
            # 左右水平位置摆动
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            # self.rect.y = rd.randint(0, 500)
            min_y = max(0, doodler.rect.bottom - 100)  # Ensure platform is not too low
            max_y = max(50, doodler.rect.top - 300)  # Ensure platform is above doodler's top
            # Ensure min_y <= max_y
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        # 绿色+蹦床平台
        if self.category == 'trampoline':
            self.image = pygame.image.load('images/trampoline.bmp')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            min_y = max(0, doodler.rect.bottom - 100)
            max_y = max(50, doodler.rect.top - 300)
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        # 绿色+弹簧平台
        if self.category == 'spring':
            self.image = pygame.image.load('images/spring_platform_right.bmp')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            min_y = max(0, doodler.rect.bottom - 100)
            max_y = max(50, doodler.rect.top - 300)
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        # 棕色断裂平台
        if self.category == 'broken':
            self.image = pygame.image.load('images/broken_platform.bmp')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            min_y = max(0, doodler.rect.bottom - 100)
            max_y = max(50, doodler.rect.top - 300)
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        # 蓝色水平移动平台
        if self.category == 'blue':
            self.image = pygame.image.load('images/blue_platform.bmp')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            min_y = max(0, doodler.rect.bottom - 100)
            max_y = max(50, doodler.rect.top - 300)
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)

        # 黄色垂直移动平台
        if self.category == 'yellow':
            self.image = pygame.image.load('images/yellow_platform.bmp')
            self.rect = self.image.get_rect()
            self.rect.x = rd.randint(0, settings.screen_width - self.rect.width)
            min_y = max(0, doodler.rect.bottom - 100)  # Ensure platform is not too low
            max_y = max(50, doodler.rect.top - 300)  # Ensure platform is above doodler's top
            # Ensure min_y <= max_y
            if min_y > max_y:
                min_y, max_y = max_y, min_y
            self.rect.y = rd.randint(min_y, max_y)
            self.initial_y = self.rect.centery

        #用小数储存平台的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制平台"""
        self.screen.blit(self.image, self.rect)

    # #管理平台的位置
    def update(self):
        """特殊平台位置更新"""
        if self.category == "blue": # 这段代码逻辑，需要仔细考虑
            if self.state == "static":
                if self.rect.centerx <= self.setting.screen_width / 2:
                    if self.rect.left == 0:   # left end for left platforms
                        self.horizontal_move = -2
                    elif self.rect.centerx == self.setting.screen_width/2: # right end for left platforms
                        self.horizontal_move = -1
                    else:
                        self.horizontal_move = -2
                else:
                    if self.rect.centerx == 1+ self.setting.screen_width / 2: # left end for right platforms
                        self.horizontal_move = 2
                    elif self.rect.right == self.setting.screen_width: #right end for right platforms
                        self.horizontal_move = 1
                    else:
                        self.horizontal_move = 2
                self.state = "moving"

            if self.state == "moving":
                if abs(self.horizontal_move) == 1: # leftward moving
                    self.rect.centerx -= self.setting.blue_platform_horizontal_speed
                elif abs(self.horizontal_move) == 2: # rightward moving
                    self.rect.centerx += self.setting.blue_platform_horizontal_speed

                if self.rect.left <= 0:
                    self.rect.left = 0
                    self.state = "static"
                elif self.rect.right >= self.setting.screen_width:
                    self.rect.right = self.setting.screen_width
                    self.state = "static"
                # right end for left platforms
                elif self.rect.centerx >= self.setting.screen_width / 2 and self.horizontal_move < 0:
                    self.rect.centerx = self.setting.screen_width/2
                    self.state = "static"
                # left end for right platforms
                elif self.rect.centerx <= 1 + self.setting.screen_width / 2 and self.horizontal_move > 0:
                    self.rect.centerx = 1+ self.setting.screen_width/2
                    self.state = "static"

        if self.category == "yellow":
            if self.state == "static":

                self.state = "moving"
                self.start_time = pygame.time.get_ticks()  # Get the starting time

            elif self.state == "moving":
                self.current_time = pygame.time.get_ticks()
                elapsed_time = (self.current_time - self.start_time) / 1000  # Time in seconds

                if elapsed_time <= 2:
                    self.vertical_move = -1
                elif elapsed_time > 3 and elapsed_time <= 5:
                    self.vertical_move = 1
                elif elapsed_time > 5:
                    self.state = "static"









