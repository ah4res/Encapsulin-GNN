# Implementation Status

## Module

FeaturePISA

（実装名: `FeaturesPISA`）

実装パス: `structure_tools/PDB_analysis/FeaturesPISA/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`

---

## Purpose

Assembly（実装では `neighbor_cluster.pdb`）に対する PISA 解析から、
Reference Chain A の界面特徴量を抽出する。

ADR-020 に従い Partner-specific Feature（Residue × Partner）を正本とし、
Global Feature をそこから集約する。ADR-019 により DSSP と入力構造を分離する。

ADR-022 により Node = SEQRES residue（missing 含む）。
missing 残基の PISA 量は計算不可のため NaN。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- neighbor_cluster.pdb 自動探索（GrepSubunits 依存）
- ローカル PISA 実行・ログ保存・interfaces XML エクスポート
- Partner-specific Feature CSV（dASA / interface_area / hbond / salt bridge）
- Global Feature CSV（global_dASA / interface_degree / totals）
- ADR-020 検証（Global ?= Σ Partner、modeled 残基）と `validation_dASA.csv`
- ADR-022: SEQRES 展開、`is_missing` / `missing_segment_length`
- Missing 残基の界面指標 = NaN（partner 行は維持）
- 可視化一式（dASA / validation / partner heatmaps & profiles）
- `summary.txt`（検証指標・Top interface residues）
- CLI（`feature_pisa.py`）と Notebook
- Result-006 と整合する検証（3構造で max|diff|=0、r≈1.0、modeled 上）

確認 PDB: 3DKT / 7S21 / 9B9I
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

実測グローバル行数: 3DKT 265、7S21 301、9B9I 281（missing 1 / 36 / 19）

---

## In Progress

- なし（単体コアは完了）。残課題は検証範囲の拡張と Merge / Contact 整合

---

## Not Implemented

- 複数 Biological Assembly / 全粒子 Assembly での系統的再検証
- Contact モジュールとの partner 集合整合
- MergeFeatures 連携
- RSA–ΔASA 相関の正式 Result（DSSP 側と共同）
- PISA 結果ディレクトリ内の missing overlay 図（DSSP/Contact/ADR022_figures 側には存在）
- モジュール専用 README.md
- ADR 命名ディレクトリ（`FeaturePISA/`）への配置
- Atlas 向け batch CLI

---

## Outputs

生成確認済み（3DKT / 7S21 / 9B9I）:

- `pisa_partner_features.csv`（is_missing, missing_segment_length 含む）
- `pisa_global_features.csv`（同上）
- `seqres_nodes.csv`
- `validation_dASA.csv`
- `summary.txt`
- `plots/global_dASA_profile.png` / `global_dASA_heatmap.png`
- `plots/interface_degree_profile.png` / `interface_degree_histogram.png`
- `plots/partner_dASA_heatmap.png` / `partner_interface_area_heatmap.png`
- `plots/combined_dASA_heatmap.png`
- `plots/dASA_validation_scatter.png` / `dASA_difference_profile.png`
- `plots/partner_contribution.png`

---

## Validation Status

- ADR-020: Global ?= Σ Partner（modeled）で max|diff|=0、Pearson r=1.0（3構造、summary / Result-006）
- ADR-022: ノード数・missing 数が期待値と一致
- Contact partner 集合との不一致は継続（例: 3DKT PISA B–F vs Contact B–H）
- Result-005: 局所 PDB での ASA 誤差可能性の注記あり（設計文脈）

関連 Result: Result-006（Global/Partner 検証）。Result-005。Result-007（SEQRES 移行根拠）。
ADR-022 移行後比較: `ADR022_before_after_comparison.csv`（正式 Result 番号は未採番）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（独立 Feature モジュール）
- ADR-019（DSSP と PISA の分離）
- ADR-020（Partner 正本、Global 集約）
- ADR-022（SEQRES Node、missing 特徴量）

---

## Known Issues

- Contact–PISA partner 集合不一致
- MergeFeatures 未着手
- PISA モジュール plots に missing overlay が無い（横断図は ADR022_figures / Contact 側）
- Edge-Features 未 SEQRES 移行とのノード長不一致

---

## Next Actions

High

- Contact–PISA partner 整合ルール固定
- MergeFeatures 連携設計（SEQRES 主キー）

Medium

- RSA–ΔASA 相関の正式 Result
- missing overlay の PISA 側追加（任意）

Low

- 全 Assembly 再検証、batch CLI、README

---

## Completion Estimate

Design: 95%

Implementation: 90%

Validation: 85%

Overall: 90%

---

### Current_State Summary

- FeaturePISA は ADR-022 対応済み（SEQRES Node、missing=NaN、3構造再計算済み）。
- ADR-020 検証（Global=ΣPartner）は modeled 残基で継続して成立。
- Contact との partner 不一致と Merge 未着手が主な残課題。
- Current_State では PISA を Mostly Complete（SEQRES 移行済）と扱う。
