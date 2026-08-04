# Implementation Status

## Module

GraphBuilder

（Scope (b): 実装ディレクトリ名を ModuleName とする。ADR-026。）

実装パス: `structure_tools/PDB_analysis/GraphBuilder/`

---

## Purpose

ADR-026 に従い、Feature Review 後の特徴量を選択・統合し、
再現可能な Graph Dataset を構築する。

責務:

```text
Feature Selection → Feature Merge → Dataset Construction → Experiment Tracking
```

Feature モジュール名や特徴量名はソースにハードコードせず、
`feature_registry.yaml` + Feature Set YAML で解決する。

初期出力は `merged_node_features.csv` / `merged_edge_features.csv`。
PyTorch Geometric 変換は後続（GraphEncoder；未実装）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- `build_graph.py` CLI（`--list-features` / `--list-feature-sets` / `--validate-registry` / `--feature-set` / `--pdb` / `--limit` / `--skip-missing`）
- `feature_registry.yaml`（45 特徴: AA 24 / DSSP 5 / PISA 6 / Contact 6 / Edge 4）
- Feature Sets: FS-AA, FS-AA-DSSP, FS-AA-PISA, FS-AA-DSSP-EDGE, FS-ALL
- CSV Merge（node outer-join / edge keys）
- Graph Dataset ID / Experiment ID 採番（`manifests/graph_index.json`）
- 実生成データセット Graph-001 … Graph-004
- README.md

確認済み出力例:

| Graph | Feature set | PDBs | nodes | edges |
|-------|-------------|------|------:|------:|
| Graph-001 | FS-AA-DSSP | 2 | 566 | 2442 |
| Graph-002 | FS-AA-DSSP-EDGE | 1 | 265 | 1233 |
| Graph-003 | FS-ALL | 1 | 265 | 1233 |
| Graph-004 | FS-AA-DSSP | 10 | 2743 | 12343 |

判定基準: merged CSV + graph/experiment manifest の実生成を Completed

---

## In Progress

- Dataset A（gold_T1-enc 全量）での本格 Graph 構築
- FS-AA / FS-AA-PISA の実 Graph 生成（定義のみ・未生成）

---

## Not Implemented

- PyTorch Geometric Export（ADR-026 Encoding Strategy；GraphEncoder 空ディレクトリ）
- AI による自動 Feature Set 提案（ADR-026 Low）
- Feature 採否履歴・Review コメント連携（ADR-024）
- git 初回コミット（ディレクトリ全体が untracked）
- Contact partner-long / PISA partner-long の学習用集約ポリシー実装
  （現状 registry は Contact summary 列・PISA global 列中心）

---

## Outputs

各 `datasets/Graph-NNN/`:

- `merged_node_features.csv`
- `merged_edge_features.csv`
- `graph_manifest.json`
- `experiment_manifest.json`

`manifests/graph_index.json`: next_graph_number=5 / next_experiment_number=5、4 graphs 登録。

`logs/`: `.gitkeep` のみ（実行ログファイルなし；成果物で成功を確認）。

---

## Validation Status

- Registry / Feature Set によるプラグイン結合が実データで動作することを確認
- Graph-001〜004 の row/col が manifest の node_count/edge_count と一致
- gold_T1-enc 全 41（または成功 39）での正式検証は未了

正式な Result は未作成。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-026（GraphBuilder 本体）
- ADR-018（独立 Feature → 統合の拡張）
- ADR-022（SEQRES 主キー）
- ADR-024（Review 後の Selection/Merge 位置づけ）
- ADR-025（上流 DatasetPreparation）

---

## Known Issues

- structure_tools 上で untracked
- Partner-specific（Contact/PISA long form）が registry に未登録
- Contact–PISA partner 不一致が学習セット品質に影響しうる
- GraphEncoder / PyG 未着手のため Training 直前まで未到達
- logs が空で再現監査が成果物依存

---

## Next Actions

High

- GraphBuilder を git へコミット
- gold_T1-enc 成功 39 PDB で FS-ALL または FS-AA-DSSP-EDGE を構築し Result 化

Medium

- partner-long 特徴の registry / Feature Set 方針を決める
- Contact–PISA partner 整合後に再マージ

Low

- GraphEncoder（PyG）着手
- 実行ログ出力の追加

---

## Completion Estimate

Design: 95%

Implementation: 85%

Validation: 60%

Overall: 75%

---

### Current_State Summary

- GraphBuilder（ADR-026）は稼働済み。Feature Merge + Dataset ID/Manifest まで実装し Graph-001〜004 を生成。
- ADR-018 の MergeFeatures ボトルネック記述は、本モジュール進捗で更新が必要。
- 残課題は全量 Dataset A 構築・partner 整合・PyG Export・git 追跡。
