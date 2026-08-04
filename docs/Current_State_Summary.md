WARNING

本ファイルは `Current_State.md` の要約版（エグゼクティブサマリー）である。

詳細な根拠・議論は `Current_State.md`（AI向け統合コンテキスト）、
および正本である ADR / Results / Roadmap / Project_Charter を参照すること。

矛盾がある場合は `Current_State.md` および正本を優先する。

SOP-001（ver1.2）に基づき、再構築済み `Current_State.md` から生成。
独自の事実判断は追加しない。

---

# Current State Summary

## Last Updated

2026-08-03

---

## Executive Summary

Encapsulin-GNNは正二十面体対称粒子の形成原理をGNNで解析しWetで検証する。
Dryでは局所グラフ（ADR-016 Trial）を土台に、SEQRESノード（ADR-022）と
HELOエッジ特徴（ADR-023；ADR-021を置換）がAccepted。パイプラインは
Feature Review（ADR-024）→ DatasetPreparation（ADR-025）→ GraphBuilder（ADR-026）
まで設計確定し、単純MergeFeaturesはGraphBuilderへ吸収された。
実装補助資料では主要Feature/Edgeがgold_T1-enc規模でSEQRES対応済み、
Graph試作（Graph-001〜004）まで到達。残課題はpartner整合・全量Graph正式化・
PyG/Training・Dataset B（Fold分類）・Wet C1着手である。

---

## Current Position

### Infrastructure

Research OS運用開始済み（ADR-001〜008）。new-HPC構成確定（ADR-015）だが
発注・納品・A7は未完。ADR-009自動文献パイプラインはclose。

### Dry Research

Atlas（ADR-010）＋`gold_T1-enc`運用中。特徴量/グラフ設計はADR-017〜023、
運用層はADR-024〜026までAccepted。GraphBuilderが統合の到達点。
B1（Dataset A/B最終確定）とB4（Baseline GNN）は未達。

### Wet Research

ADR-014で構築体・宿主確定。WT Criteria定義済みだがC1実験未着手。
文献根拠はResult-004（手動）。

---

## Implementation Status

主要モジュールのみ（補助資料；OverallはImplementation Status記載値）

- FeatureContact: Mostly Complete（90%）
- FeatureDSSP: Mostly Complete（90%）
- FeaturePISA: Mostly Complete（90%）
- FeaturesAA: Mostly Complete（85%）
- Edge-Features: Mostly Complete（90%、ADR-022/023対応済み）
- FeatureRSCC: Not Started（5%）
- DatasetPreparaton: Mostly Complete（85%）
- FeatureExtraction_Overview: Mostly Complete（80%）
- GraphBuilder: Mostly Complete（75%、Graph-001〜004）
- MergeFeatures（専用dir）: Not Started（5%；MergeはGraphBuilderへ吸収）
- PDB-GrepSubunits: Mostly Complete（90%）
- PDB-VLP-list: Mostly Complete（75%、Fold未実装）
- PDB-LiteratureMining: Maintenance（60%）

---

## Current Bottlenecks

1. Contact–PISA partner集合不一致（学習データ品質の前提未決）
2. GraphBuilder全量Dataset Aの正式化・Result化、およびPyG/Training未着手
3. Fold分類未実装によるDataset B（およびB1完了）遅延

---

## Recent Important Decisions

- ADR-023: HELO `ss_pair`（ADR-021 Supersede）
- ADR-022: SEQRESノード
- ADR-024: Feature Review
- ADR-025: DatasetPreparation
- ADR-026: GraphBuilder（MergeFeatures拡張吸収）

---

## Recent Important Results

- Result-008: エッジ検証＋HELO → ADR-023
- Result-007: missing消失 → ADR-022
- Result-006: dASA整合 → ADR-020支持
- Result-003: Dataset A/B方針
- Result-005: 局所グラフ検討の起点

---

## Top Priority Decisions

- ADR-012/013/020のStatus確定
- Contact–PISA partner整合ルール
- GraphBuilder正式Feature Set / 全量構築方針
- ADR-016 Status確定計画
- C1着手可否（Dataset待ちか並行か）

---

## Risks

- ADR-016 Trialのまま依存実装が進み手戻りする
- partner不一致のまま学習すると再現性が損なわれる
- new-HPC遅延で計算資源が不足する
- Fold未実装のままDataset Bを進めるとバイアスが残る
- Wet先行により変異体設計タイミングがずれる

---

## Next Milestones

- ADR文書整備（012/013/016/020）とpartner整合
- Dataset A正式Graph＋Result化
- Baseline GNN（B4）着手
- Dataset A/B確定・Fold分類
- C1着手／new-HPC A7
