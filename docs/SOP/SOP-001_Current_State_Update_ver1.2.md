### SOP-001

#### Current_State Update Procedure

Version: 1.2

---

##### Relationship to Previous Versions

本SOPはver1.1を継承・拡張する。

ver1.1で定義された

- Reconstruction Rule
- Required Pre-Processing
- Freshness Rule
- Rules
- Current_State.md の Required Sections
- Consistency Check
- Update Policy

はver1.2にすべて統合され、引き続き有効とする。

ver1.2で新たに追加される要素は

- Current_State_Summary.md（人間向けエグゼクティブサマリー）の新設
- Implementation Status の補助資料としての位置づけ明確化
- Dual Dashboard Principle

である。

ver1.2はver1.1を置き換える正式版（Superseding）とし、
以後のCurrent_State更新はver1.2に従う。

---

##### Location

本SOPは以下に配置する。

```text
/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/SOP
```

Current_State更新時には必ず本SOPを参照する。

---

##### Purpose

Current_State.md を最新状態へ更新する。

Current_State はプロジェクト全体の
統合ダッシュボードとする。

Current_State の役割は
既存内容を部分修正することではない。

ADR、
Result、
Roadmap
を正本として、

Current_State を再構築することを目的とする。

また、

Current_State_Summary.md

を同時生成し、

人間が短時間で現在地を把握できる
エグゼクティブサマリーを提供する。

---

##### Output Documents

Current_State更新時には以下を同時更新する。

###### Current_State.md

AI向け詳細ダッシュボード

用途：

- Copilot
- Cursor
- 将来のAI Agent

向け統合コンテキスト

詳細情報を保持する。

長文化してもよい。

---

###### Current_State_Summary.md

人間向けエグゼクティブサマリー

用途：

- PI
- 開発者
- 将来の自分

が短時間で現在地を把握すること。

詳細説明は省略し、

Current_State.md の要約版として扱う。

---

##### Input Documents

必ず以下を参照する。

###### Required

- Project_Charter.md
- Roadmap_A_Infrastructure.md
- Roadmap_B_DryResearch.md
- Roadmap_C_WetResearch.md
- ADR/*
- Results/*

###### Optional

- README.md
- Current_State.md（参考情報のみ）
- docs/Implementation/*（`IMPLEMENTATION_STATUS_*.md`）

---

##### Source of Truth

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

Implementation Status は
正本ではない。

Implementation Status は

「実装進捗の補助資料」

として扱う。

ADR・Resultと矛盾する場合、

ADRおよびResultを優先する。

---

##### Reconstruction Rule

Current_State 更新時は

「既存Current_Stateの編集」

ではなく、

「ADRとResultからの再構築」

として扱う。

Current_State の既存内容を
事実の根拠として利用してはならない。

この原則は Current_State.md 本体に適用する。

Current_State_Summary.md は、

再構築済みの Current_State.md を要約することで生成する。

Current_State_Summary.md 自体がADR/Resultを再解釈する
新たな情報源になってはならない。

---

##### Implementation Status Rule

Current_State 更新時には
Implementation Status を参照してよい。

目的：

- 実装進捗確認
- ボトルネック確認
- Current_Stateとの乖離検出

Implementation Statusは

研究上の意思決定

および

研究上の結果

を決定するためには利用してはならない。

研究判断は必ず

ADR

Result

を根拠とする。

---

##### Required Pre-Processing

Current_State 更新前に必ず以下を実施する。

###### Step 1

Project_Charter を確認する。

###### Step 2

Roadmap を確認する。

###### Step 3

ADR を全件走査する。

対象：

ADR/*

###### Step 4

Result を全件走査する。

対象：

Results/*

###### Step 5

Current_State.md を確認する。

ただし参考情報としてのみ扱う。

###### Step 6

Implementation Status（`docs/Implementation/*`）を確認する。

ただし補助資料としてのみ扱い、
研究判断の根拠にはしない。

---

##### Freshness Rule

Current_State 更新時には
特に以下を優先して確認すること。

- Current_State 最終更新日以降に追加された ADR
- Current_State 最終更新日以降に追加された Result
- 最新10件の ADR
- 最新10件の Result
- Current_State 最終更新日以降に更新された Implementation Status

---

##### Rules

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

Current_State_Summary は

Current_State をさらに要約した
エグゼクティブサマリーであり、

独自の事実判断を追加しない。

---

##### Current_State.md Required Sections

# Current State

## Project Summary

## Infrastructure

### 現在地

### 最近の重要決定

### 最近の重要結果

### 現在の課題

### 次のアクション

---

## Dry Research

### 現在地

### 最近の重要決定

### 最近の重要結果

### 現在の課題

### 次のアクション

---

## Wet Research

### 現在地

### 最近の重要決定

### 最近の重要結果

### 現在の課題

### 次のアクション

---

## Active ADR

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

## Important Results

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

## Open Questions

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

## Top Priority Decisions

今後1〜2週間で
決定すべき事項

---

## Risks

主要リスク

---

## Next Milestones

次のマイルストーン

---

##### Current_State_Summary Required Sections

Current_State_Summary.mdには
最低限以下を含める。

# Current State Summary

## Last Updated

## Executive Summary

現在地を5〜10行程度で要約する。

---

## Current Position

### Infrastructure

1〜5行

### Dry Research

1〜5行

### Wet Research

1〜5行

---

## Implementation Status

主要モジュールのみ記載する。

例

- FeatureContact
- FeatureDSSP
- FeaturePISA
- MergeFeatures
- FeatureRSCC

記載内容

- Status
- Overall Completion %

---

## Current Bottlenecks

重要なものを最大3件

---

## Recent Important Decisions

最大5件

---

## Recent Important Results

最大5件

---

## Top Priority Decisions

最大5件

---

## Risks

最大5件

---

## Next Milestones

最大5件

---

##### Summary Length Rule

Current_State_Summary.md は

人間の視認性を最優先する。

原則として

- Markdown表示で1〜2画面以内

または

- 150〜300行以内

とする。

詳細説明は禁止しないが、

可能な限り要約する。

詳細が必要な場合は

Current_State.md

を参照する。

---

##### Consistency Check

Current_State更新時には
以下を確認すること。

- 未反映のAccepted ADRは存在しないか
- 未反映のResultは存在しないか
- Rejected ADRが残っていないか
- Superseded ADRが残っていないか
- Open Questionsが既存ADRで既に解決されていないか
- Current_StateとADR/Result間に矛盾がないか
- Implementation StatusとCurrent_Stateの記載に乖離がないか
- Current_State.md と Current_State_Summary.md の間に矛盾がないか

---

##### Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

Implementation Statusの内容が
ADR・Resultと矛盾する場合は反映しない。

現在有効な内容のみ記載する。

この方針は
Current_State.md と Current_State_Summary.md
の両方に適用する。

---

##### Update Report

Current_State更新後に
必ず以下をレポートする。

###### Reflected ADR

Current_Stateへ反映したADR一覧

---

###### Reflected Results

Current_Stateへ反映したResult一覧

---

###### Reflected Implementation Status

参照したImplementation Status一覧

例

- FeatureContact
- FeatureDSSP
- FeaturePISA
- MergeFeatures

---

###### Not Reflected ADR

評価したが反映しなかったADR一覧

理由も記載する。

---

###### Not Reflected Results

評価したが反映しなかったResult一覧

理由も記載する。

---

###### Consistency Issues

Consistency Checkにより検出された不整合候補

---

##### Dual Dashboard Principle

Current_State.md は

AIによる研究支援を目的とした

詳細ダッシュボード

である。

Current_State_Summary.md は

人間による現在地把握を目的とした

エグゼクティブサマリー

である。

両者は同時に更新する。

Current_State_Summary.md は

Current_State.md の要約であり、

ADR・Resultの代替ではない。
