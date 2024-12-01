import pygame

class Settings():
    """储存《涂鸦跳跃》中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #帧率设置
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # 小人左右移动速度的设置
        self.doodler_moving_speed_factor = 10

        #小人起跳初速度
        self.initial_jumping_speed = -25
       # self.doodler_jumping_speed = self.initial_jumping_speed

        #小人上升和下降加速度的设置
        self.gravity = 0.7

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        pass

