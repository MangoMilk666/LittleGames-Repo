class GameStats:
    """用于统计游戏信息"""

    def __init__(self, settings):
        self.setting = settings
        self.reset_stats()

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        self.ships_left = self.setting.ship_limit

