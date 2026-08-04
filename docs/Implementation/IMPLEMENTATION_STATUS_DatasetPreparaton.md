# Implementation Status

## Module

DatasetPreparaton

（Scope (b): 実装ディレクトリ名を ModuleName とする。
 ディレクトリ名は `DatasetPreparaton`（i 欠落）。ADR-025 / README 表記は `DatasetPreparation`。）

実装パス: `structure_tools/PDB_analysis/DatasetPreparaton/`

---

## Purpose

ADR-025 に従い、各 Feature モジュールを統括するオーケストレーション層。

データセット CSV（既定: `PDB-VLP-list/results/gold_T1-enc.csv`）から
複数 PDB × 複数モジュールを一括実行する。

成果物の正本は各モジュールの `results_<PDBID>/` に残し、
本モジュール自身は特徴量データを保持しない。
`done.flag` による skip と batch report を提供する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- `run_dataset_preparation.py` CLI（`--force` / `--module` / `--limit` / `--pdb`）
- `modules.yaml`（DSSP, AA, Grep, PISA, Contact, Edge；EdgeFeatures は既定 disabled）
- GrepSubunits 依存の blocked 判定（PISA / Contact）
- `done.flag` skip / 成功時書込
- `reports/batch_report_*.csv`（12 本以上）と detail レポート
- `logs/dataset_preparation_*.log`
- Notebook（`DatasetPreparation.ipynb`）
- README.md

確認済み実ラン（例）:

- gold_T1-enc 41 PDB 向け DSSP/Grep/PISA/Contact/Edge 一括
- FeaturesAA 単独 41 PDB バッチ

判定基準: オーケストレータとしての CSV レポート・ログ生成を確認できたものを Completed

---

## In Progress

- なし（コア orchestrator は稼働済み）

---

## Not Implemented

- ディレクトリ名の ADR 表記（`DatasetPreparation`）へのリネーム
- 並列実行（ADR-025 Low）
- Edge / EdgeFeatures 論理二重名の整理
- git 初回コミット（ディレクトリ全体が untracked）
- 8IKA / 9RY4 など SEQRES 不能 PDB のハンドリング方針（skip ポリシー文書化）

---

## Outputs

- `reports/batch_report_YYYYMMDD_HHMMSS.csv`
- `reports/detail_batch_report_*.csv`
- `logs/dataset_preparation_*.log`
- 各モジュール `results_<PDBID>/done.flag`（成功時）

代表レポート要約（`batch_report_20260803_135928.csv`）:

| Module | skip | success | error |
|--------|-----:|--------:|------:|
| DSSP | 39 | 0 | 2 |
| Grep | 3 | 38 | 0 |
| PISA | 3 | 36 | 2 |
| Contact | 3 | 36 | 2 |
| Edge | 39 | 0 | 2 |

error はいずれも 8IKA / 9RY4（Chain A `_pdbx_poly_seq_scheme` 欠落）。

---

## Validation Status

- gold_T1-enc 41 PDB での実バッチ成功をレポートで確認
- 依存関係 blocked（Grep 未完了時の PISA/Contact）を detail レポートで確認
- Feature 側 39 構造完備と整合（2 構造は失敗として残存）

正式な Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-025（DatasetPreparation 本体）
- ADR-018（独立モジュールの一括実行）
- ADR-024（Feature Generation 自動化部分）

---

## Known Issues

- ディレクトリ名 typo（`DatasetPreparaton`）
- 8IKA / 9RY4 が継続 error
- structure_tools 上で untracked（版管理リスク）
- EdgeFeatures 論理モジュールが既定 disabled

---

## Next Actions

High

- DatasetPreparaton を git へコミット
- 8IKA / 9RY4 の適格性除外または修復方針を決める

Medium

- ディレクトリ名を ADR 表記へ揃える
- Edge/EdgeFeatures 設定の整理

Low

- 並列実行

---

## Completion Estimate

Design: 95%

Implementation: 90%

Validation: 80%

Overall: 85%

---

### Current_State Summary

- DatasetPreparation（実装名 DatasetPreparaton）は ADR-025 通り稼働し、gold_T1-enc 41 PDB バッチ実績あり。
- Feature Generation 自動化は完了に近い。残課題は失敗 PDB 2 件と git 未追跡。
- Current_State に ADR-025 実装進捗を追記する必要がある。
