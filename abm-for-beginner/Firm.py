import random
import numpy as np

class Firm:
    """企業エージェント - 生産と価格設定を行う"""

    def __init__(self, firm_id):
        self.id = firm_id
        self.price = 5.0  # 商品価格
        self.production = 50.0  # 生産量
        self.profit = 0.0  # 利益
        self.employees = []  # 従業員リスト

    def set_price(self):
        """価格設定 - ランダムに±10%変動"""
        price_change = random.uniform(-0.1, 0.1)
        self.price = max(1.0, self.price * (1 + price_change))

    def produce(self):
        """生産 - 従業員数に基づいて生産量を決定"""
        self.production = len(self.employees) * 10 #1人あたり10単位

    def hire_workers(self, households):
        """労働者を雇用（失業者を優先して最大10人まで）"""
        self.employees = []
        # 失業者を候補にする（employed == False）
        available_workers = [h for h in households if not h.employed]
        # 候補が少なければ既に雇用されている人も検討するなら、available_workers.extend(...)
        hired = random.sample(available_workers, min(6000, len(available_workers)))
        # フラグを更新（hired のみ employed=True、それ以外は False）
        for household in households:
            household.employed = household in hired
        self.employees = hired

    def calculate_profit(self, total_sales):
        """利益計算"""
        revenue = total_sales * self.price
        wage_costs = len(self.employees) * 10
        self.profit = revenue - wage_costs

    def __str__(self):
        return f"Firm {self.id}: Price={self.price:.2f}, Production={self.production:.2f}, Profit={self.profit:.2f}"