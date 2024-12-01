import sys
import pygame
from Bullet import Bullet
from Alien import Alien
from time import sleep
# ----------------------first layer-------------------------------

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

def change_fleet_direction(setting, aliens):
    """整群外星人下移，改变其方向"""
    for alien in aliens.sprites():
        alien.rect.y += setting.fleet_drop_speed
    setting.fleet_direction *= -1

# ----------------------------------------second layer------------------------------
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

def check_bullet_alien_collisions(setting, screen, stats, sb, ship, aliens, bullets):
    """检查和相应子弹是否击中（碰撞）外群组中的外星人个体"""
    # 若是，删除相应的子弹和外星人（暂定一颗子弹对应一个外星人，见groupcollide 参数）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions: # 返回的字典不为空 --> 子弹有打中外星人
        """遍历字典，确保将每个消灭的外星人的点数都计入得分"""
        # 字典的key:与外星人碰撞的子弹, value:与子弹碰撞的外星人列表
        for Aliens in collisions.values():
            stats.score += setting.alien_points * len(Aliens)
            sb.prep_score() # 即时将变化的分数渲染成图像显示

    # 外星人编组为空（被消灭），删除现有子弹，加快游戏节奏，新建外星人群
    if len(aliens) == 0:
        bullets.empty()
        setting.increase_speed()
        create_fleet(setting, screen, ship, aliens)




def create_alien(setting, screen, aliens, alien_index, row_number):
    # 创建单个，加入当前行
    alien = Alien(setting, screen)
    alien_width = alien.rect.width
    # 更新逻辑位置（小数），rect位置（整数）
    alien.x = alien_width + 2 * alien_width * alien_index
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)



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


def ship_hit(setting, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，飞船放在屏幕底端中央
        create_fleet(setting, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        # 需要点击按钮重新开始时，鼠标光标需要重新显示
        pygame.mouse.set_visible(True)

def check_aliens_bottom(setting, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(setting, stats, screen, ship, aliens, bullets)
            break

def check_play_button(setting, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y):
    """当玩家点击Play按钮时开始新游戏"""
    # 检查点击时鼠标坐标是否在button的rect内
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        setting.initialize_dynamic_settings()
        # 游戏开始后就隐藏鼠标光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建新的外星人群，飞船居中
        create_fleet(setting, screen, ship, aliens)
        ship.center_ship()

# ----------------------------------------final layer-------------------------------

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

''' 监视键盘和鼠标事件的代码，整合：
         '''
def check_events(setting, screen, stats, button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos() # 返回点击时鼠标的(x, y)
            check_play_button(setting, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y)


def update_aliens(setting, stats, screen, ship, aliens, bullets):
    """当有外星人到达屏幕边缘，更新编组中所有外星人的位置"""
    check_fleet_edges(setting, aliens)
    aliens.update()

    # 监测外星人和飞船是否碰撞
    if pygame.sprite.spritecollideany(ship, aliens): # 无碰撞会返回None
        ship_hit(setting, stats, screen, ship, aliens, bullets)

    # 检测是否有外星人到达屏幕底端
    check_aliens_bottom(setting, stats, screen, ship, aliens, bullets)

'''更新子弹数量和位置代码整合到GF类
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        print("Bullets left:", len(bullets))
        '''
def update_bullets(setting, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置
        删除到顶子弹"""
    bullets.update()
    # 通过避免直接修改正在遍历的列表，避免了跳过元素的风险
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 最好定时显示 print("Bullets left:", len(bullets))
    check_bullet_alien_collisions(setting, screen, stats, sb, ship, aliens, bullets)

'''更新屏幕的代码，整合至GF
        每次循环，背景色填充重绘屏幕
        screen.fill(settings.bg_color)
        ship.blitme()
        # 使最近绘制的屏幕可见：每次执行，擦除旧屏幕，显示新屏幕
        pygame.display.flip()
        '''
def update_screen(setting, screen, stats, sb, ship, aliens, bullets, button):
    """更新屏幕图像，切换到新屏幕"""
    # 每次循环，背景色填充重绘屏幕
    screen.fill(setting.bg_color)
    # 飞船和外星人前重绘所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    # 编组调用父类继承的draw，自动在屏幕上绘制每个元素，按照元素rect位置
    aliens.draw(screen)

    # 显示得分
    sb.show_score()
    # 若游戏处于非活动状态，就绘制（Play）按钮
    # 先绘制其他元素，再绘制button，为了使按钮处于最上方
    if not stats.game_active:
        button.draw_button()

    # 使最近绘制的屏幕可见：每次执行，擦除旧屏幕，显示新屏幕
    pygame.display.flip()

