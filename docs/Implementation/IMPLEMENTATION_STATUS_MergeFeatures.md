# Implementation Status

## Module

MergeFeatures

（実装名: 未作成）

実装パス: なし（`docs/Implementation/` および `PDB_analysis/` のいずれにも未配置）

---

## Purpose

ADR-018 に従い、独立モジュール（Contact / DSSP / PISA / 将来 RSCC 等）の
出力を学習用テーブルへ統合する。

ADR-022 以降は SEQRES 残基番号を主キーとする結合が前提。
partner 情報の保持／学習時集約、特徴量セット切替
（Contact only / Contact+DSSP / Contact+DSSP+PISA）、
将来的には Edge-Features との統合も担う想定。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Not Started

---

## Completed

- なし（ディレクトリ・スクリプト・出力いずれも未確認）

---

## In Progress

- なし

---

## Not Implemented

- モジュール設計書
- 結合キー仕様（pdb_id / chain_id / SEQRES resseq / icode）
- partner-long 形式と学習用 wide/集約形式の変換
- Contact × DSSP × PISA 結合 CSV / Parquet
- Edge Features との統合
- 特徴量セット切替
- GNN 入力（node/edge table, PyG）変換
- 検証・可視化
- batch 実行

---

## Outputs

なし

---

## Validation Status

未実施

上流3モジュール（Contact / DSSP / PISA）は ADR-022 対応済みで結合可能な素材は存在する。
Edge-Features は ATOM ベースのままのため、統合時に SEQRES 整列が別途必要。

関連 Result: Result-008 Next Action に MergeFeatures 実装が挙げられている。
統合検証の正式 Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

対象 ADR（未実装）:

- ADR-018（MergeFeatures 本体）
- ADR-017 / ADR-019 / ADR-020（統合時の粒度方針）
- ADR-021（Edge Features 統合時）
- ADR-022（SEQRES 主キー）

---

## Known Issues

- 上流の命名不一致（Feature* vs Features* / CountInteraction...）
- Contact と PISA の partner 集合不一致が結合設計のブロッカー
- Edge-Features が未 SEQRES 移行（ノード長が Feature 側と不一致）
- docs/Implementation 配下にモジュール実体が未配置
- Feature pipeline overall の到達点（学習テーブル）を遮断している本ボトルネック

---

## Next Actions

High

- MergeFeatures 設計（SEQRES キー、partner 扱い、出力スキーマ）を ADR or 設計メモとして固定
- Contact–PISA partner 整合ルールを先に決める

Medium

- 最小実装: 3DKT で Contact+DSSP+PISA を SEQRES キー結合した試作 CSV
- Edge-Features SEQRES 移行後の node–edge 整列

Low

- PyG 変換、FeatureRSCC 枠の予約

---

## Completion Estimate

Design: 25%

Implementation: 0%

Validation: 0%

Overall: 5%

---

### Current_State Summary

- MergeFeatures は Not Started（実装・出力ともに未確認）。
- Contact / DSSP / PISA は ADR-022 済みで統合素材は揃っている。
- 次の本丸ボトルネックは Merge 設計と Contact–PISA partner 整合、および Edge の SEQRES 整合。
- Current_State の次アクションに MergeFeatures 設計を明示し続ける必要がある。
