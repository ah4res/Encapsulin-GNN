WARNING

本ファイルは `Current_State.md` の要約版（エグゼクティブサマリー）である。

詳細な根拠・議論は `Current_State.md`（AI向け統合コンテキスト）、
および正本である ADR / Results / Roadmap を参照すること。

矛盾がある場合は `Current_State.md` および正本（ADR/Results/Roadmap）を優先する。

SOP-001（ver1.2）に基づき生成。

---

# Current State Summary

## Last Updated

2026-08-03

---

## Executive Summary

Encapsulin-GNNは、正二十面体対称粒子の形成原理をGNNで解析し、Wet実験で
検証するプロジェクトである。Dry Researchでは局所グラフ表現（ADR-016）の
ノード設計（ADR-022: SEQRESベース、missing residue保持）とエッジ設計
（ADR-021: Cα距離閾値、HELO拡張ss_pair）がAcceptedとなり、Feature
抽出モジュール（Contact/DSSP/PISA）はADR-022対応まで完了した。一方、
新設のEdge-FeaturesモジュールはADR-022未対応（ATOMベース）のままであり、
Feature側とEdge側でノード数が一致しない新たな整合性課題が生じている。
統合モジュールMergeFeaturesは依然Not Startedで、Feature pipeline全体の
最大ボトルネックである。Infrastructureはnew-HPC構成が確定し発注段階、
Wet ResearchはADR-014により初期構築体が確定したがC1着手前の段階にある。

---

## Current Position

### Infrastructure

Research OS運用開始済み（ADR-001〜008）。new-HPC構成は確定済み
（ADR-015）だが発注・納品・環境構築（A6/A7）は未完了。

### Dry Research

Icosahedral Particle Atlas（ADR-010）構築中。局所グラフのノード
（ADR-022: SEQRESベース）・エッジ（ADR-021: Cα距離閾値・HELO ss_pair）
設計がAccepted。FeatureContact/DSSP/PISAはADR-022対応済みでMostly
Complete、Edge-FeaturesはMostly CompleteだがADR-022未対応。
MergeFeaturesはNot Started（全体最大のボトルネック）。

### Wet Research

ADR-014により初期構築体・発現宿主が確定（Construct-Tm-01/02,
Construct-Mx-01）。WT Stage Success Criteria定義済みだが実験未着手。
`PDB-LiteratureMining`の位置づけ（維持/廃止）も未整理。

---

## Implementation Status

- FeatureContact: Mostly Complete（Overall 85%、ADR-022対応済み）
- FeatureDSSP: Mostly Complete（Overall 90%、ADR-022対応済み）
- FeaturePISA: Mostly Complete（Overall 90%、ADR-022対応済み）
- Edge-Features: Mostly Complete（Overall 85%、ADR-022未対応）
- MergeFeatures: Not Started（Overall 5%）
- PDB-GrepSubunits: Mostly Complete（Overall 85%）
- PDB-VLP-list（Atlas）: Mostly Complete（Overall 83%、Fold分類未実装）
- PDB-LiteratureMining: Mostly Complete（Overall 80%、位置づけ未整理）

---

## Current Bottlenecks

- MergeFeatures未着手のままFeature pipeline全体が学習用テーブルへ
  到達できていない（最大のボトルネック）
- Edge-FeaturesがADR-022（SEQRES）未対応のため、Feature側（例: 7S21で
  301ノード）とEdge側（同265ノード）でノード数が一致しない
- FeatureContact–FeaturePISA間でpartner chain集合が不一致
  （3DKT: Contact 7 chain vs PISA 5 chain）

---

## Recent Important Decisions

- ADR-022: GNNノードをATOMではなくSEQRES配列基準で定義し、missing
  residueも`is_missing`/`missing_segment_length`付きで保持する（Accepted）
- ADR-021: Reference Chain A内部エッジをCα距離閾値（初期値8Å）で定義し、
  actual_distance/sequence_distance/ss_pair/same_ss_elementを保持する
  （Accepted。本文はHEL表記のままでResult-008のHELO拡張が未反映）
- ADR-016: Reference Chain A中心の局所グラフ表現を採用する
  （Status: Trial、Accepted化は未了）
- ADR-018: 特徴量抽出パイプラインを独立モジュール化し、MergeFeaturesで
  統合する（Accepted）
- ADR-017: サブユニット間接触特徴量はpartner chainごとに保持する（Accepted）

---

## Recent Important Results

- Result-008: ADR-021のエッジ設計を3構造で検証し妥当性を確認。ss_pairの
  HELO拡張（10種）を採用仕様として結論づけた
- Result-007: FeaturesDSSP等がATOMベースのためmissing residueが消失
  していることを確認（7S21で約12%）。ADR-022策定の根拠となった
- Result-006: PISAのglobal_dASAとΣpartner_dASAの完全一致を確認し、
  ADR-020を支持（テンプレート未準拠の記載欠落あり）
- Result-005: 3DKT近傍サブユニット抽出により局所グラフ設計（ADR-016）の
  妥当性を検討（Related ADR欄の参照に疑義あり）
- Result-003: 系統樹解析により初期GNN学習をDataset A（T=1 Encapsulin）/
  Dataset B（T=1 Virus）の二本立てとする方針を導いた

---

## Top Priority Decisions

- MergeFeaturesの設計方針（SEQRES主キー・partner集約方式・出力スキーマ）を
  確定し、実装に着手する
- Edge-FeaturesのADR-022（SEQRES）移行の実施タイミングを決定する
- ADR-021本文のss_pair仕様をHELO版へ更新するか判断する
- FeatureContact–FeaturePISA間のpartner chain集合不一致の解消ルールを決定する
- Dataset A/Bの構造リストを確定する（B1完了条件）

---

## Risks

- Edge-FeaturesがADR-022未対応のままMergeFeaturesへ統合されると、
  ノード集合不一致のまま学習データが構築されるリスクがある
- MergeFeatures未着手のまま単体モジュールが先行 → Feature pipeline全体・
  B4着手が遅延するリスクがある
- Contact/PISA partner集合不一致が未解消のままMergeFeaturesを実装 →
  学習データ品質リスクがある
- new-HPC納品遅延 → Dry Research本格開始の遅延リスクがある
- Wet Research（ADR-014）がDry Research（B1未完了）に先行 → 後工程との
  整合リスクがある

---

## Next Milestones

- MergeFeatures設計・実装完了
- Edge-FeaturesのADR-022移行完了、ADR-021本文のHELO版更新
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の確定（B1完了条件）
- 初期GNNベースラインモデルの構築（B4着手）
- C1 Gene Preparation完了

---

詳細は `Current_State.md` を参照。
