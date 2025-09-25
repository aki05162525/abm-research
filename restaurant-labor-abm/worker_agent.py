# -*- coding: utf-8 -*-
"""
労働者エージェント
Restaurant Labor ABMシミュレーションの労働者エージェント実装
"""
import random

class WorkerAgent:
    """労働者エージェント - 求職・就職活動を行う"""

    def __init__(self, agent_id, worker_type):
        """
        労働者エージェントの初期化

        Args:
            agent_id (int): エージェントの一意識別子
            worker_type (str): 労働者タイプ（freeter, student, housewife, foreigner）
        """
        self.id = agent_id
        self.type = worker_type

        # タイプに応じたレベル（スキル）設定
        if self.type == "freeter":
            self.level = random.randint(2, 6)
        elif self.type == "student":
            self.level = random.randint(3, 5)
        elif self.type == "housewife":
            self.level = random.randint(2, 5)
        elif self.type == "foreigner":
            self.level = random.randint(1, 3)
        else:
            self.level = 3  # デフォルト

        # 状態変数
        self.state = "未就職"  # 未就職, 求職中, 結果待ち, 就職中, 情報収集中
        self.company = None   # 勤務先企業
        self.elapsed_days = 0 # 離職/求職日数
        self.work_days = 0    # 就職日数
        self.wait_days = 0    # 採用通知待ち日数

        # 位置（5x5格子上の位置）
        self.x = random.randint(0, 4)
        self.y = random.randint(0, 4)

    def step(self):
        """労働者の1ステップの行動"""
        # 就職中で30日経過ごとに離職判定
        if (self.state == "就職中" and
            self.work_days > 0 and
            self.work_days % 30 == 0):

            turnover_rate = self.get_turnover_rate()
            if random.random() < turnover_rate:
                self.quit_job()

        # 情報収集期間が1日経過したら求職開始
        if self.state == "情報収集中" and self.elapsed_days == 1:
            self.state = "求職中"

        # 日数の更新
        if self.state != "就職中":
            self.elapsed_days += 1
        else:
            self.work_days += 1

        # 採用通知待ち
        if self.wait_days > 0:
            self.wait_days -= 1

    def get_turnover_rate(self):
        """離職率を取得"""
        turnover_rates = {
            "freeter": {30: 0.05, 60: 0.04, 90: 0.04, 120: 0.03, 150: 0.02,
                       180: 0.02, 210: 0.03, 240: 0.03, 270: 0.03, 300: 0.03,
                       330: 0.03, 360: 0.03},
            "student": {30: 0.13, 60: 0.06, 90: 0.05, 120: 0.05, 150: 0.05,
                       180: 0.05, 210: 0.05, 240: 0.04, 270: 0.04, 300: 0.04,
                       330: 0.04, 360: 0.04},
            "housewife": {30: 0.03, 60: 0.02, 90: 0.02, 120: 0.02, 150: 0.02,
                         180: 0.02, 210: 0.02, 240: 0.02, 270: 0.02, 300: 0.02,
                         330: 0.02, 360: 0.02},
            "foreigner": {30: 0.10, 60: 0.05, 90: 0.05, 120: 0.04, 150: 0.03,
                         180: 0.02, 210: 0.02, 240: 0.02, 270: 0.01, 300: 0.01,
                         330: 0.01, 360: 0.01}
        }

        if self.type in turnover_rates:
            return turnover_rates[self.type].get(self.work_days, 0.01)
        return 0.01

    def quit_job(self):
        """離職処理"""
        self.state = "情報収集中"
        self.work_days = 0
        if self.company:
            self.company.remove_employee(self)
            self.company = None
        self.wait_days = 0
        self.elapsed_days = 0

    def apply_to_company(self, company):
        """企業への応募"""
        self.state = "結果待ち"
        self.company = company
        self.wait_days = random.randint(1, 7)  # 1-7日で通知
        self.elapsed_days = 0

    def get_hired(self, company):
        """採用された場合の処理"""
        self.state = "就職中"
        self.company = company
        self.work_days = 0
        self.elapsed_days = 0
        self.wait_days = 0

    def get_rejected(self):
        """不採用の場合の処理"""
        self.state = "情報収集中"
        self.company = None
        self.elapsed_days = 0
        self.wait_days = 0

    def __str__(self):
        """エージェントの状態を文字列で表現"""
        return (f"Worker {self.id}: Type={self.type}, Level={self.level}, "
                f"State={self.state}, WorkDays={self.work_days}, "
                f"Position=({self.x},{self.y})")