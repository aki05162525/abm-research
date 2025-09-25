#!/usr/bin/env python3
"""
Simple ABM Demo Runner
シンプルABMのデモ実行スクリプト

このスクリプトは、simple_abm.pyを使って基本的なABMを実行します。
初学者がABMの概念を理解するためのものです。
"""

from SimpleEconomy import SimpleEconomy
from Household import Household  
from Firm import Firm

def basic_demo():
    """基本的なデモンストレーション"""
    print("=== 基本的なABMデモ ===\n")

    # 1. エージェントを作成
    print("1. エージェントの作成")
    households = [Household(i) for i in range(3)]  # 3世帯
    firms = [Firm(i) for i in range(2)]  # 2企業

    print("初期状態:")
    for h in households:
        print(f"  {h}")
    for f in firms:
        print(f"  {f}")

    # 2. 1期間だけのシミュレーション
    print("\n2. 1期間のシミュレーション")

    # 企業が労働者を雇用
    for firm in firms:
        firm.hire_workers(households)

    # 家計が労働
    for household in households:
        household.work()

    # 企業が生産
    for firm in firms:
        firm.set_price()
        firm.produce()

    # 家計が消費
    avg_price = sum([f.price for f in firms]) / len(firms)
    for household in households:
        household.consume(avg_price)

    # 市場清算
    market = Market()
    traded_quantity = market.clear_market(households, firms)

    print("1期間後の状態:")
    for h in households:
        print(f"  {h}")
    for f in firms:
        print(f"  {f}")
    print(f"  取引量: {traded_quantity:.2f}")
    print(f"  平均価格: {market.average_price:.2f}")


def full_simulation_demo():
    """完全なシミュレーションのデモ"""
    print("\n\n=== 完全シミュレーションデモ ===")
    print("家計5世帯、企業2社で20期間のシミュレーション\n")

    # 小規模な経済システムを作成
    economy = SimpleEconomy(num_households=5, num_firms=2)

    # 20期間のシミュレーション
    history = economy.run_simulation(periods=20)

    print("\n結果サマリー:")
    print(f"最終総消費: {history['total_consumption'][-1]:.2f}")
    print(f"最終平均価格: {history['average_price'][-1]:.2f}")
    print(f"最終雇用率: {history['employment_rate'][-1]:.2f}")


def interactive_demo():
    """インタラクティブデモ"""
    print("\n\n=== インタラクティブデモ ===")
    print("パラメータを変更してシミュレーションを実行できます")

    try:
        households_num = int(input("家計数を入力してください (デフォルト: 10): ") or "10")
        firms_num = int(input("企業数を入力してください (デフォルト: 3): ") or "3")
        periods = int(input("シミュレーション期間を入力してください (デフォルト: 30): ") or "30")

        print(f"\n家計{households_num}世帯、企業{firms_num}社で{periods}期間のシミュレーション開始...")

        economy = SimpleEconomy(num_households=households_num, num_firms=firms_num)
        history = economy.run_simulation(periods=periods)

        print("\nシミュレーション結果:")
        print(f"最終総消費: {history['total_consumption'][-1]:.2f}")
        print(f"最終平均価格: {history['average_price'][-1]:.2f}")
        print(f"最終雇用率: {history['employment_rate'][-1]:.2f}")

        # グラフ表示の確認
        show_graph = input("\nグラフを表示しますか？ (y/n): ").lower() == 'y'
        if show_graph:
            try:
                economy.plot_results()
            except ImportError:
                print("matplotlib がインストールされていないため、グラフは表示できません。")

    except KeyboardInterrupt:
        print("\n\n中断されました。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


def explain_concepts():
    """ABMの概念説明"""
    print("\n=== ABM (Agent-Based Model) の基本概念 ===")
    print("""
エージェントベースモデル（ABM）とは：
- 個々のエージェント（家計、企業など）の行動をモデル化
- エージェント間の相互作用から全体の経済現象が創発
- 複雑な経済システムを理解するためのシミュレーション手法

このシンプルモデルの構成要素：

1. Household（家計）エージェント：
   - 労働して賃金を得る
   - 資産を使って消費する
   - 雇用状態が変化する

2. Firm（企業）エージェント：
   - 労働者を雇用する
   - 商品を生産する
   - 価格を設定する
   - 利益を計算する

3. Market（市場）：
   - 需要と供給を調整
   - 取引量を決定
   - 価格形成

4. Economy（経済システム）：
   - 全体の調整役
   - シミュレーションの進行
   - 統計の記録

BaselineModelとの違い：
- BaselineModel: 金融機関、政府、中央銀行などを含む複雑なモデル
- このモデル: 家計と企業のみの最小構成

学習のポイント：
- まずはシンプルなモデルで基本概念を理解
- 徐々に複雑な要素を追加していく
- シミュレーション結果から経済の動きを観察
""")


def main():
    """メイン関数"""
    print("Simple ABM Learning Tool")
    print("シンプルABM学習ツール")
    print("=" * 50)

    while True:
        print("\n選択してください:")
        print("1. 基本デモ（1期間だけの動作）")
        print("2. 完全シミュレーション（20期間）")
        print("3. インタラクティブデモ（パラメータ指定）")
        print("4. ABMの概念説明")
        print("5. 終了")

        try:
            choice = input("\n選択 (1-5): ").strip()

            if choice == "1":
                basic_demo()
            elif choice == "2":
                full_simulation_demo()
            elif choice == "3":
                interactive_demo()
            elif choice == "4":
                explain_concepts()
            elif choice == "5":
                print("終了します。")
                break
            else:
                print("1-5の数字を入力してください。")

        except KeyboardInterrupt:
            print("\n\n終了します。")
            break
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

        input("\nEnterキーを押して続行...")


if __name__ == "__main__":
    main()