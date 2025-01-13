import pygame

class Settings():
    """储存《涂鸦跳跃》中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color_grey = (230, 230, 230)
        self.color_white = (255, 255, 255)
        self.bg_color_black = (0, 0, 0)
        self.screen_font = pygame.font.SysFont("noteworthy", 74)  # Default font with size 74

        #帧率设置
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # 小人左右移动速度的设置
        self.doodler_moving_speed_factor = 10

        #小人起跳初速度 - 一般情况
        self.initial_jumping_speed_common = -25

        # 小人起跳初速度 - 蹦床/弹簧
        self.initial_jumping_speed_spring = -35

        #小人上升和下降加速度的设置
        self.gravity = 0.7

        # 平台移动参数
        self.blue_platform_horizontal_speed = 3
        self.yellow_platform_vertical_relative_speed = 2
        self.yellow_platform_height_limitation = 25

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        pass

