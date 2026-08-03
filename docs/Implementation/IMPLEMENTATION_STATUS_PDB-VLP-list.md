# Implementation Status

## Module

PDB-VLP-list（Icosahedral Particle Atlas）

実装パス: `structure_tools/PDB_analysis/PDB-VLP-list/`

ADR-018 の Feature 抽出モジュール例示（FeatureContact 等）には属さない。
Dry Research のデータセット構築基盤（Atlas）を担う独立プロジェクトである。

---

## Purpose

正二十面体対称粒子（Encapsulin / Virus / VLP / Engineered Nanocage 等）を、
名称キーワードではなく対称性（Point Group I 等）で収集し、
PDB/EMDB metadata・粒子分類・T-number・データセット適格性・系統関係を
一元管理する Icosahedral Particle Atlas を構築する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

（Phase 1: Notebook検証 / Phase 2: srcライブラリ化は完了。
Phase 3: CLI化は未着手）

---

## Completed

- Notebook 01〜08（対称性検索 / PDB metadata / EMDB metadata / 粒子分類 /
  DB統合 / 統計 / T-number検出 / Atlas系統樹）
- `src/api/`（pdb_search, pdb_metadata, emdb_metadata, http_client）
- `src/database/`（SQLAlchemy models・ops・session、`data/db/atlas.sqlite`）
- `src/analysis/`（classify, statistics, geometry, tnumber, dataset_eligibility,
  shell_protein, phylogeny）
- `src/export/`（csv_export, json_export）
- `config/`（API・検索・分類ルールのYAML化）
- CLIスクリプト3種（`scripts/run_dataset_eligibility.py`,
  `scripts/run_tnumber_all.py`, `scripts/run_atlas_phylogeny.py`）
- 単体テスト 43件全てpass（`tests/test_tnumber.py`,
  `tests/test_phylogeny.py`, `tests/test_dataset_eligibility.py`）
- 実データ検証: `rcsb_struct_symmetry.symbol == I` でtotal_count=1812を
  確認済み（`docs/current_state.md`記載）
- T-number全件出力（`outputs/tnumber_all.csv`、1817件データ）
- Dataset Eligibility出力（Result-003対応、Gold T1 / Silver T3 / Excluded）
- Atlas系統樹（全体版・Encapsulin限定版の両方）
  - CD-HIT (95%) → MAFFT → FastTree のパイプライン成果物
    （fasta, nr95, aligned.fasta, atlas_tree.nwk/png, cluster_report.tsv,
    atlas_phylogeny_summary.md）を`results/`と`results/enc/`双方で確認

判定基準: CSV・DB・系統樹画像・テストパスの実確認まで確認できたもののみ
Completed

---

## In Progress

- T-number決定ロジック（ADR-013 Level1〜4優先順位）の適用範囲拡大・
  再検証（ADR-011→ADR-013のSupersedingを受けた継続調整）

---

## Not Implemented

- Phase 3 CLI（`atlas discover/update/classify/export-csv/export-json/stats/
  list/show`、README上で明示的に未実装と記載）
- Result-002で指摘されたIcosahedral判定誤検出（Cyclic/C2構造の誤分類）の
  修正確認
- Result-002で指摘されたCaspar-Klug例外（多層粒子、Rotavirus/Reovirus等）
  への対応確認
- Fold分類（HK97 / Jelly-roll / Other）— Dataset B構築に必要だが
  `src/analysis/`内に実装が見当たらない
- PDB-EMDB対応付けの完了（Result-002 Next Action）

---

## Outputs

生成確認済み:

- `outputs/tnumber_all.csv`, `tnumber_T1.csv`, `tnumber_T3.csv`,
  `tnumber_T1_encapsulin.csv`, `tnumber_T3_encapsulin.csv`, `tnumber_100.csv`,
  `classified_preview.csv`, `stats_summary.json`
- `outputs/tables/`（organism / T-number / method / particle-type 分布）
- `results/Result-003_dataset_eligibility.csv` + `_summary.md`
- `results/gold_T1.csv`, `silver_T3.csv`, `gold_T1-enc.csv`, `silver_T3-enc.csv`
- `results/enc/`（Encapsulin限定系統樹一式）・`results/`（全体系統樹一式）
- `data/db/atlas.sqlite`
- `metadata/all_particles.csv`, `metadata/enc_particles.csv`

---

## Validation Status

- 単体テスト 43/43 pass（tnumber / phylogeny / dataset_eligibility）
- RCSB Search APIでの実データスモークテスト（Icosahedral symmetry検索で
  total_count=1812）を`docs/current_state.md`で確認
- Result-002/Result-003がAtlas構築・T-number推定・系統樹解析の妥当性を
  裏付けている
- Result-002で指摘された誤検出・例外構造への対応が実際に修正されたかは
  本調査の範囲では再確認できていない（テストケースに該当構造が
  含まれているかは未確認）

関連 Result: Result-002（Atlas基盤技術検証、課題3件の指摘）、
Result-003（Gold/Silver系統樹解析、初期GNN学習方針への反映）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-010（Icosahedral Particle Atlas構築方針、Encapsulin限定からの拡張）
- ADR-011（T-number決定ロジック Level1〜4優先順位。ADR-013へSuperseded）
- ADR-012（GNN学習の段階的拡張戦略。Status記載が「Proposed」と
  「Accepted」で文書内矛盾あり）
- ADR-013（Gold/Silver/Future Tierによるデータセット適格性基準。
  Status欄なしの草稿だがResult-003により方向性は支持）

---

## Known Issues

- ADR-012はヘッダー「Status: Proposed」とValidation Results欄
  「Status: Accepted」が矛盾したまま（docs側課題、本モジュールの
  実装自体は当該ADRの方針に沿って進んでいる）
- ADR-013はStatus/Rationale/Alternatives/Consequences/Next Actionが
  未記載の草稿状態
- Result-002指摘のIcosahedral誤検出・Caspar-Klug例外の修正状況が
  コードから確認できていない（回帰テストの追加が必要）
- Fold分類（HK97/Jelly-roll）未実装のため、Dataset B（T=1全粒子）の
  構築がブロックされている
- PDB-EMDB対応付けの完了状況が不明確

---

## Next Actions

High

- Result-002指摘のIcosahedral誤検出・Caspar-Klug例外に対する修正状況を
  検証し、回帰テストとして固定化する
- Fold分類（HK97/Jelly-roll/Other）を実装し、Dataset B構築のブロッカーを
  解消する

Medium

- Dataset A（T=1 Encapsulin）・Dataset B（T=1全粒子）の最終構造リストを
  確定する（B1完了条件）
- ADR-012のStatus矛盾解消、ADR-013の未記載セクション補完（docs側作業）

Low

- Phase 3 CLI（`atlas ...`）の実装
- PDB-EMDB対応付けの完了確認

---

## Completion Estimate

Design: 90%

Implementation: 85%

Validation: 75%

Overall: 83%

---

### Current_State Summary

- PDB-VLP-list（Icosahedral Particle Atlas）はPhase 1/2が完了し、
  検索・metadata取得・分類・DB・統計・T-number・Dataset Eligibility・
  系統樹解析まで実装済み（単体テスト43/43 pass）。
- Gold(T1)/Silver(T3)データセットと系統樹（Result-003対応）は
  再現的に生成可能。
- Result-002指摘のIcosahedral誤検出・Caspar-Klug例外の修正確認は
  未完了のまま。
- Dataset B構築に必要なFold分類（HK97/Jelly-roll）は未実装。
- Phase 3 CLIは未着手、Dataset A/Bの最終構造リストも未確定（B1未完了）。
