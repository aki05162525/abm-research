class Household:
    """
    家計エージェント - 消費と労働供給を行う
    
    このクラスは、経済システムにおける家計（消費者）の行動をモデル化します。
    家計は以下の経済活動を行います：
    1. 消費：商品を購入して効用を得る
    2. 労働：賃金を得て所得を増やす
    """

    def __init__(self, agent_id):
        """
        家計エージェントの初期化
        
        Args:
            agent_id (int): エージェントの一意識別子
        """
        self.id = agent_id              # エージェントID（識別用）
        self.money = 100.0              # 初期資産（貨幣残高）
        self.consumption = 0.0          # 前回の消費量（財の数量）
        self.wage = 10.0                # 時間当たり賃金率
        self.employed = True            # 雇用状態（True=雇用, False=失業）

    def consume(self, price):
        """
        消費行動 - 資産の一部を消費に使う
        
        経済学的解釈：
        - 家計は限られた予算制約の下で消費を決定
        - ここでは単純化して、資産の70%を消費予算とする
        - 実際の経済では、所得・価格・選好によって消費が決まる
        
        Args:
            price (float): 商品の単価
            
        Returns:
            float: 消費した商品の数量
        """
        if self.money > 0:
            # 予算制約：資産の70%を消費予算として設定
            consumption_budget = self.money * 0.7
            
            # 需要関数：予算 ÷ 価格 = 購入可能数量
            self.consumption = consumption_budget / price
            
            # 資産から消費額を差し引く（会計処理）
            self.money -= consumption_budget
            
        return self.consumption

    def work(self):
        """
        労働行動 - 雇用されていれば賃金を得る
        
        経済学的解釈：
        - 労働市場において労働供給を行う
        - 雇用状態の場合のみ賃金所得を獲得
        - 実際の経済では労働時間や労働強度も考慮される
        """
        if self.employed:
            # 労働所得の獲得（1期間の労働に対する賃金）
            self.money += self.wage
            
    def update_employment(self, is_employed):
        """
        雇用状態の更新
        
        Args:
            is_employed (bool): 新しい雇用状態
        """
        self.employed = is_employed

    def __str__(self):
        """
        エージェントの現在状態を文字列で表現
        デバッグやログ出力に使用
        """
        return (f"Household {self.id}: "
                f"Money={self.money:.2f}, "
                f"Consumption={self.consumption:.2f}, "
                f"Employed={self.employed}")