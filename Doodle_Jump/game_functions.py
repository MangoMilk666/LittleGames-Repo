import random as rd
import sys
import time

import pygame
from Platform import Platform

# --------------------------------first layer------------------------------
def check_keydown_events(event, doodler):
    if event.key == pygame.K_RIGHT:
        doodler.moving_right = True
    elif event.key == pygame.K_LEFT:
        doodler.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()



def check_keyup_events(event, doodler):
    if event.key == pygame.K_RIGHT:
        doodler.moving_right = False
    elif event.key == pygame.K_LEFT:
        doodler.moving_left = False
def show_splash_screen(setting, screen):
    """点击PLAY后，游戏开始前倒计时屏幕"""
    start_time = pygame.time.get_ticks()  # Get the starting time
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # Time in seconds

        # Render splash screen
        screen.fill(setting.bg_color_black)
        text = setting.screen_font.render("Get Ready!", True, setting.color_white)
        countdown = setting.screen_font.render(f"{1 - int(elapsed_time)}", True, setting.color_white)  # Countdown timer
        screen.blit(text, (setting.screen_width // 2 - text.get_width() // 2, setting.screen_height // 2 - 100))
        screen.blit(countdown, (setting.screen_width // 2 - countdown.get_width() // 2, setting.screen_height // 2))

        pygame.display.flip()

        # Wait for 3 seconds
        if elapsed_time >= 1:
            break
def show_gameOver_screen(setting, screen):
    """小人落地后，游戏结束界面"""
    start_time = pygame.time.get_ticks()  # Get the starting time
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # Time in seconds

        # Render splash screen
        screen.fill(setting.bg_color_black)
        text = setting.screen_font.render("Game Over", True, setting.color_white)
        screen.blit(text, (setting.screen_width // 2 - text.get_width() // 2, setting.screen_height // 2 - 100))

        pygame.display.flip()

        if elapsed_time >= 1:
            break

# -----------------------------second layer------------------------------
def check_play_button(setting, camera, screen, stats, button, doodler, platforms, mouse_x, mouse_y):
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
        # 倒计时屏幕
        show_splash_screen(setting, screen)
        # 正式开始
        stats.game_active = True

        # 清空平台列表
        platforms.empty()



        # 创建新的平台群，飞船居中
        create_platforms(setting, camera, doodler, screen, platforms)

def check_doodler_platform_collisions(setting, screen, stats, sb, doodler, platforms):
    """检查doodler是否碰撞平台群组中的platform对象"""
    # # 若是，删除相应的子弹和外星人（暂定一颗子弹对应一个外星人，见groupcollide 参数）
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #
    # if collisions: # 返回的字典不为空 --> 子弹有打中外星人
    #     # 字典的key:与外星人碰撞的子弹, value:与子弹碰撞的外星人列表
    #     for Aliens in collisions.values():
    #         stats.score += setting.alien_points * len(Aliens)
    #         sb.prep_score() # 即时将变化的分数渲染成图像显示
    pass

def platforms_move(platform, camera):
    if platform.category == "yellow":
        camera.apply_to_position(platform.initial_y)
    platform.update()


# ------------ Third Layer---------------------
def check_events(setting, camera, screen, stats, button, doodler, platforms):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, doodler)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, doodler)
        elif event.type == pygame.USEREVENT:
            # 小人在地面而且没起跳，那么允许其再度起跳
            if not doodler.jumping and doodler.rect.bottom >= doodler.screen_rect.bottom:
                if stats.maxHeight - stats.height < 600 and stats.height > 0:
                    doodler.jumpAgain()
                elif stats.maxHeight - stats.height >= 600 and stats.height > 0:
                    doodler.fastFall = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # 返回点击时鼠标的(x, y)
            check_play_button(setting, camera, screen, stats, button, doodler, platforms, mouse_x, mouse_y)

def create_platforms(setting, camera, doodler, screen, platforms):
    """创建平台群"""
    while len(platforms) < 10:
        category_dict = {0:"green", 1:"broken", 2:"trampoline", 3:"blue", 4:"yellow", 5:"spring"}
        category_index = rd.randint(0, 5)
        platform = Platform(doodler, setting, screen, camera, category=category_dict.get(category_index))
        platforms.add(platform)





def get_lowest_platformPosition(platforms):
    lowest_bottom = 0
    if len(platforms) > 0:
        for platform in platforms:
            if platform.rect.bottom > lowest_bottom:  # 位置比既定的最低点还低
                lowest_bottom = platform.rect.bottom
    return lowest_bottom


def collide_condition(doodler, platform):
    return doodler.rect.bottom >= platform.rect.top and \
        doodler.rect.centerx >= platform.rect.left and \
        doodler.rect.centerx <= platform.rect.right and \
        doodler.rect.bottom <= platform.rect.bottom

def update_platforms(setting, screen, camera, doodler, platforms):
    """检测小人是否跳上平台，并更新"""
    create_platforms(setting, camera, doodler, screen, platforms)

    # 小人落下状态且至少有一个平台碰撞
    collided_platform = pygame.sprite.spritecollideany(doodler, platforms, collide_condition)
    if not doodler.jumping and collided_platform:
        doodler.jumpAgain(collided_platform.category)

    # 处理不同平台碰撞逻辑时使用
    # any_collided_platform = pygame.sprite.spritecollide(doodler, platforms, False, collide_condition):
    # if not doodler.jumping and any_collided_platform:
    #     doodler.jumpAgain()

    for platform in platforms.copy():
        platforms_move(platform, camera)
        if platform.rect.top >= setting.screen_height + 250:
            platforms.remove(platform)
        elif platform.rect.bottom < -150:
            platforms.remove(platform)


def update_camera(camera, stats, doodler, platforms):
    # 跟随小人位置，更新摄像机位置
    camera.update(doodler,stats)
    for platform in platforms:
        camera.apply(platform)
    # ----以下代码转移至update_scoreboard()-----
    # stats.height = camera.get_upwardHeight()
    # sb.prep_height()
    #camera.y_offset = 0


def update_scoreboard(camera, sb, stats):
    stats.height = camera.get_upwardHeight()
    sb.prep_height()
    if stats.height > stats.maxHeight:
        stats.maxHeight = stats.height
    delta_height = stats.height - stats.maxHeight



def update_screen(settings, screen, stats, camera, sb, doodler, platforms, button):
     # Redraw screen each frame
     screen.fill(settings.bg_color_grey)

     # Draw doodler and platform(s)
     doodler.blitme()
     platforms.draw(screen)

     # 显示高度
     sb.show_height()

     # 若游戏处于非活动状态，就绘制（Play）按钮
     # 先绘制其他元素，再绘制button，为了使按钮处于最上方
     if not stats.game_active:
         button.draw_button()

     if doodler.fastFall and camera.get_upwardHeight() == 0:
         show_gameOver_screen(settings, screen)

     pygame.display.flip()
