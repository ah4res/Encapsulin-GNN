# Implementation Status

## Module

PDB-VLP-list（Icosahedral Particle Atlas）

実装パス: `structure_tools/PDB_analysis/PDB-VLP-list/`

ADR-018 の Feature 抽出モジュール例示には属さない。
Dry Research のデータセット構築基盤（Atlas）を担う独立プロジェクトである。

---

## Purpose

正二十面体対称粒子（Encapsulin / Virus / VLP / Engineered Nanocage 等）を、
名称キーワードではなく対称性（Point Group I 等）で収集し、
PDB/EMDB metadata・粒子分類・T-number・データセット適格性・系統関係を
一元管理する Icosahedral Particle Atlas を構築する。

DatasetPreparation / GraphBuilder の既定入力
`results/gold_T1-enc.csv`（41 Encapsulin T=1）を供給する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- Phase 1 Notebook 検証（01–08）
- Phase 2 src ライブラリ（検索 / metadata / 分類 / DB / T-number / eligibility / 系統樹）
- Dataset eligibility 出力（Gold T=1 / Silver T=3、Encapsulin サブセット）
- `gold_T1-enc.csv`（41）/ `silver_T3-enc.csv`（8）
- 系統樹解析成果（Result-003 系）
- 単体テスト（`tests/test_tnumber.py` / `test_dataset_eligibility.py` / `test_phylogeny.py`）
- 内部 docs（development_plan / ADR-012/013 ローカルコピー）

判定基準: CSV・summary・主要解析出力の実生成を確認

---

## In Progress

- Dataset A/B 最終リストの運用確定（gold_T1-enc は稼働中の暫定マスタ）

---

## Not Implemented

- Fold 分類（HK97 / Jelly-roll / Other）の本実装
  （`src/analysis/geometry.py` は `NotImplementedError` stub）
- Phase 3 CLI（`atlas discover/update/classify/...`）
- Icosahedral 誤検出（Cyclic/C2）・Caspar-Klug 例外の修正確認
- PDB–EMDB 対応付けの本格化
- T=3 Encapsulin 追加構造探索（BLAST/DALI/MATRAS）

---

## Outputs

主要確認済み:

- `results/gold_T1-enc.csv`（41 data rows）— DatasetPreparation / GraphBuilder 既定入力
- `results/silver_T3-enc.csv`（8）
- `results/gold_T1.csv` / `silver_T3.csv`（symlink → Result-003 系）
- `results/Result-003_dataset_eligibility.csv`（1818）
- `results/Result-003_dataset_eligibility_summary.md`（Gold 403 / Silver 243 / Gold-enc 41 / Silver-enc 8）
- phylogeny（`aligned.fasta`, `atlas_tree.nwk`, `atlas_tree.png` 等）
- `outputs/tnumber_*.csv`, `metadata/all_particles.csv`（647）等

---

## Validation Status

- Result-002: Assembly / T-number 基盤の実用性
- Result-003: 系統樹・段階的学習方針（Dataset A/B）
- テストファイルは存在（再実行は本調査では未実施；pytest_cache に過去収集痕跡）

Fold 分類未実装により Dataset B（T=1 全粒子）構築は未完。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-010（Icosahedral Particle Atlas）
- ADR-012（段階的拡張；文書内 Status 矛盾あり）
- ADR-013（Gold/Silver/Future；Status 欄欠落）
- ADR-025（`gold_T1-enc.csv` 入力）

---

## Known Issues

- Fold 分類未実装（Dataset B ブロッカー）
- geometry stub（NotImplementedError）
- Result-002 指摘の誤検出・Caspar-Klug 例外の修正状況未確認
- ADR-012/013 文書の不完全さは正本側課題

---

## Next Actions

High

- Fold 分類実装（HK97 / Jelly-roll / Other）
- Dataset A/B 最終構造リスト確定

Medium

- Icosahedral 誤検出・Caspar-Klug 例外の修正確認
- Phase 3 CLI

Low

- T=3 追加探索、PDB–EMDB 対応付け

---

## Completion Estimate

Design: 90%

Implementation: 75%

Validation: 70%

Overall: 75%

---

### Current_State Summary

- PDB-VLP-list は Atlas Phase 1–2 完了、gold_T1-enc（41）を Feature pipeline に供給中。
- Fold 分類と Phase 3 CLI が未実装で Dataset B が止まる。
- Current_State の Atlas 記述と整合；Fold 未実装を継続課題として維持。
