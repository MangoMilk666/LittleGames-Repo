import pygame

from GameStats import GameStats
from Settings import Settings
from Ship import Ship
import Game_Functions as gf
from pygame.sprite import Group #sprite类的编组
from Alien import Alien
def run_game():
    # 创建屏幕对象
    pygame.init()

    setting = Settings()
    # screen对象是一个surface（游戏中每个元素都是）
    screen = pygame.display.set_mode((setting.screen_width,
                                      setting.screen_height))
    ship = Ship(setting, screen)
    alien = Alien(setting, screen)

    # group for bullets and aliens
    bullets = Group()
    aliens = Group()

    # 创建游戏统计实例
    stats = GameStats(setting)
    pygame.display.set_caption("Alien Invasion")

    # 创建外星人群
    gf.create_fleet(setting, screen, ship, aliens)


    # 游戏主循环
    while True:
        ''' 监视键盘和鼠标事件的代码，整合到GF类：
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 sys.exit()
         '''
        gf.check_events(setting, screen, ship, bullets)

        ship.update()
        '''更新子弹数量和位置代码整合到GF类
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        print("Bullets left:", len(bullets))
        '''
        gf.update_bullets(setting, screen, ship, aliens, bullets)

        # 更新外星人位置
        gf.update_aliens(setting, stats, screen, ship, aliens, bullets)
        '''更新屏幕的代码，整合至GF
        每次循环，背景色填充重绘屏幕
        screen.fill(settings.bg_color)
        ship.blitme()
        # 使最近绘制的屏幕可见：每次执行，擦除旧屏幕，显示新屏幕
        pygame.display.flip()
        '''
        gf.update_screen(setting, screen, ship, aliens, bullets)

if __name__ == "__main__":
    run_game()