# ABM Code Reading Guide

## エージェントベースモデル（ABM）コード読解ガイド

このガイドでは、本プロジェクトの具体的なコードを例に、ABMのコード読解方法を説明します。

## 1. プロジェクト構造の理解

### ファイル構成
```
abm-for-beginner/
├── Household.py          # 家計エージェント
├── Firm.py              # 企業エージェント
├── Market.py            # 市場クラス
├── SimpleEconomy.py     # 経済システム全体
├── main.py              # メイン実行ファイル
└── run_simple_demo.py   # デモ実行スクリプト
```

### エージェントの種類
- **Household（家計）**: 消費と労働を行う経済主体
- **Firm（企業）**: 生産と価格設定を行う経済主体
- **Market（市場）**: 需要と供給を調整する仕組み
- **SimpleEconomy（経済システム）**: 全体を統括する環境

## 2. コード読解の実践例

### ステップ1: エージェントクラスの理解

#### 家計エージェント（Household.py:11-23）
```python
def __init__(self, agent_id):
    self.id = agent_id              # エージェントID
    self.money = 100.0              # 初期資産（貨幣残高）
    self.consumption = 0.0          # 前回の消費量
    self.wage = 10.0                # 時間当たり賃金率
    self.employed = True            # 雇用状態
```

**読解ポイント:**
- 各エージェントが持つ**状態変数**に注目
- `money`, `consumption`, `employed`などが時間とともに変化
- 初期値の設定が全体の挙動に影響

#### 企業エージェント（Firm.py:7-13）
```python
def __init__(self, firm_id):
    self.id = firm_id
    self.price = 5.0                # 商品価格
    self.production = 50.0          # 生産量
    self.profit = 0.0               # 利益
    self.employees = []             # 従業員リスト
```

**読解ポイント:**
- 企業の**意思決定変数**（価格、生産量）
- 他エージェント（従業員）との**関係性**を保持

### ステップ2: エージェントの行動ルール

#### 家計の消費行動（Household.py:24-49）
```python
def consume(self, price):
    if self.money > 0:
        # 予算制約：資産の70%を消費予算として設定
        consumption_budget = self.money * 0.7

        # 需要関数：予算 ÷ 価格 = 購入可能数量
        self.consumption = consumption_budget / price

        # 資産から消費額を差し引く
        self.money -= consumption_budget

    return self.consumption
```

**読解ポイント:**
- **予算制約**（資産の70%）という経済学的概念
- 価格に応じた**需要関数**の実装
- **会計処理**（資産から消費額を減算）

#### 企業の価格設定（Firm.py:14-17）
```python
def set_price(self):
    """価格設定 - ランダムに±10%変動"""
    price_change = random.uniform(-0.1, 0.1)
    self.price = max(1.0, self.price * (1 + price_change))
```

**読解ポイント:**
- **確率的意思決定**（ランダムな価格変動）
- **制約条件**（最低価格1.0の設定）

### ステップ3: エージェント間の相互作用

#### 雇用関係（Firm.py:23-33）
```python
def hire_workers(self, households):
    """労働者を雇用（失業者を優先して最大10人まで）"""
    self.employees = []
    # 失業者を候補にする
    available_workers = [h for h in households if not h.employed]
    # 最大10人まで雇用
    hired = random.sample(available_workers, min(10, len(available_workers)))
    # 雇用状態を更新
    for household in households:
        household.employed = household in hired
    self.employees = hired
```

**読解ポイント:**
- エージェント間の**選択メカニズム**
- **状態の更新**（雇用フラグの変更）
- **制約条件**（最大雇用数）

### ステップ4: 市場メカニズム

#### 市場清算（Market.py:13-37）
```python
def clear_market(self, households, firms):
    """市場清算 - 需要と供給を調整"""
    # 需要の計算
    total_demand = sum([h.consumption for h in households])

    # 供給の計算
    total_supply = sum([f.production for f in firms])

    # 実際の取引量（需要と供給の最小値）
    traded_quantity = min(total_demand, total_supply)

    # 各企業の売上を計算
    if total_supply > 0:
        for firm in firms:
            firm_sales = (firm.production / total_supply) * traded_quantity
            firm.calculate_profit(firm_sales)
```

**読解ポイント:**
- **集計メカニズム**（需要・供給の合計）
- **市場清算条件**（取引量は需要と供給の最小値）
- **売上配分**（生産量に比例して売上を分配）

### ステップ5: シミュレーション実行

#### メインループ（SimpleEconomy.py:26-63）
```python
def run_simulation(self, periods=50):
    for t in range(periods):
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
```

**読解ポイント:**
- **時系列の構造**（期間ごとのループ）
- **実行順序**の重要性（雇用→労働→生産→消費→市場清算）
- **データ収集**のタイミング

## 3. このコードベース特有のパターン

### パラメータ設定
- **家計初期資産**: 100.0（Household.py:19）
- **賃金率**: 10.0（Household.py:21）
- **消費性向**: 0.7（Household.py:41）
- **労働生産性**: 10単位/人（Firm.py:21）

### 確率的要素
- **価格変動**: ±10%のランダム変動（Firm.py:16）
- **雇用選択**: ランダムサンプリング（Firm.py:29）

### 制約条件
- **最低価格**: 1.0（Firm.py:17）
- **最大雇用数**: 10人（Firm.py:29）

## 4. コード読解のチェックリスト

### エージェントの状態
- [ ] 初期値は何か？
- [ ] どの変数が時間とともに変化するか？
- [ ] 状態の更新はいつ行われるか？

### 行動ルール
- [ ] 決定的か確率的か？
- [ ] どんな制約条件があるか？
- [ ] 他エージェントの情報を使うか？

### 相互作用
- [ ] どのエージェント間で相互作用があるか？
- [ ] 相互作用のタイミングは？
- [ ] 情報の流れはどうなっているか？

### 時間構造
- [ ] 実行順序は適切か？
- [ ] 同期/非同期どちらか？
- [ ] データ収集のタイミングは？

## 5. デバッグとテスト方法

### 実行方法
```bash
# 基本実行
python main.py

# デモ実行（段階的理解）
python run_simple_demo.py
```

### 状態確認
各クラスの`__str__`メソッドでエージェント状態を確認:
```python
print(household)  # → "Household 0: Money=85.00, Consumption=10.50, Employed=True"
print(firm)       # → "Firm 0: Price=5.25, Production=50.00, Profit=125.50"
```

### パラメータ実験
- **初期資産**を変更して消費行動の変化を観察
- **雇用人数**を変更して生産量への影響を確認
- **シミュレーション期間**を変更して収束性を検証

## 6. 学習の進め方

### 段階的理解
1. **run_simple_demo.py**で1期間だけの動作を確認
2. **main.py**で長期間の動的変化を観察
3. パラメータを変更して感度分析

### 拡張のヒント
- 新しいエージェント属性の追加
- 異なる行動ルールの実装
- 追加の制約条件や市場メカニズム

## まとめ

このコードベースは、ABMの基本概念を実装した教育的なサンプルです。単純化された経済システムですが、エージェントベース・モデリングの核心的な要素（個別エージェントの行動、相互作用、創発現象）を含んでいます。

コード読解の際は、まず全体の構造を把握し、次に個別エージェントの行動ルール、そしてエージェント間の相互作用に注目することが重要です。