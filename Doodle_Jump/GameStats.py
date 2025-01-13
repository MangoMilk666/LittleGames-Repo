class GameStats:
    def __init__(self, settings):
        self.setting = settings
        self.reset_stats()
        # 让游戏一开始处于非活动状态
        self.game_active = False
        # 三条命的高度/得分记录
        self.height_records = []
        self.highest_height = max(self.height_records) if self.height_records else 0




    def reset_stats(self):
        """初始化游戏期间可能变化的统计信息"""
        # 统计上升的高度及得分
        self.height = 0
        self.score = 0
        self.maxHeight = 0


