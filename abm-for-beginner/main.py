import random
import numpy as np
import matplotlib.pyplot as plt
from SimpleEconomy import SimpleEconomy

def main():
    """メイン関数 - シミュレーションを実行"""
    print("=== Simple Agent-Based Model ===")
    print("シンプルなエージェントベースモデルのデモンストレーション")

    # 経済システムを作成（家計20、企業5）
    economy = SimpleEconomy(num_households=20, num_firms=5)

    # 50期間のシミュレーションを実行
    history = economy.run_simulation(periods=50)

    # 結果をグラフで表示
    economy.plot_results()

    return history


if __name__ == "__main__":
    # ランダムシードを設定（再現可能な結果のため）
    random.seed(42)
    np.random.seed(42)

    history = main()