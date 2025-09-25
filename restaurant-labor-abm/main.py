# -*- coding: utf-8 -*-
"""
Restaurant Labor ABM メイン実行ファイル
レストラン労働力ABMシミュレーションのメイン実行スクリプト
"""
import random
import numpy as np
from restaurant_labor_model import RestaurantLaborModel

def main():
    """メイン実行関数"""
    print("=== Restaurant Labor Agent-Based Model ===")
    print("レストラン労働力エージェントベースモデル")
    print("=" * 50)

    # ランダムシードの設定（再現性のため）
    random.seed(42)
    np.random.seed(42)

    # モデルの作成
    # 実際の研究では労働者3600人、企業約100社だが、テスト用に小さくする
    model = RestaurantLaborModel(
        num_workers=360,    # 労働者数（元: 3600）
        num_companies=10    # 企業数（元: 約100）
    )

    # シミュレーション実行（1年間 = 360日）
    history = model.run_simulation(periods=120)

    # 結果の表示
    print("\n" + "=" * 50)
    print("シミュレーション結果")
    print("=" * 50)

    stats = model.get_summary_statistics()
    print(f"最終雇用率: {stats['final_employment_rate']*100:.1f}%")
    print(f"最終平均賃金: {stats['final_average_wage']:.0f}円/時")
    print(f"最終企業総利益: {stats['final_total_profit']:,.0f}円")
    print(f"最終求人充足率: {stats['final_job_matching_rate']*100:.1f}%")
    print(f"最高雇用率: {stats['max_employment_rate']*100:.1f}%")
    print(f"最低雇用率: {stats['min_employment_rate']*100:.1f}%")

    # グラフ表示の確認
    show_graph = input("\nグラフを表示しますか？ (y/n): ").lower()
    if show_graph == 'y':
        try:
            model.plot_results()
        except ImportError:
            print("matplotlibがインストールされていないため、グラフは表示できません。")
        except Exception as e:
            print(f"グラフ表示でエラーが発生しました: {e}")

    return model, history

def demo_mode():
    """デモモード - より小規模なシミュレーション"""
    print("=== デモモード ===")
    print("小規模シミュレーション（労働者50人、企業5社、30日間）")

    # より小さなモデルでのテスト
    model = RestaurantLaborModel(num_workers=50, num_companies=5)

    # 短期間実行
    history = model.run_simulation(periods=30)

    # 簡易結果表示
    stats = model.get_summary_statistics()
    print(f"\nデモ結果:")
    print(f"雇用率: {stats['final_employment_rate']*100:.1f}%")
    print(f"求人充足率: {stats['final_job_matching_rate']*100:.1f}%")

    return model, history

def interactive_mode():
    """インタラクティブモード"""
    print("=== インタラクティブモード ===")

    try:
        # パラメータの入力
        num_workers = int(input("労働者数を入力してください (デフォルト: 100): ") or "100")
        num_companies = int(input("企業数を入力してください (デフォルト: 5): ") or "5")
        periods = int(input("シミュレーション期間（日）を入力してください (デフォルト: 60): ") or "60")

        print(f"\n労働者{num_workers}人、企業{num_companies}社で{periods}日間のシミュレーションを開始...")

        # モデル実行
        model = RestaurantLaborModel(num_workers=num_workers, num_companies=num_companies)
        history = model.run_simulation(periods=periods)

        # 結果表示
        stats = model.get_summary_statistics()
        print(f"\n結果:")
        print(f"最終雇用率: {stats['final_employment_rate']*100:.1f}%")
        print(f"最終平均賃金: {stats['final_average_wage']:.0f}円/時")
        print(f"最終企業総利益: {stats['final_total_profit']:,.0f}円")

        return model, history

    except ValueError:
        print("無効な入力です。デフォルト設定で実行します。")
        return demo_mode()
    except KeyboardInterrupt:
        print("\n中断されました。")
        return None, None

if __name__ == "__main__":
    print("Restaurant Labor ABM Simulator")
    print("選択してください:")
    print("1. 標準実行")
    print("2. デモモード（小規模・高速）")
    print("3. インタラクティブモード（パラメータ指定）")

    try:
        choice = input("選択 (1-3): ").strip()

        if choice == "1":
            model, history = main()
        elif choice == "2":
            model, history = demo_mode()
        elif choice == "3":
            model, history = interactive_mode()
        else:
            print("デフォルトでデモモードを実行します。")
            model, history = demo_mode()

    except KeyboardInterrupt:
        print("\n\nプログラムが中断されました。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()