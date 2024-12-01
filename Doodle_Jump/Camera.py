import pygame

class Camera:
    def __init__(self, settings):
        self.settings = settings
        self.y_offset = 0  # Tracks the vertical offset of the camera
        self.max_speed = 10

    def update(self, target):
        # Reset y_offset at the beginning of each update
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
        # if target.rect.bottom < self.settings.screen_height // 3:
        #     self.y_offset = min(0, self.y_offset + (self.settings.screen_height // 3 - target.rect.bottom))
        # elif target.rect.top > self.settings.screen_height // 3 * 2:
        #     self.y_offset = max(-self.max_speed,
        #                         self.y_offset + (self.settings.screen_height // 3 * 2 - target.rect.top))
        pass

    def apply(self, target_rect):
        # Apply the camera's offset to the **target rectangle**
        target_rect.centery += self.y_offset
