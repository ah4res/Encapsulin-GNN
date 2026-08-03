## SOP-001

### Current_State Update Procedure

#### Purpose

Current_State.md を最新状態へ更新する。

Current_State はプロジェクト全体の
唯一のダッシュボードとする。

Current_State の役割は
既存内容を部分修正することではない。

ADR、
Result、
Roadmap
を正本として、

Current_State を再構築することを目的とする。

---

### Location

本SOPは以下に配置する。

/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/SOP

Current_State 更新時には
必ず本SOPを参照する。

---

### Input Documents

必ず以下を参照する。

#### Required

- Project_Charter.md
- Roadmap_A_Infrastructure.md
- Roadmap_B_DryResearch.md
- Roadmap_C_WetResearch.md
- ADR/*
- Results/*

#### Optional

- README.md
- Current_State.md（参考情報のみ）

---

### Source of Truth

Current_State は正本ではない。

正本は以下とする。

- Project_Charter
- Roadmap
- ADR
- Result

Current_State はこれらから生成される派生文書である。

Current_State の既存記載が
ADR や Result と矛盾する場合は、

ADR および Result を優先する。

---

### Reconstruction Rule

Current_State 更新時は

「既存Current_Stateの編集」

ではなく、

「ADRとResultからの再構築」

として扱う。

Current_State の既存内容を
事実の根拠として利用してはならない。

---

### Required Pre-Processing

Current_State 更新前に必ず以下を実施する。

#### Step 1

Project_Charter を確認する。

#### Step 2

Roadmap を確認する。

#### Step 3

ADR を全件走査する。

対象：

ADR/*

#### Step 4

Result を全件走査する。

対象：

Results/*

#### Step 5

Current_State.md を確認する。

ただし参考情報としてのみ扱う。

---

### Freshness Rule

Current_State 更新時には
特に以下を優先して確認すること。

- Current_State 最終更新日以降に追加された ADR
- Current_State 最終更新日以降に追加された Result
- 最新10件の ADR
- 最新10件の Result

---

### Rules

Current_State は履歴ではない。

Current_State は

「今現在」

を表す。

過去の詳細は ADR および Result に残す。

Current_State は

- Project_Charter
- Roadmap
- ADR
- Result

から生成される派生文書である。

---

### Required Sections

## Current State

### Project Summary

### Infrastructure

#### 現在地

#### 最近の重要決定

#### 最近の重要結果

#### 現在の課題

#### 次のアクション

---

### Dry Research

#### 現在地

#### 最近の重要決定

#### 最近の重要結果

#### 現在の課題

#### 次のアクション

---

### Wet Research

#### 現在地

#### 最近の重要決定

#### 最近の重要結果

#### 現在の課題

#### 次のアクション

---

### Active ADR

Cursor Suggested

現在プロジェクトを支配していると考えられる
ADRを最大5件抽出する。

抽出基準

- 現在の意思決定に強く影響している
- Current_Stateの内容に直接関係する
- 現在の研究方針を規定している

追加ルール

Current_State更新日以降に追加された
Accepted ADRは必ず評価対象とする。

---

### Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えている
Resultを最大5件抽出する。

抽出基準

- 現在の研究方針に影響している
- Current_Stateの理解に重要である
- 今後の研究計画に影響している

追加ルール

Current_State更新日以降に追加された
Resultは必ず評価対象とする。

---

### Open Questions

Cursor Generated

Project_Charter、
Roadmap、
ADR、
Result をもとに、

現在十分に解決されていない重要課題を
3〜10件程度抽出する。

Open Questionsは正本ではない。

Current_State生成時点での
Cursorによる提案である。

以下を含めてもよい。

- 未決定の研究課題
- 将来ADRとなる可能性のある論点
- トラック間依存
- 見落とされている課題
- 将来のボトルネック

---

### Top Priority Decisions

今後1〜2週間で
決定すべき事項

---

### Risks

主要リスク

---

### Next Milestones

次のマイルストーン

---

### Consistency Check

Current_State更新時には
以下を確認すること。

- 未反映のAccepted ADRは存在しないか
- 未反映のResultは存在しないか
- Rejected ADRが残っていないか
- Superseded ADRが残っていないか
- Open Questionsが既存ADRで既に解決されていないか
- Current_StateとADR/Result間に矛盾がないか

---

### Update Report

Current_State更新後に
必ず以下をレポートする。

#### Reflected ADR

Current_Stateへ反映したADR一覧

#### Reflected Results

Current_Stateへ反映したResult一覧

#### Not Reflected ADR

評価したが反映しなかったADR一覧

理由も記載する。

#### Not Reflected Results

評価したが反映しなかったResult一覧

理由も記載する。

#### Consistency Issues

検出された不整合候補

---

### Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

Current_State.md ファイルの編集だけであれば
実行可否を問い合わせる必要はない。
