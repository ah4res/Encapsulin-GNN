# Implementation Status

## Module

FeatureContact

（実装名: `CountInteractionWithNCSchain`）

実装パス: `structure_tools/PDB_analysis/CountInteractionWithNCSchain/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`

---

## Purpose

Reference Chain A の各残基について、近傍 NCS partner chain との
Cα距離帯別接触数・最短距離を特徴量化する。

ADR-016 / ADR-017 に従い、サブユニット間相互作用はエッジではなく
ノード特徴量として保持し、partner chain 情報を合算せず残す。

入力は `PDB-GrepSubunits/results_<PDBID>/neighbor_cluster.pdb`。
SEQRES 取得用 mmCIF は FeaturesDSSP `data/<PDB>.cif` を参照。

ADR-022 により参照残基 Node = SEQRES（missing 含む）。
missing 残基の接触量は計算不可のため NaN。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- neighbor_cluster.pdb 自動探索
- Cαのみによる距離計算（ATOM / polymer）
- 距離帯別累積接触数（2 / 4 / 6 / 8 / 10 Å）
- partner chain 別レコード保持（`partner_chain` 列）
- ADR-022: SEQRES 参照残基への展開、`is_missing` / `missing_segment_length`
- Missing 残基の距離・接触カウント = NaN（partner 行は維持）
- `contact_features.csv` / `contact_features_summary.csv` 生成（3構造）
- `seqres_nodes.csv` 生成
- `summary.txt` 生成
- 可視化（heatmap / distance / profile / histogram / top residues / contribution / missing overlay）
- CLI（`count_interaction_with_ncs_chain.py`）と Notebook

確認 PDB: 3DKT / 7S21 / 9B9I
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

実測参照ノード数: 3DKT 265、7S21 301、9B9I 281
特徴量行数: 1855 / 3010 / 2248（ADR022 after と一致）

---

## In Progress

- なし（単体モジュールとしてのコア実装は完了）

---

## Not Implemented

- Atlas / Dataset A・B 向け batch 一括実行 CLI
- 対称軸分類（2-fold / 3-fold / 5-fold）へのマッピング
- GNN 入力形式への統合（MergeFeatures 依存）
- Contact–PISA partner 集合の整合ルール実装
- モジュール専用 README.md
- ADR 命名ディレクトリ（`FeatureContact/`）への配置・同期

---

## Outputs

生成確認済み（3DKT / 7S21 / 9B9I）:

- `contact_features.csv`
  （列に is_missing, missing_segment_length を含む）
- `contact_features_summary.csv`
- `seqres_nodes.csv`
- `summary.txt`
- `plots/contact_heatmap.png`
- `plots/minimum_distance_heatmap.png`
- `plots/total_contact_profile.png`
- `plots/distance_histogram.png`
- `plots/top_contact_residues.png`
- `plots/partner_chain_contribution.png`
- `plots/Figure_missing_overlay.png`

---

## Validation Status

- ADR-017 要求の partner 列保持を CSV で確認
- 距離帯列（n_2A … n_10A）および `normalized_n_10A` を確認
- ADR-022: ノード数・missing 数が期待値と一致（3構造）
- Contact partner 数と PISA partner 数が一致しない
  （例: 3DKT Contact B–H vs PISA B–F；7S21 / 9B9I でも Contact 側が広い）
- 対称軸別再分類や学習前集約の妥当性検証は未実施

関連 Result: Result-005（近傍サブユニット・局所グラフ）。Result-007（SEQRES 移行根拠）。
ADR-022 移行後比較: `ADR022_before_after_comparison.csv`（正式 Result 番号は未採番）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016 / ADR-017（局所グラフ、相互作用はノード特徴）
- ADR-018（独立 Feature モジュール）
- ADR-022（SEQRES Node、missing 特徴量）

---

## Known Issues

- Contact と PISA の partner 集合不一致（Contact ⊃ PISA の傾向）
- GrepSubunits / FeaturesDSSP mmCIF への依存
- MergeFeatures 未着手
- Edge-Features は ATOM ベースのまま（ノード長不一致）

---

## Next Actions

High

- Contact–PISA partner 整合ルールを ADR / 設計として固定
- MergeFeatures での SEQRES 主キー結合

Medium

- 対称軸分類マッピング
- モジュール README / ADR 命名同期

Low

- batch CLI

---

## Completion Estimate

Design: 90%

Implementation: 90%

Validation: 80%

Overall: 85%

---

### Current_State Summary

- FeatureContact は ADR-022 対応済み（SEQRES 参照ノード、missing=NaN、3構造再計算済み）。
- partner 列保持は継続；PISA との partner 集合不一致は未解消。
- MergeFeatures 未着手が学習統合のブロッカー。
- Current_State では Contact を Mostly Complete（SEQRES 移行済）と扱う。
