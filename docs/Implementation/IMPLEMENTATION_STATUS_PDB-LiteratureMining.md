# Implementation Status

## Module

PDB-LiteratureMining

実装パス: `structure_tools/PDB_analysis/PDB-LiteratureMining/`

ADR-018 の Feature 抽出モジュール例示（FeatureContact 等）には属さない。
Wet Research（文献マイニング）向けの独立パイプラインである。

---

## Purpose

PDB ID を入力に、関連論文を取得し、Methods セクションから発現・精製条件を
LLM で抽出し、Evidence（原文引用）付きの構造化 Metadata（CSV/JSON）を
生成する。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

（ただし ADR Coverage 参照。ADR-009 は本パイプラインの自動化方針自体を
close しており、Current Status の解釈には注意が必要）

---

## Completed

- Phase 1: Single PDB Prototype（対象: 3DKT）
  - `01_single_pdb_prototype.ipynb`（PDB→Metadata取得）
  - `02_paper_retrieval.ipynb`（DOI→論文取得、手動配置フォールバック含む）
  - `03_pdf_to_text.ipynb`（PDF→テキスト変換）
  - `04_methods_extraction.ipynb`（Methodsセクション抽出）
  - `05_metadata_extraction.ipynb`（LLMによるEvidence付き構造化抽出）
- Phase 2: Notebook 01〜05 のロジックを `src/step1_*.py`〜`src/step5_*.py` へ
  モジュール化
- Phase 4: Batch Processing（`06_batch_processing.ipynb`）
  - 対象7 PDB（3DKT, 7MU1, 7KQ5, 7K5W, 4PT2, 7S20, 8VJO）で
    Methods抽出まで完了（README記載の結果サマリで確認）
- Evidence-Based Extraction スキーマ（Value + Evidence）
- サプリメンタリPDF活用ロジック（`find_supplementary_pdf_links`、
  手動配置3件の本文外補完に利用）
- 実データ検証で発見された抽出ロジックの不具合修正
  （Vector正規表現の誤抽出、IPTG単位のµM未対応、Methods見出し検出の
  空白文字問題、Temperature誤抽出、Evidence文字列の長さ上限）
- API応答キャッシュ（`data/cache/`、複数PDB分を確認）
- LLMプロンプトの外部ファイル化（`prompts/`）

確認 PDB: 3DKT, 7MU1, 7KQ5, 7K5W, 4PT2, 7S20, 8VJO（7件）
判定基準: CSV・テキスト・metadata JSON の実生成まで確認できたもののみ Completed

---

## In Progress

- なし（Phase 1/2/4 のコア実装は完了）

---

## Not Implemented

- Phase 3: CLI化（README上で明示的に「未着手」と記載）
- 自動テスト
- 本パイプライン自体の実行結果を対象とした正式な Result 文書
  （Result-004は本コードベースの出力ではなく、別途の手動文献調査の結果）

---

## Outputs

生成確認済み:

- `data/pdb/*.json`（RCSB metadata）
- `data/papers/*.pdf`（自動取得3件 + 手動配置4件）
- `data/text/*.txt`
- `data/methods/*_methods.txt`（7件）
- `data/metadata/*.json`（Evidence付き構造化抽出結果）
- `outputs/<PDB>_metadata.csv`（個別7件）
- `outputs/encapsulin_batch_metadata.csv`（全Value/Evidence列、PDBごと1行）
- `outputs/encapsulin_batch_summary.csv`（主要項目要約）

`logs/` ディレクトリは存在するが、本調査時点でファイルは確認できなかった
（実行ログが永続化されていない可能性）。

---

## Validation Status

- README記載の結果サマリ（2026-07-29時点）で対象7件全てMethods抽出まで完了
- 実データ検証で発見した抽出ロジックの不具合修正について、
  3DKTの結果への影響がないことが確認済み（README記載）
- Evidence-Based原則（未検証値は`null`、捏造しない）をAPIキー未設定時にも
  遵守する設計を確認
- 本コードベースの出力自体を評価した正式なResultは存在しない
  （Result-004は別途の手動調査結果であり、本パイプラインの出力とは独立）

関連 Result: なし（本パイプラインの出力を直接評価したResultは未作成。
Result-004は目的が異なる別成果物）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-009（PDB起点の自動文献マイニングパイプライン方針）
  Status: Close。対象系統がT. maritima / M. xanthusの2系統のみのため、
  自動化パイプラインではなく手動調査（Result-004）で運用する方針への
  変更が採択されている。

---

## Known Issues

- **仕様差分（重要）**: ADR-009はパイプライン自動化戦略そのものをcloseし、
  手動調査（Result-004）を正式な運用方法としているが、本コードベースは
  Phase 1/2/4が実装済みで実際に7 PDB分の出力を生成している。
  ADR決定とコードの完成度に不整合があり、Current_State側でも
  本コードベースの存在・出力がWet Research欄に反映されていない
- Phase 3（CLI化）が未実装のまま
- `logs/`が空（実行ログの永続化方針が不明）
- 自動取得できたPDFは7件中3件のみ（4件は出版社ボット対策・PMCのProof-of-Work
  チャレンジにより手動配置が必要。方針上、回避策は実装しない）

---

## Next Actions

High

- ADR-009の「close」決定と本コードベースの完成度の関係を整理し、
  Current_Stateに反映する（本パイプラインを補助ツールとして維持するか、
  完全に運用終了とするかを明確化）

Medium

- Phase 3 CLI化の要否をADR-009の方針を踏まえて再検討する

Low

- `logs/`の運用方針（永続化するか否か）を明確化する

---

## Completion Estimate

Design: 100%

Implementation: 80%

Validation: 70%

Overall: 80%

---

### Current_State Summary

- PDB-LiteratureMining は Phase 1/2/4 が実装済みで、7 PDB分の
  構造化Metadata CSVを実際に生成している（Phase 3 CLIのみ未実装）。
- ADR-009は自動化パイプライン戦略自体をcloseし、手動調査（Result-004）を
  正式な運用方法としており、本コードベースの完成度とADR決定の間に
  仕様差分がある。
- Current_StateのWet Research欄は本コードベースの存在・出力に触れておらず、
  更新時に反映または位置づけの明確化が必要。
- 本パイプライン自体の出力を評価した正式なResultは存在しない。
- 自動PDF取得は7件中3件のみで、残りは方針上手動配置に依存している。
