# -*- coding: utf-8 -*-
"""
企業エージェント
Restaurant Labor ABMシミュレーションの企業エージェント実装
"""
import random

class CompanyAgent:
    """企業エージェント - 飲食店の経営を行う"""

    def __init__(self, company_id):
        """
        企業エージェントの初期化

        Args:
            company_id (int): 企業の一意識別子
        """
        self.id = company_id

        # レベル（企業グレード）の設定
        level_weights = [(20, 1), (30, 2), (20, 3), (15, 4), (10, 5), (5, 6)]
        self.level = self._weighted_choice(level_weights)

        # 企業規模の設定
        scale_weights = [(50.1, 1), (30.9, 2), (11.7, 3), (7.3, 4)]
        self.scale = self._weighted_choice(scale_weights)

        # 規模に応じた基本設定
        scale_config = {
            1: {"frame": 1, "seats": 20, "member_num": 1},
            2: {"frame": 2, "seats": 50, "member_num": 4},
            3: {"frame": 3, "seats": 100, "member_num": 9},
            4: {"frame": 4, "seats": 150, "member_num": 16}
        }

        config = scale_config.get(self.scale, scale_config[1])
        self.frame = config["frame"]          # 求人枠
        self.seats = config["seats"]          # 席数
        self.member_num = config["member_num"] # 基本従業員数

        # 満席率の設定
        occupancy_weights = [(1, 0.5), (1, 0.6), (1, 0.7), (1, 0.8)]
        self.occupancy = self._weighted_choice(occupancy_weights)

        # 単価の設定
        price_weights = [(1, 1000), (1, 2000), (1, 3000), (1, 4000), (1, 5000)]
        self.price = self._weighted_choice(price_weights)

        # 食材原価（単価の30%）
        self.food_cost = self.price * 0.3

        # 単価に応じた最大稼働回数
        turn_num_config = {
            1000: 12, 2000: 8, 3000: 6, 4000: 4.8, 5000: 4
        }
        self.turn_num_max = turn_num_config.get(self.price, 8)

        # 従業員管理
        self.applicants = []      # 応募者リスト
        self.employees = []       # 採用済み従業員リスト

        # 賃金テーブル
        self.wages = {1: 980, 2: 1080, 3: 1180, 4: 1280, 5: 1380, 6: 1480}

        # 位置（5x5格子上の位置）
        self.x = random.randint(0, 4)
        self.y = random.randint(0, 4)

        # 経営指標
        self.sales = 0.0
        self.costs = 0.0
        self.profit = 0.0

    def _weighted_choice(self, weights):
        """重み付き選択"""
        total = sum(weight for weight, _ in weights)
        r = random.uniform(0, total)
        upto = 0
        for weight, choice in weights:
            if upto + weight >= r:
                return choice
            upto += weight
        return weights[-1][1]  # フォールバック

    def step(self):
        """企業の1ステップの行動"""
        # 応募者の選考
        self._process_applicants()

        # 経営指標の計算
        self._calculate_business_metrics()

    def _process_applicants(self):
        """応募者の選考処理"""
        processed_applicants = []

        for applicant in self.applicants[:]:  # コピーを作ってイテレート
            if applicant.wait_days > 0:
                # まだ待機期間中
                continue

            # 選考実施
            if self.level - 1 <= applicant.level:
                # 採用
                self.employees.append(applicant)
                applicant.get_hired(self)
                self.applicants.remove(applicant)
            else:
                # 不採用
                applicant.get_rejected()
                self.applicants.remove(applicant)

    def _calculate_business_metrics(self):
        """経営指標の計算"""
        # 現在の稼働回数（従業員数に依存）
        current_employees = self.member_num + len(self.employees)
        max_employees = self.member_num + self.frame
        self.turn_num = self.turn_num_max * (current_employees / max_employees)

        # 売上計算
        self.sales = self.seats * self.occupancy * self.turn_num * self.price

        # コスト計算
        # - 食材コスト
        food_costs = self.seats * self.occupancy * self.turn_num * self.food_cost
        # - 人件費（基本従業員 + 採用済み従業員）
        labor_costs = current_employees * self.wages[self.level] * 6
        # - 求人コスト（未充足分 x 3000円）
        recruitment_costs = (self.frame - len(self.employees)) * 3000

        self.costs = food_costs + labor_costs + recruitment_costs

        # 利益計算
        self.profit = self.sales - self.costs

    def can_accept_applicant(self):
        """新規応募者を受け入れ可能か判定"""
        return len(self.applicants) + len(self.employees) < self.frame

    def accept_applicant(self, worker):
        """応募者を受け入れ"""
        if self.can_accept_applicant():
            self.applicants.append(worker)
            return True
        return False

    def remove_employee(self, worker):
        """従業員の削除（離職時）"""
        if worker in self.employees:
            self.employees.remove(worker)

    def get_distance_to(self, worker):
        """労働者との距離を計算（マンハッタン距離）"""
        return abs(self.x - worker.x) + abs(self.y - worker.y)

    def __str__(self):
        """企業の状態を文字列で表現"""
        return (f"Company {self.id}: Level={self.level}, Scale={self.scale}, "
                f"Employees={len(self.employees)}/{self.frame}, "
                f"Applicants={len(self.applicants)}, "
                f"Sales={self.sales:.0f}, Profit={self.profit:.0f}, "
                f"Position=({self.x},{self.y})")