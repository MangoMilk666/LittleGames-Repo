import pygame

class Ship():
    def __init__(self, settings, screen):
        self.screen = screen
        self.setting = settings
        # 加载ship图像，获取外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #每艘新飞船放在屏幕底部中央
        # 元素和屏幕边缘对齐：top, bottom, left, right
        # rect对象的属性：center,centerx,centery
        # 调整元素水平/垂直位置：x, y,矩形左上角坐标
        # pygame中，原点(0, 0)位于屏幕左上角，下右正方向
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 属性center存储小数
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整位置"""
        # 先更新能存储小数的逻辑位置center
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.setting.ship_speed_factor

        # 再更新rect对象位置
        self.rect.centerx = self.center

    def blitme(self):
        # 指定位置绘制飞船
        self.screen.blit(self.image, self.rect)
