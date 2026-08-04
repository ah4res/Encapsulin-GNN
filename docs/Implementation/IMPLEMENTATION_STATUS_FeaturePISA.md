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
Global Feature（`global_dASA` 等）も併せて保持する。

ADR-019 により DSSP RSA とは独立に計算する（Assembly 由来 ΔASA）。
ADR-022 により SEQRES ノードへ展開し、missing は NaN。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- neighbor_cluster.pdb 入力でのローカル CCP4 PISA 実行
- Partner-specific CSV（`partner_chain`, `dASA`, `interface_area`, `hbond_count`, `salt_bridge_count`）
- Global CSV（`global_dASA`, `interface_degree`, `total_interface_area`, `total_hbond_count`, `total_salt_bridge_count`, `interface_flag`）
- ADR-020 内蔵検証（`global_dASA ?= Σ partner dASA` → `validation_dASA.csv`）
- ADR-022: SEQRES 展開、`is_missing` / `missing_segment_length`、missing → NaN
- `seqres_nodes.csv` / `summary.txt` / plots（10 PNG）
- CLI（`feature_pisa.py`）と Notebook（one-shot `run_analysis`）
- DatasetPreparation 経由の batch 実行（`done.flag`）

確認 PDB: gold_T1-enc 由来 **39 構造**（全 results_* で両 CSV + summary + plots 完備）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

---

## In Progress

- なし（単体モジュールとしてのコア実装・Dataset A 規模の再計算は完了）

---

## Not Implemented

- Contact–PISA partner 集合の整合ルール実装
- モジュール専用 README.md（仕様は `input_cursor.md` / CLI docstring）
- ADR 命名ディレクトリ（`FeaturePISA/`）への配置・同期
- `feature_manifest.csv` は global 列のみ（partner / ADR-022 列は未列挙）
- RSA–ΔASA 相関の正式 Result 化（ADR-019 Next Action）

---

## Outputs

生成確認済み（39 PDB）:

- `pisa_partner_features.csv`
- `pisa_global_features.csv`
- `validation_dASA.csv`
- `seqres_nodes.csv`
- `summary.txt`
- `done.flag`
- `plots/`（partner_dASA_heatmap / combined_dASA_heatmap / validation scatter 等 10 PNG）

中間物: `working/` 配下の PISA XML / logs（成果物正本ではない）

---

## Validation Status

- ADR-020: Global + Partner 両形式の列を CSV で確認
- 内蔵 QC: `global_dASA` と Σpartner_dASA の差分（Result-006 と整合する検証経路）
- ADR-022: SEQRES ノード長・missing NaN を代表 3 構造で確認、全 39 完備
- Contact 側との partner 集合不一致は継続（例: 3DKT PISA B–F vs Contact B–H）

関連 Result: Result-006（global vs Σpartner 完全一致）。Result-007（SEQRES 移行根拠）。
RSA–ΔASA 相関の正式 Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（独立 Feature モジュール）
- ADR-019（DSSP RSA と独立の ΔASA）
- ADR-020（Global + Partner-specific）
- ADR-022（SEQRES Node）
- ADR-025（DatasetPreparation batch）

---

## Known Issues

- Contact との partner 集合不一致（PISA は A 関与 interface のみ）
- CCP4 PISA パスがマシン固有ハードコード
- `feature_manifest.csv` が partner スキーマを未反映
- 8IKA / 9RY4 は SEQRES 構築不可で DatasetPreparation で error

---

## Next Actions

High

- Contact–PISA partner 整合ルールを固定
- GraphBuilder での PISA 列採用方針（global vs partner-long）を確定

Medium

- RSA–ΔASA 相関を正式 Result として記録（ADR-019）
- `feature_manifest.csv` / README 整備

Low

- ADR 命名ディレクトリ同期
- CCP4 パスの環境変数化

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 90%

Overall: 90%

---

### Current_State Summary

- FeaturePISA は ADR-019/020/022 対応済み。39 構造で CSV/summary/plots/validation 完備。
- Result-006 系の dASA 検証経路がモジュール内に残っている。
- Contact との partner 集合不一致は Merge / GraphBuilder 設計前の未解消課題。
- Current_State では PISA を Mostly Complete（Dataset A 規模展開済）と扱う。
