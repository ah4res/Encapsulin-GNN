# Implementation Status

## Module

Edge-Features

（Scope (b): ADR-018 Feature 例示名ではなく、実装ディレクトリ名を ModuleName とする。
 ADR-021/023 のエッジ定義・特徴量を実装するモジュール。）

実装パス: `structure_tools/PDB_analysis/Edge-Features/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`（SEQRES ノード）

---

## Purpose

ADR-016 の局所グラフ表現に基づき、Reference Chain A 内部の残基間エッジを
Cα距離閾値で定義し、エッジ特徴量を抽出する。

特徴量:

- `actual_distance`
- `sequence_distance`
- `ss_pair`（ADR-023: HELO 10 分類 — HH/EE/LL/HE/HL/EL/HO/EO/LO/OO）
- `same_ss_element`

初期閾値 8 Å（4/6/8/10 Å でアブレーション可能）。
ADR-022 によりノードは SEQRES 基準（missing 含む）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- Cα距離閾値エッジ定義（default 8 Å、CLI `--threshold`）
- `actual_distance` / `sequence_distance` / `ss_pair` / `same_ss_element`
- ADR-023 HELO 10-class `ss_pair`（コード・CSV・summary.json で確認）
- ADR-022 SEQRES ノード（`seqres_nodes.csv`、`node_definition: SEQRES`）
- `edge_features.csv` / `summary.json` / `ss_pair_same_element_summary.csv`
- plots Figure1–6
- CLI（`edge_features.py`）と Notebook
- `validation/` 閾値グリッド（4/6/8/10 Å）および same_ss_element QC
- DatasetPreparation 経由の batch（Edge モジュール；`done.flag`）
- `feature_manifest.csv`（4 edge features）
- README.md

確認 PDB: gold_T1-enc 由来 **39 構造**（全 results_* で CSV + summary + 6 plots 完備）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

代表例（threshold=8）:

| PDB | nodes | missing | edges |
|-----|------:|--------:|------:|
| 3DKT | 265 | 1 | 1233 |
| 7S21 | 301 | 36 | 1209 |
| 9B9I | 281 | 19 | 1197 |

→ Feature 側 SEQRES ノード数と一致（旧 ATOM ベース不一致は解消済み）

---

## In Progress

- なし（単体モジュールとしてのコア実装・Dataset A 規模の再計算は完了）

---

## Not Implemented

- ソース／README 内の ADR 参照が ADR-021 表記のまま（ADR-023 名を未記載）
- README 検証表の一部が HEL 6-class 集計のまま（現行 summary は 10-class）
- Distance RBF 展開（ADR-021 Deferred / ADR-023 Low）
- DatasetPreparation 上 EdgeFeatures 論理名は既定 disabled（Edge と同一物理パイプライン）

---

## Outputs

生成確認済み（39 PDB）:

- `edge_features.csv`
- `seqres_nodes.csv`
- `summary.json`
- `ss_pair_same_element_summary.csv`
- `done.flag`
- `plots/Figure1_*.png` … `Figure6_*.png`（6 PNG）

validation/:

- `threshold_edge_counts.csv` 等
- `results_{3DKT,7S21,9B9I}_thr{4,6,8,10}/`（CSV/JSON；plots なし）

working/: Chain A PDB / DSSP 中間物（scratch）

---

## Validation Status

- Result-008 と整合する閾値エッジ数（例: 3DKT 4/6/8/10 Å = 267/689/1233/2125）を validation で再現
- HELO 由来 HO/EO/LO/OO が summary.json で非ゼロ（Result-008 / ADR-023 を支持）
- ADR-022: ノード数が SEQRES 長と一致（旧「Feature 301 vs Edge 265」問題は解消）
- 全 39 構造で主出力完備

関連 Result: Result-008。
正式な ADR-023 反映確認 Result の追加採番は任意。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016（局所グラフ・A 内部エッジ）
- ADR-021（エッジ定義の初版；Superseded → ADR-023）
- ADR-023（HELO ss_pair；現行仕様）
- ADR-022（SEQRES Node）
- ADR-025（DatasetPreparation）
- ADR-026（GraphBuilder EdgeFeatures ソース）

---

## Known Issues

- ドキュメント上の ADR-021 / HEL 表記と実装（ADR-023 HELO）の表記ずれ
- 8IKA / 9RY4 は SEQRES 構築不可で batch error
- Edge と EdgeFeatures が同一ディレクトリを共有（オーケストレータ上の二重論理名）

---

## Next Actions

High

- README / ソースコメントの ADR 参照を ADR-023 へ更新
- Dataset A 全量での GraphBuilder 統合確認

Medium

- README 検証表を HELO 10-class 集計へ更新
- EdgeFeatures 論理モジュールの orchestrator 整理

Low

- Distance RBF 検討

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 90%

Overall: 90%

---

### Current_State Summary

- Edge-Features は ADR-023 HELO と ADR-022 SEQRES の両方に対応済み。39 構造で完備。
- Feature 側とのノード数不一致（旧課題）は解消。Current_State の「Edge 未 SEQRES」記述は更新が必要。
- ドキュメントの ADR-021 表記残存が残課題。
