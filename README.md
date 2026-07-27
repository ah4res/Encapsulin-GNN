# Encapsulin-GNN Research Operating System

## Purpose

本プロジェクトは、正二十面体対称粒子形成を規定する構造原理をGraph Neural Network（GNN）により解析し、その予測結果をWet実験によって検証することを目的とする。

本研究では、

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

研究期間を通じて、

- なぜその意思決定を行ったのか
- 何が分かったのか
- 現在どこまで進んでいるのか

を追跡可能とするため、本 Research Operating System（Research OS）を採用する。

---

# Basic Principles

本プロジェクトでは GitHub Repository を唯一の正本（Single Source of Truth）とする。

チャット履歴は保存対象としない。

保存対象は以下とする。

- Project Charter
- Roadmap
- Current State
- ADR
- Result

AIとの対話履歴そのものではなく、

- 意思決定
- 実験結果
- 解析結果

を記録する。

---

# Repository Structure

```text
06_Encapsulin-GNN/

README.md

docs/

├─ Project_Charter.md
├─ Current_State.md

├─ Roadmap/
│  ├─ Roadmap_A_Infrastructure.md
│  ├─ Roadmap_B_DryResearch.md
│  └─ Roadmap_C_WetResearch.md

├─ ADR/
│  ├─ ADR-001.md
│  ├─ ADR-002.md
│  └─ ...

└─ Results/
   ├─ Result-001.md
   ├─ Result-002.md
   └─ ...

src/
data/
analysis/
manuscript/
```

---

# Document Roles

## Project_Charter.md

プロジェクトの憲章。

定義する内容

- 研究目的
- 科学的問い
- 研究範囲
- 成功条件

原則として頻繁に変更しない。

研究目的そのものが変更される場合のみ更新する。

---

## Roadmap

中長期計画を管理する。

以下の3トラックで構成する。

### Track A: Infrastructure

研究基盤整備

対象例

- Research OS
- GitHub
- Cursor
- Google Colab
- HPC
- 再現性確保
- Storage for backup

---

### Track B: Dry Research

AI・計算解析

対象例

- Dataset construction
- Feature engineering
- Graph representation
- GNN analysis
- Interpretation

---

### Track C: Wet Research

実験検証

対象例

- 遺伝子構築
- 発現
- 精製
- 粒子評価
- 変異体解析
- AI予測検証

---

Roadmap は中長期計画を示す。

日常的には更新しない。

大きな方針変更が生じた場合のみ更新する。

---

## Current_State.md

プロジェクト全体のダッシュボード。

最重要ファイル。

壁打ち開始時には必ず参照する。

記載内容

- 現在位置
- 最近の重要決定
- 最近の重要結果
- 現在の課題
- 次の意思決定事項
- 次のアクション

Current_State は ADR と Result を要約したものとする。

---

# ADR

ADR = Architecture Decision Record

本プロジェクトにおける重要な意思決定を記録する。

ソフトウェア開発だけではなく、

- 研究方針
- 実験方針
- データセット方針
- モデル選択
- 検証戦略

もADRとして扱う。

---

## ADRを書く基準

記録するもの

- ノード定義
- エッジ定義
- モデル選択
- 学習方針
- 評価方針
- Wet実験方針
- 検証戦略
- 研究上重要な判断

記録しないもの

- 軽微な実装変更
- バグ修正
- ファイル整理
- 一時的試行

---

## ADR命名規則

```text
ADR-001.md
ADR-002.md
ADR-003.md
...
```

通し番号とする。

Trackごとの番号体系は採用しない。

---

## ADRテンプレート

```markdown
# ADR-XXX

Date

Track

Question

Decision

Rationale

Alternatives Considered

Status

Validation Results / ex.) - Results-###
```

statusには以下を記載する
Proposed/Trial/Accepted/Rejected/Superseded -> ADR###

---

# Results

Result は

「何を行い、何が分かったか」

を記録する。

Result は実験ノートではない。

研究方針に影響を与える重要な結果のみ記録する。

---

## Resultを書く基準

記録するもの

- GNN性能評価
- 特徴量比較
- モデル比較
- 変異体評価
- 粒子形成評価
- AI予測の検証結果

記録しないもの

- 日常実験記録
- 単なる作業ログ
- 一時的な失敗

---

## Result命名規則

```text
Result-001.md
Result-002.md
Result-003.md
...
```

通し番号とする。

Trackごとの番号体系は採用しない。

---

Result-000はResearch OS導入以前の運用方針確立を記録する例外的なResultである。
Result-001以降は、関連するADRを少なくとも1件持つものとする。

---

## Resultテンプレート

```markdown
# Result-XXX

Date

Track

Related ADR / ex.) ADR-###

Objective

Method

Result

Interpretation

Conclusion

Next Action
```
すべてのResultは、関連するADRを最低1件記載する。
関連ADRが存在しない場合は "None" と記載する。

---

# Relationship Between Documents

```text
Discussion

↓

ADR

↓

Experiment / Analysis

↓

Result

↓

Current_State

↓

Next Discussion
```

Current_State は常に現在地を示す。

ADR と Result は履歴保管庫である。

---

# AI Usage Policy

## Copilot

役割

- 壁打ち
- アイデア検討
- 批判的レビュー
- ADR作成支援

Copilotは長期記憶を持たない。

壁打ち時には

- Project_Charter
- Current_State

を入力として利用する。

---

## Cursor

役割

- コーディング
- 実装
- 文書解析
- Current_State更新支援

Cursorは

- Project_Charter
- Roadmap
- ADR
- Result

を参照する。

定期的にADRおよびResultを統合し、

Current_Stateを更新する。

---

# Operational Rules

重要な議論を行った場合

1. ADR作成
2. Current_State更新
3. Git Commit

重要な結果が得られた場合

1. Result作成
2. Current_State更新
3. Git Commit

---

# Guiding Principle

未来の自分が、

「なぜその判断をしたのか」

を理解できることを最優先とする。

記録の目的は保存ではない。

研究の再現性、継続性、共有可能性を高めることである。

## File Ownership Policy

### Human Managed

以下のファイルは人間のみが編集する。

- Project_Charter.md
- Roadmap/*
- ADR/*
- Results/*
- README.md
- SOP/*

### Cursor Managed

以下のファイルはCursorによる更新を許可する。

- Current_State.md

Current_Stateはプロジェクトの現在地を示す
ダッシュボードであり、

ADR
Result
Roadmap

から生成される派生文書として扱う。
