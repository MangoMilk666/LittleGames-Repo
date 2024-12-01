import pygame

from Button import Button
from GameStats import GameStats
from Settings import Settings
from Ship import Ship
import Game_Functions as gf
from pygame.sprite import Group #sprite类的编组
from Alien import Alien
from ScoreBoard import Scoreboard
def run_game():
    # 创建屏幕对象
    pygame.init()

    setting = Settings()
    # screen对象是一个surface（游戏中每个元素都是）
    screen = pygame.display.set_mode((setting.screen_width,
                                      setting.screen_height))
    ship = Ship(setting, screen)

    # group for bullets and aliens
    bullets = Group()
    aliens = Group()

    # 创建游戏统计实例
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)
    pygame.display.set_caption("Alien Invasion")

    # 创建外星人群
    gf.create_fleet(setting, screen, ship, aliens)

    # 创建Play按钮
    play_button = Button(setting, screen, "Play")

    # 游戏主循环
    while True:
        # 任何情况下都调用
        gf.check_events(setting, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:  # 当且仅当游戏处于活动状态下调用
            ship.update()

            gf.update_bullets(setting, screen, stats, sb, ship, aliens, bullets)

            # 更新外星人位置
            gf.update_aliens(setting, stats, screen, ship, aliens, bullets)


        gf.update_screen(setting, screen, stats, sb, ship, aliens, bullets, play_button)

if __name__ == "__main__":
    run_game()