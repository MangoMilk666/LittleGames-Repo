import sys
import pygame
from Bullet import Bullet
from Alien import Alien
from time import sleep
def check_keydown_events(event, setting, screen, ship, bullets):
    # ship移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 子弹射出
    elif event.key == pygame.K_SPACE:
        # 创建子弹，加入编组
        fire_bullets(setting, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(setting, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_bullets(setting, screen, ship, aliens, bullets):
    """更新子弹位置
        删除到顶子弹"""
    bullets.update()
    # 通过避免直接修改正在遍历的列表，避免了跳过元素的风险
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 最好定时显示 print("Bullets left:", len(bullets))
    check_bullet_alien_collisions(setting, screen, ship, aliens, bullets)
def check_bullet_alien_collisions(setting, screen, ship, aliens, bullets):
    """检查和相应子弹是否击中（碰撞）外群组中的外星人个体"""
    # 若是，删除相应的子弹和外星人（暂定一颗子弹对应一个外星人，见groupcollide 参数）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 外星人编组为空（被消灭），删除现有子弹，新建外星人群
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(setting, screen, ship, aliens)

def fire_bullets(setting, screen, ship, bullets):
    """若未达到限制，则发射"""
    if len(bullets) < setting.bullets_allowed:
        new_bullet = Bullet(setting, screen, ship)
        bullets.add(new_bullet)
def get_number_aliens_x(setting, alien_width):
    # 一行能容纳的个数
    # 屏幕左右留出等宽
    available_space_x = setting.screen_width - 2 * alien_width
    # 单个间隔等宽
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(setting, screen, aliens, alien_index, row_number):
    # 创建单个，加入当前行
    alien = Alien(setting, screen)
    alien_width = alien.rect.width
    # 更新逻辑位置（小数），rect位置（整数）
    alien.x = alien_width + 2 * alien_width * alien_index
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(setting, screen, ship, aliens):
    # 创建一个实例
    alien = Alien(setting, screen)
    # 每行容纳多少个
    number_aliens_x = get_number_aliens_x(setting, alien.rect.width)
    number_rows = get_number_rows(setting, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_index in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(setting, screen, aliens, alien_number, row_index)

def get_number_rows(setting, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = setting.screen_height - 3*alien_height - ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def check_fleet_edges(setting, aliens):
    """外星人群（其中任意一个外星人）到达边缘时采取措施规"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(setting, aliens)
            break

def change_fleet_direction(setting, aliens):
    """整群外星人下移，改变其方向"""
    for alien in aliens.sprites():
        alien.rect.y += setting.fleet_drop_speed
    setting.fleet_direction *= -1
def update_aliens(setting, ship, aliens):
    """当有外星人到达屏幕边缘，更新编组中所有外星人的位置"""
    check_fleet_edges(setting, aliens)
    aliens.update()

    # 监测外星人和飞船是否碰撞
    if pygame.sprite.spritecollideany(ship, aliens): # 无碰撞会返回None
        print("Ship hit!!!")

def ship_hit(setting, stats, screen, ship, aliens, bullets):
    pass # 继续code
def update_screen(setting, screen, ship, aliens, bullets):
    """更新屏幕图像，切换到新屏幕"""
    # 每次循环，背景色填充重绘屏幕
    screen.fill(setting.bg_color)
    # 飞船和外星人前重绘所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    # 编组调用父类继承的draw，自动在屏幕上绘制每个元素，按照元素rect位置
    aliens.draw(screen)
    # 使最近绘制的屏幕可见：每次执行，擦除旧屏幕，显示新屏幕
    pygame.display.flip()

