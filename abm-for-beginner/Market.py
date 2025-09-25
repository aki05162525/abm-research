import random
import numpy as np


class Market:
    """市場 - 取引の場"""

    def __init__(self):
        self.total_demand = 0.0
        self.total_supply = 0.0
        self.average_price = 0.0

    def clear_market(self, households, firms):
        """市場清算 - 需要と供給を調整"""
        # 需要の計算
        total_demand = sum([h.consumption for h in households])

        # 供給の計算
        total_supply = sum([f.production for f in firms])

        # 平均価格の計算
        if len(firms) > 0:
            self.average_price = sum([f.price for f in firms]) / len(firms)

        # 実際の取引量（需要と供給の最小値）
        traded_quantity = min(total_demand, total_supply)

        # 各企業の売上を計算
        if total_supply > 0:
            for firm in firms:
                firm_sales = (firm.production / total_supply) * traded_quantity
                firm.calculate_profit(firm_sales)

        self.total_demand = total_demand
        self.total_supply = total_supply

        return traded_quantity
