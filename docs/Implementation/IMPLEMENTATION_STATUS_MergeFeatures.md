# Implementation Status

## Module

MergeFeatures

（実装名: 専用ディレクトリは未作成）

実装パス: なし（`PDB_analysis/MergeFeatures/` は存在しない）

後継実装: `structure_tools/PDB_analysis/GraphBuilder/`（ADR-026）

---

## Purpose

ADR-018 に従い、独立モジュール（Contact / DSSP / PISA / AA / Edge 等）の
出力を学習用テーブルへ統合する、という当初の責務。

ADR-026 により、単純な MergeFeatures 実装は採用せず、
GraphBuilder が次を一体管理する方針へ拡張された。

```text
Feature Selection → Feature Merge → Dataset Construction → Experiment Tracking
```

したがって本ファイルは「ADR-018 の MergeFeatures 概念」の追跡用であり、
実際の結合・データセット構築の実装状況は `IMPLEMENTATION_STATUS_GraphBuilder.md` を正とする。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Not Started

（専用モジュールとしては Not Started。Feature Merge 機能自体は GraphBuilder で In Progress〜Mostly Complete）

---

## Completed

- なし（`MergeFeatures/` ディレクトリ・専用スクリプト・専用出力は未確認）

GraphBuilder 側で確認済みの代替成果（詳細は GraphBuilder ファイル）:

- `merged_node_features.csv` / `merged_edge_features.csv`
- Graph-001 … Graph-004 + manifests

---

## In Progress

- なし（本モジュール固有の作業なし）

---

## Not Implemented

- `MergeFeatures/` ディレクトリおよび専用 CLI
- ADR-018 想定の「単純 CSV 結合のみ」モジュール（ADR-026 で Rejected）
- GraphBuilder 未カバーの partner-long 形式の学習用 wide 変換ポリシー文書化
- PyTorch Geometric 変換（GraphEncoder へ委譲予定；未実装）

---

## Outputs

専用モジュール出力: なし

代替: `GraphBuilder/datasets/Graph-NNN/`

---

## Validation Status

専用モジュールとしての検証: 未実施。

上流 Feature モジュール（AA/DSSP/PISA/Contact/Edge）は SEQRES 対応済みで結合可能な素材は存在する。
GraphBuilder による試作結合（最大 10 PDB / FS-ALL）は実在。

関連 Result: Result-008 Next Action に MergeFeatures 実装が挙げられているが、
ADR-026 以降は GraphBuilder が後継。統合検証の正式 Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-018（MergeFeatures 概念の起点）
- ADR-022（SEQRES 主キー）
- ADR-024（Merge 前の Feature Review）
- ADR-026（GraphBuilder が Feature Merge を包含；単純 MergeFeatures は不採用）

---

## Known Issues

- Current_State が「MergeFeatures = Not Started が最大ボトルネック」と記載し続けているが、
  Feature Merge 自体は GraphBuilder で試作済み（ボトルネック記述の更新が必要）
- Contact–PISA partner 集合不一致は結合設計上の課題として残存
- 専用 MergeFeatures と GraphBuilder の文書上の二重表現が混乱を招きうる

---

## Next Actions

High

- Current_State / Roadmap 上の「MergeFeatures」表記を GraphBuilder（ADR-026）へ更新
- Contact–PISA partner 整合ルールを固定

Medium

- GraphBuilder の Dataset A 全量構築と正式 Result 化
- partner-long の学習時集約方針を Feature Set / ADR で明示

Low

- 歴史的 MergeFeatures 名のアーカイブ注記のみ残す運用

---

## Completion Estimate

Design: 80%（ADR-026 で設計は GraphBuilder へ移行）

Implementation: 0%（専用モジュール）／ GraphBuilder 側は別ファイル参照

Validation: 0%（専用）

Overall: 5%（専用モジュール基準）

---

### Current_State Summary

- 専用 MergeFeatures ディレクトリは依然 Not Started。
- ADR-026 により Feature Merge 責務は GraphBuilder へ吸収・拡張済み（試作 Graph-001〜004 あり）。
- 「統合が完全未着手」という表現は現状と矛盾する。Current_State は GraphBuilder 進捗を反映すべき。
