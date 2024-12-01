"""
涂鸦跳跃游戏
小人不断往上，键盘操控其不碰到怪物或落地
"""
import pygame
from settings import Settings
from doodler import Doodler
import game_functions as gf
from Platform import Platform
import pygame
from Camera import Camera
from pygame.sprite import Group
from GameStats import GameStats
from Button import Button
def run():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    # 创建游戏统计实例
    stats = GameStats(settings)
    pygame.display.set_caption("Doodle Jump")

    # Initialize doodler and platforms
    doodler = Doodler(settings, screen)
    # 绘制平台
    platforms = Group()

    # 初始化camera对象 （Camera整好了再启用）
    camera = Camera(settings)

    # 创建平台群
    gf.create_platforms(settings, camera, doodler, screen, platforms)
    # 设置自动跳跃定时器，影响小人落地后和再起跳之间的时间区间
    pygame.time.set_timer(pygame.USEREVENT, 50)

    # 创建Play按钮
    play_button = Button(settings, screen, "Play")

    while True:
        # Check for events like keypress，控制小人水平（手动）和垂直方向（半自动）
        gf.check_events(doodler)

        # Update doodler's position and movement 更新小人的逻辑位置和rect位置
        doodler.update()

        # 更新摄像机位置，以doodler为中心
        gf.update_camera(camera, doodler, platforms)

        # Update platform and handle doodler-platform collisions
        gf.update_platforms(settings, screen, camera, doodler, platforms)

        # Redraw screen and flip the display
        gf.update_screen(settings, screen, stats, doodler, platforms, play_button)

        # Control game frame rate
        settings.clock.tick(settings.FPS)

    def test():
        pass
    def test1():
        pass


if __name__ == "__main__":
    run()
