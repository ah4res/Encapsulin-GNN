# Implementation Status

## Module

Edge-Features

（Scope (b): ADR-018 Feature 例示名ではなく、実装ディレクトリ名を ModuleName とする）

実装パス: `structure_tools/PDB_analysis/Edge-Features/`

---

## Purpose

ADR-021 に従い、Reference Chain A 内部の残基間エッジを
Cα距離閾値で定義し、エッジ特徴量を抽出する。

特徴量:

- `actual_distance`
- `sequence_distance`
- `ss_pair`
- `same_ss_element`

`ss_pair` は Result-008 で採用された HELO 拡張
（HH / EE / LL / HE / HL / EL / HO / EO / LO / OO）を実装する。
正規化は Edge-Features 内のみ（FeaturesDSSP の8状態出力は変更しない）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- RCSB 構造取得 → Chain A 抽出 → mkdssp
- エッジ定義: Cα–Cα < threshold（初期値 8 Å、CLI 可変）
- `actual_distance` / `sequence_distance` / `ss_pair` / `same_ss_element`
- HELO 正規化: H→H、E→E、coil（blank/`-`）→L、T/S/G/I/B 等→O
- `edge_features.csv` / `summary.json` / `ss_pair_same_element_summary.csv`
- 可視化 Figure1–6（距離・配列距離・散布図・ss_pair・contact map・same_ss_element）
- threshold アブレーション用 validation 出力（4 / 6 / 8 / 10 Å）
- CLI（`edge_features.py`）、README、Notebook、validation スクリプト

確認 PDB: 3DKT / 7S21 / 9B9I（threshold=8 Å）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

実測（8 Å）: 3DKT 264 nodes / 1233 edges；7S21 265 / 1209；9B9I 262 / 1197
O 系ペア出現例（3DKT）: HO 75、EO 121、LO 122、OO 112（Result-008 と一致）

---

## In Progress

- なし（単体コアは完了）。ADR-021 本文の HEL 表記と HELO 実装の文書整合は Result-008 側で採用済

---

## Not Implemented

- ADR-022 SEQRES Node への移行（現状は ATOM/DSSP 可能な残基のみ；missing はグラフから除外）
- `is_missing` / `missing_segment_length` のエッジ側付与
- MergeFeatures との統合
- Dataset A への系統適用
- Threshold の学習性能に基づく最終最適化
- RBF 距離展開（ADR-021 Deferred）

---

## Outputs

生成確認済み（3DKT / 7S21 / 9B9I）:

- `edge_features.csv`
  （列: pdb_id, chain, res_i, res_j, actual_distance, sequence_distance, ss_pair, same_ss_element）
- `summary.json`（ss_pair_counts に HO/EO/LO/OO を含む）
- `ss_pair_same_element_summary.csv`
- `plots/Figure1_edge_distance_histogram.png`
- `plots/Figure2_sequence_distance_histogram.png`
- `plots/Figure3_distance_vs_sequence_distance.png`
- `plots/Figure4_ss_pair_distribution.png`
- `plots/Figure5_contact_map.png`
- `plots/Figure6_ss_pair_same_element_distribution.png`

validation/: `threshold_edge_counts*.csv`、`results_*_thr{4,6,8,10}/`、same_ss_element 集計

---

## Validation Status

- Result-008: エッジ設計妥当、HELO 拡張を採用仕様として記録
- threshold 4/6/8/10 Å でエッジ数単調増加を確認（Result-008 表と整合）
- same_ss_element: HH は同一要素内優位、EE は要素間接触が多い（Result-008）
- O カテゴリは無視できない頻度（Result-008 HELO Extension Validation）
- ADR-021 原文の ss_pair 列挙は HEL 6種のまま；正式採用は Result-008 Conclusion（HELO 10種）
- ADR-022 未対応のため FeatureDSSP 等の SEQRES ノード長と不一致

関連 Result: Result-008（Edge / HELO 検証）。Result-005（局所グラフ文脈）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016（局所グラフ・Chain A）
- ADR-021（エッジ定義・特徴量）
- ADR-022（未実装: SEQRES Node 整合）

---

## Known Issues

- Node = ATOM（Cα+DSSP あり）のまま。FeatureDSSP/Contact/PISA（SEQRES）とノード集合が不一致
  （例: 7S21 Edge 265 vs Feature 301）
- L/O 残基は要素 ID なし → `same_ss_element` が情報を持つのは主に HH / EE
- ADR-021 本文と Result-008 / 実装の HELO 表記差（正本優先: ADR 更新が望ましい）
- MergeFeatures 未着手

---

## Next Actions

High

- HELO を ADR-021 本文へ正式反映（Result-008 Next Action）
- ADR-022: Edge Node を SEQRES に揃える設計・実装

Medium

- Dataset A 適用
- MergeFeatures との node–edge 整列

Low

- Threshold 最適化、RBF 展開

---

## Completion Estimate

Design: 90%

Implementation: 85%

Validation: 90%

Overall: 85%

---

### Current_State Summary

- Edge-Features は ADR-021 コア＋HELO ss_pair 実装済み（3構造、Result-008 と整合）。
- FeaturesDSSP の出力は変更していない（Edge 内正規化のみ）。
- 未対応の主課題は ADR-022 SEQRES Node 整合と Merge 統合。
- Current_State では Edge を Mostly Complete、ただし Feature 側 SEQRES 長との不一致を明記する。
