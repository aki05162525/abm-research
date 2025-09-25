# -*- coding: utf-8 -*-
"""
レストラン労働力ABMモデル
Restaurant Labor ABMシミュレーションのメインモデル
"""
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from worker_agent import WorkerAgent
from company_agent import CompanyAgent

class RestaurantLaborModel:
    """レストラン労働力ABMのメインモデル"""

    def __init__(self, num_workers=3600, num_companies=100):
        """
        モデルの初期化

        Args:
            num_workers (int): 労働者エージェント数
            num_companies (int): 企業エージェント数
        """
        self.num_workers = num_workers
        self.num_companies = num_companies
        self.time = 0

        # エージェントの生成
        self.workers = self._create_workers()
        self.companies = self._create_companies()

        # 統計データ保存用
        self.history = {
            'time': [],
            'employment_rate': [],
            'average_wage': [],
            'total_profit': [],
            'job_matching_rate': [],
            'turnover_rate': []
        }

        # 応募者選定パラメータ
        self.daily_applicants = max(1, int(num_workers / 360))  # 1日あたりの新規応募者数

    def _create_workers(self):
        """労働者エージェントの生成"""
        workers = []
        # タイプ別の分布
        type_weights = [(30, "freeter"), (37, "student"), (24, "housewife"), (9, "foreigner")]

        for i in range(self.num_workers):
            worker_type = self._weighted_choice(type_weights)
            worker = WorkerAgent(i, worker_type)
            workers.append(worker)

        return workers

    def _create_companies(self):
        """企業エージェントの生成"""
        companies = []
        for i in range(self.num_companies):
            company = CompanyAgent(i)
            companies.append(company)
        return companies

    def _weighted_choice(self, weights):
        """重み付き選択"""
        total = sum(weight for weight, _ in weights)
        r = random.uniform(0, total)
        upto = 0
        for weight, choice in weights:
            if upto + weight >= r:
                return choice
            upto += weight
        return weights[-1][1]

    def step(self):
        """1ステップの実行"""
        self.time += 1

        # 1. 新規応募者の選定とマッチング
        self._select_applicants_and_match()

        # 2. 全労働者のステップ実行
        for worker in self.workers:
            worker.step()

        # 3. 全企業のステップ実行
        for company in self.companies:
            company.step()

        # 4. 統計情報の記録
        self._record_statistics()

    def _select_applicants_and_match(self):
        """応募者選定とマッチング処理"""
        # 新規応募者の選定（未就職者から）
        unemployed = [w for w in self.workers if w.state == "未就職"]
        if len(unemployed) > self.daily_applicants:
            new_applicants = random.sample(unemployed, self.daily_applicants)
        else:
            new_applicants = unemployed[:]

        # 求職中の労働者も応募候補に追加
        job_seekers = [w for w in self.workers
                      if w.state == "求職中" and w.elapsed_days > 1]

        all_applicants = new_applicants + job_seekers

        # マッチング処理
        for worker in all_applicants:
            self._match_worker_to_company(worker)

    def _match_worker_to_company(self, worker):
        """労働者と企業のマッチング"""
        # 応募可能な企業を検索
        candidate_companies = []

        for company in self.companies:
            # 採用枠に余裕があるか
            if not company.can_accept_applicant():
                continue

            # スキルレベルが適合するか
            if worker.level - 1 <= company.level:
                candidate_companies.append(company)

        # マッチングする企業がある場合
        if candidate_companies:
            # ランダムに企業を選択
            chosen_company = random.choice(candidate_companies)
            chosen_company.accept_applicant(worker)
            worker.apply_to_company(chosen_company)

    def _record_statistics(self):
        """統計情報の記録"""
        # 雇用率
        employed = sum(1 for w in self.workers if w.state == "就職中")
        employment_rate = employed / len(self.workers)

        # 平均賃金（雇用されている労働者の）
        employed_workers = [w for w in self.workers if w.state == "就職中"]
        if employed_workers:
            total_wage = sum(w.company.wages[w.company.level] for w in employed_workers)
            average_wage = total_wage / len(employed_workers)
        else:
            average_wage = 0

        # 総利益
        total_profit = sum(c.profit for c in self.companies)

        # マッチング率（求人枠の充足率）
        total_positions = sum(c.frame for c in self.companies)
        filled_positions = sum(len(c.employees) for c in self.companies)
        job_matching_rate = filled_positions / total_positions if total_positions > 0 else 0

        # 離職率（概算）
        total_workers_employed = sum(len(c.employees) for c in self.companies)
        if total_workers_employed > 0:
            # 簡易的な離職率計算
            turnover_rate = 0.05  # プレースホルダー
        else:
            turnover_rate = 0

        # 履歴に記録
        self.history['time'].append(self.time)
        self.history['employment_rate'].append(employment_rate)
        self.history['average_wage'].append(average_wage)
        self.history['total_profit'].append(total_profit)
        self.history['job_matching_rate'].append(job_matching_rate)
        self.history['turnover_rate'].append(turnover_rate)

    def run_simulation(self, periods=360):
        """シミュレーションの実行"""
        print("レストラン労働力ABMシミュレーション開始...")
        print(f"労働者: {self.num_workers}人, 企業: {self.num_companies}社")
        print(f"実行期間: {periods}日")

        for t in range(periods):
            self.step()

            # 定期的な進捗表示
            if (t + 1) % 60 == 0:
                self._print_status()

        print("\nシミュレーション完了!")
        return self.history

    def _print_status(self):
        """現在の状況を表示"""
        employed = sum(1 for w in self.workers if w.state == "就職中")
        unemployed = sum(1 for w in self.workers if w.state == "未就職")
        job_seeking = sum(1 for w in self.workers if w.state == "求職中")
        waiting = sum(1 for w in self.workers if w.state == "結果待ち")

        print(f"\n=== 期間 {self.time} ===")
        print(f"就職中: {employed}, 未就職: {unemployed}, 求職中: {job_seeking}, 結果待ち: {waiting}")
        print(f"雇用率: {employed/len(self.workers)*100:.1f}%")

        total_profit = sum(c.profit for c in self.companies)
        print(f"企業総利益: {total_profit:,.0f}円")

    def plot_results(self):
        """結果をグラフで表示"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Restaurant Labor ABM Simulation Results', fontsize=16)

        # 雇用率の推移
        axes[0, 0].plot(self.history['time'], self.history['employment_rate'])
        axes[0, 0].set_title('Employment Rate')
        axes[0, 0].set_xlabel('Time (Days)')
        axes[0, 0].set_ylabel('Employment Rate')
        axes[0, 0].grid(True)

        # 平均賃金の推移
        axes[0, 1].plot(self.history['time'], self.history['average_wage'])
        axes[0, 1].set_title('Average Wage')
        axes[0, 1].set_xlabel('Time (Days)')
        axes[0, 1].set_ylabel('Wage (Yen/hour)')
        axes[0, 1].grid(True)

        # 総利益の推移
        axes[0, 2].plot(self.history['time'], self.history['total_profit'])
        axes[0, 2].set_title('Total Profit')
        axes[0, 2].set_xlabel('Time (Days)')
        axes[0, 2].set_ylabel('Profit (Yen)')
        axes[0, 2].grid(True)

        # マッチング率の推移
        axes[1, 0].plot(self.history['time'], self.history['job_matching_rate'])
        axes[1, 0].set_title('Job Matching Rate')
        axes[1, 0].set_xlabel('Time (Days)')
        axes[1, 0].set_ylabel('Matching Rate')
        axes[1, 0].grid(True)

        # 労働者タイプ別分布
        type_counts = defaultdict(int)
        for worker in self.workers:
            type_counts[worker.type] += 1

        axes[1, 1].bar(type_counts.keys(), type_counts.values())
        axes[1, 1].set_title('Worker Type Distribution')
        axes[1, 1].set_xlabel('Worker Type')
        axes[1, 1].set_ylabel('Count')

        # 企業レベル別分布
        level_counts = defaultdict(int)
        for company in self.companies:
            level_counts[company.level] += 1

        axes[1, 2].bar(level_counts.keys(), level_counts.values())
        axes[1, 2].set_title('Company Level Distribution')
        axes[1, 2].set_xlabel('Company Level')
        axes[1, 2].set_ylabel('Count')

        plt.tight_layout()
        plt.show()

    def get_summary_statistics(self):
        """サマリー統計の取得"""
        if not self.history['time']:
            return {}

        return {
            'final_employment_rate': self.history['employment_rate'][-1],
            'final_average_wage': self.history['average_wage'][-1],
            'final_total_profit': self.history['total_profit'][-1],
            'final_job_matching_rate': self.history['job_matching_rate'][-1],
            'max_employment_rate': max(self.history['employment_rate']),
            'min_employment_rate': min(self.history['employment_rate']),
            'simulation_periods': len(self.history['time'])
        }