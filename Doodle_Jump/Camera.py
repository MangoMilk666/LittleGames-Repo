import pygame

class Camera:
    def __init__(self, settings):
        self.settings = settings
        self.y_offset = 0  # Tracks the vertical offset of the camera
        self.max_speed = 5
        self.upHeight = 0

    def update(self, target, stats):
        # Adjust offset if the Doodler moves above or below 1/3 of the screen height
        # if target.rect.bottom < self.settings.screen_height // 3:
        #     single_offset = self.settings.screen_height // 3 - target.rect.top #正的
        #     self.y_offset += min(single_offset, self.max_speed)
        #     target.rect.bottom = self.settings.screen_height // 3 # Reset Doodler's position
        # elif target.rect.bottom > self.settings.screen_height // 3 * 2:
        #     single_offset = self.settings.screen_height // 3 * 2 - target.rect.top # 负的
        #     self.y_offset += max(single_offset, -self.max_speed)
        #     target.rect.bottom = self.settings.screen_height // 3 * 2

        # Adjust y_offset based on the doodler's position
        if target.rect.bottom < self.settings.screen_height // 3:
            self.y_offset = min(self.max_speed, self.y_offset + (self.settings.screen_height // 3 - target.rect.bottom))
        elif target.rect.top > self.settings.screen_height // 3 * 2:
            self.y_offset = max(-self.max_speed,
                                self.y_offset + (self.settings.screen_height // 3 * 2 - target.rect.top))
            if target.rect.top >= self.settings.screen_height // 4 * 3 and target.fastFall:
                target.rect.top = self.settings.screen_height // 4 * 3
                self.y_offset += (-5*self.max_speed - self.settings.gravity) # 如何表示加速下落的逻辑？

        # pass

    def apply(self, target):
        # Apply the camera's offset to the target rectangle
        """target: platform"""
        # 黄色升降平台还要继续移动
        target.rect.centery += self.y_offset
        if target.category == "yellow" and target.state == "moving":
            if target.vertical_move == 1: # shift downward delta H > 0
                if self.y_offset >= 0: # 小人向上，平台总体向下
                    target.rect.centery += self.settings.yellow_platform_vertical_relative_speed
                elif self.y_offset < 0: # 小人向下，平台总体向上
                    target.rect.centery += self.settings.yellow_platform_vertical_relative_speed

            elif target.vertical_move == -1: #shift upward, delta H < 0
                if self.y_offset >= 0: # 小人向上，平台总体向下
                    target.rect.centery += (-1)*(self.settings.yellow_platform_vertical_relative_speed)
                elif self.y_offset < 0: # 小人向下，平台总体向上
                    target.rect.centery += (-1)*(self.settings.yellow_platform_vertical_relative_speed)


    def apply_to_position(self, positionY):
        positionY += self.y_offset
    def get_upwardHeight(self):
        if self.y_offset >= 0: #小人向上，平台下移
            self.upHeight += abs(self.y_offset)
        else:                  #小人向下，平台上移
            self.upHeight -= abs(self.y_offset)
            if self.upHeight <= 0:
                self.upHeight = 0
        return self.upHeight

