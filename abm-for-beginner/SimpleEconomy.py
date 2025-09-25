import random
import numpy as np
import matplotlib.pyplot as plt
from Household import Household
from Firm import Firm
from Market import Market

class SimpleEconomy:
    """シンプルな経済システム"""

    def __init__(self, num_households=20, num_firms=5):
        self.households = [Household(i) for i in range(num_households)]
        self.firms = [Firm(i) for i in range(num_firms)]
        self.market = Market()
        self.time = 0

        # 統計データ保存用
        self.history = {
            'time': [],
            'total_consumption': [],
            'average_price': [],
            'total_profit': [],
            'employment_rate': []
        }

    def run_simulation(self, periods=50):
        """シミュレーション実行"""
        print("シミュレーション開始...")

        for t in range(periods):
            self.time = t
            print(f"\n=== 期間 {t+1} ===")

            # 1. 企業が労働者を雇用
            for firm in self.firms:
                firm.hire_workers(self.households)

            # 2. 家計が労働
            for household in self.households:
                household.work()

            # 3. 企業が価格設定と生産
            for firm in self.firms:
                firm.set_price()
                firm.produce()

            # 4. 家計が消費
            avg_price = sum([f.price for f in self.firms]) / len(self.firms)
            for household in self.households:
                household.consume(avg_price)

            # 5. 市場清算
            traded_quantity = self.market.clear_market(self.households, self.firms)

            # 6. 統計の記録
            self.record_statistics()

            # 7. 現在の状態を表示
            if t % 10 == 0:  # 10期間ごとに表示
                self.print_status()

        print("\nシミュレーション完了!")
        return self.history

    def record_statistics(self):
        """統計データを記録"""
        total_consumption = sum([h.consumption for h in self.households])
        total_profit = sum([f.profit for f in self.firms])
        employed = sum([1 for h in self.households if h.employed])
        employment_rate = employed / len(self.households)

        self.history['time'].append(self.time)
        self.history['total_consumption'].append(total_consumption)
        self.history['average_price'].append(self.market.average_price)
        self.history['total_profit'].append(total_profit)
        self.history['employment_rate'].append(employment_rate)

    def print_status(self):
        """現在の経済状況を表示"""
        employed = sum([1 for h in self.households if h.employed])
        avg_money = sum([h.money for h in self.households]) / len(self.households)
        total_profit = sum([f.profit for f in self.firms])

        print(f"雇用者数: {employed}/{len(self.households)}")
        print(f"平均資産: {avg_money:.2f}")
        print(f"総利益: {total_profit:.2f}")
        print(f"平均価格: {self.market.average_price:.2f}")

    def plot_results(self):
        """結果をグラフで表示"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Simple ABM Simulation Results', fontsize=16)

        # 消費の推移
        axes[0, 0].plot(self.history['time'], self.history['total_consumption'])
        axes[0, 0].set_title('Total Consumption')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Consumption')

        # 価格の推移
        axes[0, 1].plot(self.history['time'], self.history['average_price'])
        axes[0, 1].set_title('Average Price')
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Price')

        # 利益の推移
        axes[1, 0].plot(self.history['time'], self.history['total_profit'])
        axes[1, 0].set_title('Total Profit')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Profit')

        # 雇用率の推移
        axes[1, 1].plot(self.history['time'], self.history['employment_rate'])
        axes[1, 1].set_title('Employment Rate')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Employment Rate')

        plt.tight_layout()
        plt.show()