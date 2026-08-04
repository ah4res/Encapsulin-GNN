# Implementation Status

## Module

PDB-GrepSubunits

実装パス: `structure_tools/PDB_analysis/PDB-GrepSubunits/`

ADR-018 の Feature 抽出モジュール例示（FeatureContact 等）には属さないが、
FeatureContact / FeaturePISA の共通上流入力（`neighbor_cluster.pdb`）を
生成する前処理パイプラインである。

---

## Purpose

Biological Assembly 内で Reference Chain A と直接相互作用する可能性の高い
サブユニット群（近傍サブユニット）を抽出する。

ADR-016（局所グラフ表現）の入力データを構築する役割を持ち、
DatasetPreparation（ADR-025）では GrepSubunits として PISA/Contact の前提になる。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- PDB ID → CIF 取得 → Biological Assembly 展開
- 同長シェルサブユニット候補抽出・距離計算
- `neighbor_cluster.pdb` / `.pml` / chain map / contacts CSV
- `neighbor_overview.png`
- CLI（`scripts/grep_neighbor_subunits.py`）と prototype Notebook
- DatasetPreparation 経由の batch（`--no-png` オプション対応、`done.flag`）

確認 PDB: gold_T1-enc 由来 **41 構造**
（全 results_* に `neighbor_cluster.pdb` + overview PNG + done.flag）
判定基準: CSV・画像・summary 相当（overview）・主要 PDB 出力の実生成

代表サンプル（3DKT/7S21/9B9I）は `_chainA.png` を含むフルセット。
他 PDB は overview あり・`_chainA.png` なし（`--no-png` batch 由来）でも完備扱い。

---

## In Progress

- なし（コア前処理としての役割は完了）

---

## Not Implemented

- residue graph / PyG 変換（README「次段階」）
- 専用 tests/
- Contact–PISA partner 不一致の原因切り分け（Grep 抽出条件 vs 下流フィルタ）

---

## Outputs

生成確認済み（41 PDB）:

- `neighbor_cluster.pdb`（必須上流入力）
- `neighbor_subunits.csv` / `chain_info.csv` / `atom_distance.csv` 等
- `neighbor_overview.png`
- `done.flag`
- （一部）`neighbor_cluster_chainA.png`

`results/`（単数）は空。集約 CSV なし。

---

## Validation Status

- Result-005（3DKT 近傍抽出・局所グラフ検討）と役割が整合
- gold_T1-enc 41 全件で neighbor_cluster.pdb 生成を確認
- Contact/PISA の入力として DatasetPreparation 依存関係が機能

正式な GrepSubunits 専用 Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016（局所グラフ入力）
- ADR-019（`neighbor_cluster.pdb` 概念）
- ADR-025（GrepSubunits 実行順・依存）

---

## Known Issues

- Contact ⊃ PISA の partner 集合差の一因候補（全 non-A CA vs interface）
- singular `results/` が空で運用上未使用
- `_chainA.png` が batch では省略される

---

## Next Actions

High

- Contact–PISA partner 不一致の原因切り分け（Grep vs 下流）

Medium

- Dataset A 確定後の再バッチ方針整理

Low

- residue graph / PyG 変換（必要なら GraphBuilder 側で充足）

---

## Completion Estimate

Design: 90%

Implementation: 95%

Validation: 80%

Overall: 90%

---

### Current_State Summary

- PDB-GrepSubunits は gold_T1-enc 41 構造すべてで neighbor_cluster.pdb を生成済み。
- FeatureContact / FeaturePISA / DatasetPreparation の共通上流として安定稼働。
- partner 不一致の切り分けが残課題。
