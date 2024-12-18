import pygame.font


class Button:
    def __init__(self, setting, screen, msg):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 按钮尺寸等属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0) # 亮绿色
        self.text_color = (255,255,255) #白色
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，设置为居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只要创建一次，msg：待显示文本
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg储存的文本渲染为图像，并使其在按钮上居中"""
        # antialias：反锯齿，让文本边缘更光滑
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)