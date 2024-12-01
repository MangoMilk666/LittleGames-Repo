# 以下为GPT修改版本：
import sys
import pygame
from Platform import Platform
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

# ------------ Third Layer---------------------
def check_events(doodler):
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
                doodler.jumpAgain()

def create_platforms(setting, camera, doodler, screen, platforms):
    """创建平台群"""
    while len(platforms) < 7:
        platform = Platform(doodler, setting, screen, camera, category="green")
        platforms.add(platform)

def lowest_platform_position(platforms):
    pass

def collide_condition(doodler, platform):
    return doodler.rect.bottom >= platform.rect.top + 20 and \
        doodler.rect.centerx >= platform.rect.left and \
        doodler.rect.centerx <= platform.rect.right

def update_platforms(setting, screen, camera, doodler, platforms):
    """检测小人是否跳上平台，并更新"""
    create_platforms(setting, camera, doodler, screen, platforms)
    # 小人落下状态且至少有一个平台碰撞
    if not doodler.jumping and pygame.sprite.spritecollideany(doodler, platforms, collide_condition):
        doodler.jumpAgain()

    # 处理不同平台碰撞逻辑时使用
    # any_collided_platform = pygame.sprite.spritecollide(doodler, platforms, False, collide_condition):
    # if not doodler.jumping and any_collided_platform:
    #     doodler.jumpAgain()

    for platform in platforms.copy():
        if platform.rect.top >= setting.screen_height:
            platforms.remove(platform)


def update_camera(camera, doodler, platforms):
    # 跟随小人位置，更新摄像机位置
    camera.update(doodler)
    for platform in platforms:
        camera.apply(platform.rect)


def update_screen(settings, screen, stats, doodler, platforms, button):
     # Redraw screen each frame
     screen.fill(settings.bg_color)

     # Draw doodler and platform(s)
     doodler.blitme()
     platforms.draw(screen)

     # 若游戏处于非活动状态，就绘制（Play）按钮
     # 先绘制其他元素，再绘制button，为了使按钮处于最上方
     if not stats.game_active:
         button.draw_button()
     pygame.display.flip()
