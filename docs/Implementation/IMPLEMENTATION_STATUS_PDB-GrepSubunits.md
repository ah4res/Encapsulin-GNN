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
FeatureContact（CountInteractionWithNCSchain）および FeaturePISA（FeaturesPISA）は
本モジュールの出力 `neighbor_cluster.pdb` に依存する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- gemmi による PDB/mmCIF 読込・Biological Assembly 展開（`assembly_loader.py`）
- 全 chain の残基数・重心計算（`subunit_parser.py`）
- Chain A と同一残基数の候補抽出（`--same-length-only`、既定 ON）
- 重心間距離計算・昇順ソート
- 最短原子間距離計算（`distance_calculator.py`）
- cutoff（既定 10 Å）による近傍サブユニット判定
- `neighbor_cluster.pdb` 出力（Chain A + 近傍サブユニット）
- Chain ID対応表（`neighbor_cluster_chain_map.csv`）・接触距離表
  （`neighbor_cluster_contacts.csv`）出力
- PyMOL 用 `.pml` スクリプトおよび確認用 PNG 生成（`export_view.py`）
- 距離散布図 + 重心3D可視化（`neighbor_overview.png`）
- CLI（`scripts/grep_neighbor_subunits.py`）
  （`--chain` / `--cutoff` / `--same-length-only` / `--out` / `--assembly-index` /
  `--force-download` / `--no-png` / `--pymol-bin` 等のオプション対応）
- Notebook（`notebooks/analyze_3DKT_neighbors.ipynb`）
- モジュール化（`src/pipeline.py` 等、CLI/Notebook 双方から再利用可能）

確認 PDB: 3DKT / 7S21 / 9B9I
判定基準: CSV・PDB・PNG の実生成まで確認できたもののみ Completed

---

## In Progress

- なし（単体モジュールとしてのコア実装は完了）

---

## Not Implemented

- Dataset A/B（Atlas全体）向け batch 一括実行
- Result-002 で指摘された Caspar-Klug 例外（多層粒子）・Icosahedral 判定誤検出への
  対応を踏まえた cutoff / same-length-only ヒューリスティックの体系的再検証
- 自動リグレッションテスト
- モジュール専用の Implementation Status 以外の検証 Result
  （現状は Result-005 が唯一の関連 Result）

---

## Outputs

生成確認済み（3DKT / 7S21 / 9B9I、`results_<PDBID>/` 配下）:

- `chain_info.csv`
- `candidate_subunits.csv`
- `centroid_distance.csv`
- `atom_distance.csv`
- `neighbor_subunits.csv`
- `neighbor_cluster.pdb`（必須出力、約1〜1.4MB）
- `neighbor_cluster.pml`
- `neighbor_cluster_chain_map.csv`
- `neighbor_cluster_contacts.csv`
- `neighbor_overview.png`
- `neighbor_cluster_chainA.png`

---

## Validation Status

- 3構造（3DKT / 7S21 / 9B9I）で全出力ファイルの生成を確認
- `neighbor_cluster.pdb` は FeatureContact / FeaturePISA の入力として
  実際に消費され、両モジュールの CSV 生成に繋がっていることを確認
  （下流モジュールの Outputs 生成が本モジュールの間接的な動作検証となっている）
- Result-005（3DKT近傍サブユニット抽出による局所グラフ検討）が
  本モジュールの妥当性検討に relates するが、
  Result-005 の Related ADR 欄は「ADR-015」（HPC）と記載されており、
  内容的には ADR-016 との対応が想定される（Current_State既知の不整合）
- cutoff = 10 Å・same-length-only=ON という Phase 1 ヒューリスティックの
  体系的な精度検証（Caspar-Klug 例外構造等での妥当性）は未実施

関連 Result: Result-005（近傍サブユニット抽出・局所グラフ検討）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016（Reference Chain A を中心とした局所グラフ表現。本モジュールが
  その入力データ生成を担う）

---

## Known Issues

- PyMOL 実行ファイルへの依存（`--pymol-bin`、PNG生成に必要）。
  未導入環境での挙動は本調査で確認していない
- cutoff / same-length-only の既定値は Phase 1 の仮ヒューリスティックであり、
  Result-002 が指摘した Icosahedral 判定誤検出・Caspar-Klug 例外との
  相互作用が未評価
- Result-005 の Related ADR 参照（ADR-015）が内容と一致していない可能性
  （本モジュール側での修正対象ではなく docs 側の課題）
- FeatureContact と FeaturePISA で本モジュール出力からの partner chain 集合が
  異なる例がある（3DKT: Contact側 B–H, PISA側 B–F）。原因は下流側の
  抽出条件差の可能性が高いが、本モジュール側の出力自体に揺らぎがないか
  未検証

---

## Next Actions

High

- Dataset A（T=1 Encapsulin）確定後、対象 PDB リストに対する batch 実行経路を用意する
- FeatureContact/FeaturePISA 間の partner chain 集合不一致の原因が
  本モジュール側にあるかを切り分ける

Medium

- Result-002 の Caspar-Klug 例外・誤検出構造を用いた cutoff / same-length-only
  ヒューリスティックの再検証

Low

- CLI の自動テスト（smoke test）追加
- PyMOL 未導入環境でのフォールバック挙動の明文化

---

## Completion Estimate

Design: 100%

Implementation: 90%

Validation: 70%

Overall: 85%

---

### Current_State Summary

- PDB-GrepSubunits は Mostly Complete。FeatureContact / FeaturePISA の
  共通上流入力（neighbor_cluster.pdb）として実際に機能している。
- 3構造（3DKT / 7S21 / 9B9I）で CSV・PDB・PNG 一式の生成を確認済み。
- cutoff / same-length-only ヒューリスティックは Result-002 の
  Caspar-Klug 例外・誤検出構造で未検証。
- Dataset A/B 確定後の batch 実行経路は未整備。
- Result-005 の Related ADR 参照不整合（ADR-015 vs 想定ADR-016）は
  docs 側の既知課題として残る。
