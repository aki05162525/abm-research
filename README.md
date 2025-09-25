# ABM Research Project

このプロジェクトは、エージェントベースモデル（Agent-Based Model）の研究用リポジトリです。

## セットアップ

### 前提条件

- Python 3.12 以上
- Ubuntu/Debian 系の場合：`python3-venv`パッケージ

### 仮想環境の作成と使用方法

#### 1. 仮想環境の作成

```bash
# 仮想環境を作成
python3 -m venv venv
```

Ubuntu/Debian 系でエラーが出る場合は、以下のコマンドで必要なパッケージをインストール：

```bash
sudo apt install python3.12-venv -y
```

#### 2. 仮想環境のアクティベート

```bash
# 仮想環境をアクティベート
source venv/bin/activate
```

アクティベートが成功すると、プロンプトの先頭に `(venv)` が表示されます。

#### 3. パッケージのインストール

```bash
# 例：よく使用されるパッケージのインストール
pip install numpy pandas matplotlib seaborn jupyter
```

#### 4. 仮想環境のデアクティベート

```bash
# 仮想環境を終了
deactivate
```

### プロジェクト構造

```
abm-research/
├── README.md
├── venv/                    # Python仮想環境
└── restaurant-labor-abm/    # レストラン労働ABMプロジェクト
```

## 使用方法

1. このリポジトリをクローン
2. 仮想環境を作成・アクティベート
3. 必要なパッケージをインストール
4. プロジェクトを実行

## 注意事項

- `venv/` フォルダは Git にコミットしないでください（.gitignore に追加推奨）
- 各プロジェクトで必要なパッケージは `requirements.txt` ファイルで管理することを推奨します

## requirements.txt の作成と使用

### パッケージリストの出力

```bash
pip freeze > requirements.txt
```

### パッケージの一括インストール

```bash
pip install -r requirements.txt
```
