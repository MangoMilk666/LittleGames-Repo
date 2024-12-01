class GameStats:
    def __init__(self, settings):
        self.setting = settings
        self.reset_stats()
        # 让游戏一开始处于非活动状态
        self.game_active = False

    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        # 统计上升的高度
        self.height = 0
