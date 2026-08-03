# Implementation Status

## Module

FeatureDSSP

（実装名: `FeaturesDSSP`）

実装パス: `structure_tools/PDB_analysis/FeaturesDSSP/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`

---

## Purpose

Reference Chain A 単独構造に対して mkdssp を実行し、
二次構造・ASA・RSA・φ/ψ を残基特徴量として抽出する。

ADR-019 により RSA はモノマー状態の表面露出性を表し、
Assembly / neighbor_cluster には適用しない。

ADR-022 により Node = SEQRES residue（missing 含む）とし、
共通 Node Feature `is_missing` / `missing_segment_length` を付与する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- RCSB からの構造取得（mmCIF）→ `data/`
- Chain A 抽出 → `working/<PDB>_chainA.pdb`
- mkdssp 実行（確認: mkdssp 4.4.5）
- RSA = ASA / MaxASA（Tien et al. 2013）
- ADR-022: `_pdbx_poly_seq_scheme` 由来 SEQRES テーブル展開
- ADR-022: `is_missing` / `missing_segment_length` 列
- Missing 時: `secondary_structure=MISSING`、ASA/RSA/φ/ψ = NaN
- `dssp_features.csv` 生成（3構造、行数 = SEQRES 長）
- `seqres_nodes.csv` 生成（3構造）
- `summary.txt` 生成
- 可視化一式（ss map / RSA / combined / Ramachandran / histogram / missing overlay）
- CLI（`feature_dssp.py`）と Notebook

確認 PDB: 3DKT / 7S21 / 9B9I
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

実測ノード数 / missing: 3DKT 265/1、7S21 301/36、9B9I 281/19（ADR-022 期待値と一致）

---

## In Progress

- なし（単体モジュールとしてのコア実装は完了）

---

## Not Implemented

- ADR-019 Next Action の **RSA と ΔASA の相関確認を Result として正式記録**
- Atlas / Dataset 向け batch 一括実行 CLI
- MergeFeatures 連携（統合モジュール未着手）
- ADR 命名ディレクトリ（`FeatureDSSP/`）への配置・同期
- モジュール専用 README.md
- ADR-022 移行後状態を正とする **正式 Result の更新**（Result-007 は移行前スナップショット）

---

## Outputs

生成確認済み（3DKT / 7S21 / 9B9I）:

- `dssp_features.csv`
  （列: pdb_id, chain_id, resseq, icode, resname, secondary_structure, asa, rsa, phi, psi, is_missing, missing_segment_length）
- `seqres_nodes.csv`
- `summary.txt`
- `plots/secondary_structure_map.png`
- `plots/rsa_profile.png` / `rsa_histogram.png` / `rsa_heatmap.png`
- `plots/ss_rsa_combined.png`
- `plots/ramachandran_plot.png`
- `plots/ss_alignment_heatmap.png`
- `plots/Figure_missing_overlay.png`

関連横断成果物: `PDB_analysis/ADR022_before_after_comparison.csv`、`ADR022_Implementation_Report.md`

---

## Validation Status

- 3構造で CSV / plots / summary まで一貫生成
- Node 数 = SEQRES 長、missing 数は ADR-022 / Result-007 調査と一致
- Result-007: 移行前の ATOM ベース消失問題を記録し ADR-022 策定の根拠
- 移行後の before/after 比較は `ADR022_before_after_comparison.csv` で確認（正式 Result 番号は未採番）
- summary 上、7S21 / 9B9I で Max RSA > 1 の事例あり（MaxASA スケール限界）

関連 Result: Result-007（missing 調査・移行前）。Result-005（局所グラフ文脈）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（独立 Feature モジュール）
- ADR-019（DSSP と PISA の物理量分離、RSA 定義）
- ADR-022（SEQRES Node、is_missing / missing_segment_length）

---

## Known Issues

- `missing_residue_report.md` 等の調査メモが移行前（ATOM 行数）の記述のまま残存し得る
- Max RSA > 1（7S21 / 9B9I）
- Edge-Features は未 SEQRES 移行のため、DSSP ノード長と Edge ノード長が不一致
- MergeFeatures 未着手のため学習テーブル未統合

---

## Next Actions

High

- ADR-022 移行後検証を正式 Result として記録（Result-007 の後継）
- MergeFeatures 設計時の SEQRES 主キー結合仕様を固定

Medium

- RSA–ΔASA 相関の正式 Result（FeaturePISA と共同）
- モジュール README / ADR 命名同期

Low

- MaxASA 超過 RSA の扱い方針（クリップ vs そのまま保持）

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 85%

Overall: 90%

---

### Current_State Summary

- FeatureDSSP は ADR-022 対応済み（SEQRES Node、missing 特徴量、3構造再計算済み）。
- ノード数は 3DKT 265 / 7S21 301 / 9B9I 281、missing は 1 / 36 / 19。
- Result-007 は移行前状態の記録；実装は既に後続状態。
- 残課題は正式 Result 更新、Merge 連携、RSA–ΔASA 相関。
- Current_State では「DSSP 未着手」ではなく Mostly Complete（SEQRES 移行済）と扱う。
