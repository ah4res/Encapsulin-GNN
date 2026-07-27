# Roadmap B: Dry Research

## B1 Dataset Construction

目的

解析対象となる構造データセット構築

成果物

- Encapsulin構造一覧
- 文献一覧
- メタデータ

主な対象

- T=1 Encapsulin
- PDB登録構造
- 関連論文情報

完了条件

- 解析対象構造の決定

---

## B2 Structure Feature Engineering

目的

粒子形成関連物理量の定量化

候補特徴量

- buried surface area
- hydrophobic interaction
- electrostatic interaction
- local curvature
- structural distortion

成果物

- Feature extraction pipeline

完了条件

- 全構造から特徴量抽出可能

---

## B3 Graph Representation Design

目的

GNN入力表現の設計

主要判断

- ノード定義
- エッジ定義
- 属性定義

成果物

- Graph Builder

完了条件

- 全構造のグラフ化

---

## B4 Baseline GNN Analysis

目的

ベースラインモデル構築

候補

- GCN
- GAT

成果物

- 学習パイプライン
- 評価パイプライン

完了条件

- ベースライン性能取得

---

## B5 Advanced GNN Analysis

目的

高性能モデルの検討

候補

- Graph Transformer
- Attention系モデル

成果物

- 高精度モデル
- Feature importance解析

完了条件

- 重要残基ランキング取得

---

## B6 AI-driven Hypothesis Generation

目的

実験検証候補抽出

成果物

- 重要残基候補
- 界面候補
- 変異候補一覧

完了条件

- Wet検証対象決定
