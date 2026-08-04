# Implementation Status

## Module

FeaturesAA

（ADR-018 例示名ではなく、ADR-026 / 実装ディレクトリ名 `FeaturesAA` を ModuleName とする）

実装パス: `structure_tools/PDB_analysis/FeaturesAA/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`

---

## Purpose

SEQRES 配列のみからノード特徴量（アミノ酸特徴）を生成する。

構造情報・DSSP・PISA・Contact には依存しない。
ADR-022 の「1 residue = 1 node」に従い、missing 残基もノードとして保持する
（配列由来特徴は deposited `mon_id` から付与し、NaN 化しない）。

特徴: `charge`, `hydrophobicity`（Kyte–Doolittle）, `aromatic`, `polar`,
標準 20 AA One-Hot（`aa_A`…`aa_V`）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- PDB ID → mmCIF 取得 → SEQRES テーブル構築
- AA 特徴量計算（電荷・疎水性・芳香族・極性・One-Hot）
- `aa_features.csv` / `summary.json` / `seqres_nodes.csv`
- plots（aa_frequency / charge_distribution / hydrophobicity_distribution）
- CLI（`feature_aa.py`）と Notebook
- `feature_manifest.csv`（24 特徴）
- README.md
- DatasetPreparation 経由の batch（`done.flag`；modules.yaml で enabled）

確認 PDB: gold_T1-enc 由来 **39 構造**（全 results_* で CSV + summary.json + plots 完備）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

代表例: 3DKT 265 nodes（missing 1）、7S21 301（missing 36）、9B9I 281（missing 19）

---

## In Progress

- なし（単体モジュールとしてのコア実装は完了）

---

## Not Implemented

- git への初回コミット（ディレクトリ全体が untracked）
- `aa_features.csv` 本体への `is_missing` 列同梱
  （missing メタは sibling `seqres_nodes.csv` に分離；DSSP とは列パッケージが異なる）
- 正式な Result による検証記録

---

## Outputs

生成確認済み（39 PDB）:

- `aa_features.csv`
- `summary.json`（`node_definition: SEQRES` 等）
- `seqres_nodes.csv`（`is_missing` / `missing_segment_length`）
- `done.flag`
- `plots/aa_frequency.png`
- `plots/charge_distribution.png`
- `plots/hydrophobicity_distribution.png`

---

## Validation Status

- SEQRES のみ依存・構造非依存をコードと README で確認
- ノード数が SEQRES 長と一致することを代表構造で確認
- 全 39 構造で CSV + summary + plots 完備
- GraphBuilder registry に登録済み（FS-AA 等）

正式な Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（独立 Feature モジュール思想の拡張）
- ADR-022（SEQRES Node）
- ADR-025（DatasetPreparation 実行順に組込）
- ADR-026（GraphBuilder Feature Registry の主要ソース）

---

## Known Issues

- structure_tools リポジトリ上で FeaturesAA が未コミット（再現性の版管理リスク）
- missing フラグが feature CSV に無く `seqres_nodes.csv` 側のみ（Merge 時のキー結合に注意）
- 8IKA / 9RY4 は SEQRES 構築不可で batch error

---

## Next Actions

High

- FeaturesAA を structure_tools へコミットし版管理を確立

Medium

- GraphBuilder 全量 Dataset A への本格適用
- missing 列パッケージ方針を他モジュールと揃えるか設計メモ化

Low

- 正式 Result による分布 QC 記録

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 75%

Overall: 85%

---

### Current_State Summary

- FeaturesAA は新規 Feature モジュールとして Mostly Complete。39 構造で出力完備。
- SEQRES 配列のみ依存；GraphBuilder / DatasetPreparation に組込済み。
- git 未追跡が残課題。Current_State の Feature 一覧に FeaturesAA を追加する必要がある。
