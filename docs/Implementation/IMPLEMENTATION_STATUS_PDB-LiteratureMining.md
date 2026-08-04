# Implementation Status

## Module

PDB-LiteratureMining

実装パス: `structure_tools/PDB_analysis/PDB-LiteratureMining/`

ADR-018 の Feature 抽出モジュール例示には属さない。
Wet Research（文献マイニング）向けの独立パイプラインである。

---

## Purpose

PDB ID を入力に、関連論文を取得し、Methods セクションから発現・精製条件を
抽出し、Evidence（原文引用）付きの構造化 Metadata（CSV/JSON）を生成する。

ADR-009 で自動パイプライン方針が示されたが、対象が 2 系統に絞られた後
close（手動調査へ切替）となった。実装コード自体は残り、7 PDB 分の出力がある。

現行抽出バックエンドは **rule_based**（`LLMExtractor` は NotImplementedError の placeholder）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Maintenance

（ADR-009 close 後の補助資産。新規機能開発は停止気味だが成果物は残存）

---

## Completed

- Phase 1/2: src ステップ分割（metadata → paper → PDF text → methods → metadata extraction）
- Phase 4: 7 PDB バッチ出力
- 対象 PDB: 3DKT, 7MU1, 7KQ5, 7K5W, 4PT2, 7S20, 8VJO
- `outputs/*_metadata.csv` / `encapsulin_batch_metadata.csv` / summary CSV
- `data/` 配下の JSON / methods text / PDF キャッシュ
- prompts/ に LLM 用テンプレート準備（現行 batch では未使用）

判定基準: CSV/JSON 等の実生成を確認

---

## In Progress

- なし（運用方針の整理待ち）

---

## Not Implemented

- Phase 3 CLI 化
- 本番 LLM 抽出（`LLMExtractor` は NotImplementedError）
- ADR-009 再稼働または正式アーカイブの決定
- tests/

---

## Outputs

確認済み（7 PDB）:

- `outputs/<PDB>_metadata.csv`
- `outputs/encapsulin_batch_metadata.csv`
- `outputs/encapsulin_batch_summary.csv`
- `data/metadata/*.json`, `data/pdb/*.json`, `data/methods/*.txt`, `data/papers/*.pdf`

`logs/` は空（`.gitkeep` のみ）。
Extraction_Backend=`rule_based`。

---

## Validation Status

- Result-004 は手動文献調査として ADR-014 の根拠になっており、
  本パイプライン出力とは別経路
- 自動抽出結果の正式 Result 化は未実施
- README の「Notebook 05 = OpenAI」記述は現行コード（rule_based）と不一致

関連 ADR: ADR-009（close）。関連 Result: Result-004（手動）。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-009（パイプライン方針；close）
- ADR-014（Wet 構築体；Result-004 手動調査が正本的根拠）

---

## Known Issues

- ADR-009 close と実装残存の仕様差分（維持か廃止か未決）
- README / Notebook の LLM 記述と rule_based 実装の不一致
- LLMExtractor 未実装
- Closed-access PDF 取得の制限（手動配置で回避）

---

## Next Actions

High

- 補助ツール維持 or 運用終了を ADR-009 方針に沿って確定

Medium

- 維持する場合: README を rule_based 現状へ修正
- 廃止する場合: アーカイブ方針と outputs の扱いを決める

Low

- Phase 3 CLI / 本番 LLM（維持決定時のみ）

---

## Completion Estimate

Design: 80%

Implementation: 70%（rule_based まで；LLM 未）

Validation: 40%

Overall: 60%

---

### Current_State Summary

- PDB-LiteratureMining は 7 PDB の rule_based 出力を持つが、ADR-009 は close。
- Wet の正本的文献根拠は Result-004（手動）。本コードの位置づけ確定が Open Question。
- Current Status は Maintenance。
