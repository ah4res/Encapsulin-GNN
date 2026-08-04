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
PISA ΔASA とは意図的に分離する。

ADR-022 により Node = SEQRES。missing 残基は `is_missing` /
`missing_segment_length` を持ち、構造特徴量は NaN（SS=`MISSING`）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- mmCIF 自動取得（`data/<PDBID>.cif`）
- Chain A 単独抽出 → mkdssp
- RSA = ASA / MaxASA（Tien et al. 2013）
- ADR-022: SEQRES ノード展開、`is_missing` / `missing_segment_length`
- missing 残基: SS=`MISSING`、asa/rsa/phi/psi = NaN
- `dssp_features.csv` / `seqres_nodes.csv` / `summary.txt`
- QC plots（8 PNG: ss_rsa_combined / missing overlay / ramachandran 等）
- CLI（`feature_dssp.py`）と Notebook
- DatasetPreparation 経由の batch（`done.flag`）
- `feature_manifest.csv`（rsa/asa/dssp_state/phi/psi）

確認 PDB: gold_T1-enc 由来 **39 構造**（全 results_* で CSV + summary + plots 完備）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

代表例: 3DKT 265 rows（missing 1）、7S21 301（missing 36）、9B9I 281（missing 19）
→ Result-007 時点の ATOM 行数（264/265/262）ではなく SEQRES 長と一致

---

## In Progress

- なし（単体モジュールとしてのコア実装・Dataset A 規模の再計算は完了）

---

## Not Implemented

- モジュール専用 README.md（`input_cursor.md` / Notebook が代替）
- ADR 命名ディレクトリ（`FeatureDSSP/`）への配置・同期
- `feature_manifest.csv` への `is_missing` / `missing_segment_length` 列挙
- RSA–ΔASA 相関の正式 Result 化（ADR-019）

---

## Outputs

生成確認済み（39 PDB）:

- `dssp_features.csv`
  （列: secondary_structure, asa, rsa, phi, psi, is_missing, missing_segment_length）
- `seqres_nodes.csv`
- `summary.txt`
- `done.flag`
- `plots/`（8 PNG）

---

## Validation Status

- ADR-019: DSSP は neighbor_cluster ではなく Chain A 単独で実行されることをコード・出力で確認
- ADR-022: 現行 CSV は SEQRES 長（Result-007 記載の ATOM のみ状態は **解消済み**）
- 全 39 構造で CSV + summary + plots 完備
- `missing_residue_report.md` は移行前調査の歴史資料（現行状態とは矛盾するため正本にしない）

関連 Result: Result-007（移行前 ATOM ベース問題の根拠）。ADR-022 移行後比較資料は正式 Result 未採番。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（独立 Feature モジュール）
- ADR-019（モノマー RSA）
- ADR-022（SEQRES Node）
- ADR-025（DatasetPreparation batch）

---

## Known Issues

- README 未整備；`input_cursor.md` / `missing_residue_report.md` に移行前記述が残る
- 8IKA / 9RY4 は SEQRES 構築不可で DatasetPreparation で error
- RSA–ΔASA 相関の正式 Result 未作成

---

## Next Actions

High

- なし（コア完了；下流は GraphBuilder / Review）

Medium

- README 整備と stale 文書の明示（historical）
- RSA–ΔASA 相関を正式 Result 化

Low

- ADR 命名ディレクトリ同期
- manifest への missing 列追加

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 90%

Overall: 90%

---

### Current_State Summary

- FeatureDSSP は ADR-019/022 対応済み。39 構造で SEQRES 長の CSV/summary/plots 完備。
- Result-007 が示した ATOM のみ問題は実装側では解消済み（文書側の stale 報告に注意）。
- Current_State では DSSP を Mostly Complete（Dataset A 規模展開済）と扱う。
