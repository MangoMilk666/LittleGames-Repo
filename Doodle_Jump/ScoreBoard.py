import pygame.font
class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, setting, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.setting = setting
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分及上升高度的图像
        self.prep_score()
        self.prep_height()

    def prep_score(self):
        """将得分渲染成一幅图像"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_height(self):
        """将上升高度渲染成一幅图像"""
        height_str = str(self.stats.score)
        self.height_image = self.font.render(height_str, True, self.text_color, self.setting.bg_color)

        # 将得分放在屏幕右上角
        self.height_rect = self.height_image.get_rect()
        self.height_rect.right = self.screen_rect.right - 20
        self.height_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)

    def show_height(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.height_image, self.height_rect)
