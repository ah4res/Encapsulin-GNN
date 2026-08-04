# Implementation Status

## Module

FeatureRSCC

（ADR-018 例示名: `FeatureRSCC`）

実装名: なし（`PDB_analysis/` 配下に FeatureRSCC / FeaturesRSCC / RSCC ディレクトリは存在しない）

探索的実装パス: `structure_tools/RSCC/`（PDB_analysis 外）

---

## Purpose

残基単位の Real-Space Correlation Coefficient（RSCC）を特徴量として抽出し、
構造品質・モデル信頼性のノード特徴候補とする。

ADR-018 / ADR-019 では将来 Feature として例示されているが、
専用 ADR（定義・粒度・SEQRES 整合）は未策定。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Not Started

（PDB_analysis モジュールとしては未着手。`structure_tools/RSCC/` に探索的 notebook/batch のみ存在）

---

## Completed

- なし（Feature モジュールとしての CSV / summary / plots / results_<PDBID> は未確認）

探索的資産（モジュール Completed 判定には使わない）:

- `rscc_per_residue.ipynb` / `rscc_chain_per_residue.ipynb`
- `batch_run_rscc_aef.py`（Phenix `real_space_correlation` / Cryo-EM `map_model_cc`）
- ログ上の過去バッチ（例: 9/10 成功、7CXM/7CXN 修正ラン）

---

## In Progress

- なし

---

## Not Implemented

- `PDB_analysis/FeatureRSCC/`（または FeaturesRSCC）ディレクトリ
- ADR-022 SEQRES ノード整合
- `results_<PDBID>/` 規約、`feature_manifest.csv`、README
- DatasetPreparation / GraphBuilder への組込
- Encapsulin gold_T1-enc 向け再計算
- FeatureRSCC 専用 ADR

---

## Outputs

`PDB_analysis` 規約の出力: なし

`structure_tools/RSCC/` は `work/<pdbid>/` 形式を想定するが、
現行 checkout に `work/` は無く、ログのみ残存（CSV/plots は不在）。

---

## Validation Status

未実施（Feature モジュールとして）。

関連 Result: なし。
ADR 言及: ADR-018 / ADR-019 の例示リストのみ。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（例示モジュール FeatureRSCC；未実装）
- ADR-019（将来特徴量リストに RSCC）

専用 ADR: なし

---

## Known Issues

- 探索コードが PDB_analysis 規約外・別マシンパス依存
- ATOM 志向の残基番号；SEQRES / missing 未対応
- Phenix / 密度マップ依存で再現環境が重い
- Feature pipeline（DatasetPreparation → GraphBuilder）に未接続

---

## Next Actions

High

- FeatureRSCC を採否するかを ADR で決定（採用する場合は仕様 ADR を先行）

Medium

- 採用時: PDB_analysis 配下へ移植、SEQRES 整合、gold_T1-enc で試作

Low

- 探索 notebook の整理またはアーカイブ方針

---

## Completion Estimate

Design: 10%

Implementation: 5%（探索コードのみ）

Validation: 0%

Overall: 5%

---

### Current_State Summary

- FeatureRSCC は ADR-018 例示のみで、PDB_analysis モジュールとしては Not Started。
- `structure_tools/RSCC/` に探索資産はあるが results_<PDBID> 規約の成果物は無い。
- Current_State では「未着手の将来特徴量」として扱う。
