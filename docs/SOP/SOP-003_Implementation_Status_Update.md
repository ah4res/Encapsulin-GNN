## SOP-003

### Implementation Status Update Procedure

#### Purpose

本手順は、
特徴量抽出パイプライン等の実装モジュールについて、

IMPLEMENTATION_STATUS_<Module>.md

を再現性よく生成・更新するための標準手順である。

IMPLEMENTATION_STATUSは
ADRやResultの代替ではない。

Current_State.md更新時に参照する
「実装進捗の補助資料」
として作成する。

---

#### Location

本SOPおよび生成されるIMPLEMENTATION_STATUSファイルは
以下に配置する。

/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/SOP

他のSOP（SOP-001, SOP-002）と同一ディレクトリに配置し、
通し番号で管理する（ADR-005と同様の考え方）。

生成されるIMPLEMENTATION_STATUS_<Module>.mdファイルは、
以下に配置する。

/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/Implementation

SOP本体と生成物の配置先ディレクトリは異なる。

---

#### Scope

対象は以下の2種類とする。

##### (a) ADR-018で言及される特徴量抽出モジュール・統合モジュール

例

- FeatureContact
- FeatureDSSP
- FeaturePISA
- FeatureRSCC
- MergeFeatures

将来追加されるモジュール（Evolutionary Conservation、Energy Features等）にも
同様のルールを適用する。

##### (b) `structure_tools/PDB_analysis/` 配下のその他の独立実装モジュール

ADR-018のFeature抽出パイプラインには属さないが、
Encapsulin-GNNプロジェクトの実装資産として実装状況を追跡すべきモジュール。

例

- PDB-GrepSubunits（FeatureContact/FeaturePISAの上流入力生成）
- PDB-LiteratureMining（Wet Research文献マイニング）
- PDB-VLP-list（Icosahedral Particle Atlas構築）

(b)に該当するモジュールは、ADR-018上のモジュール例示名を持たないため、
ModuleNameには実装ディレクトリ名をそのまま用いる
（File Naming Rule参照）。

---

#### Invocation Rule

本SOPは常時実行しない。

通常の実装作業、
バグ修正、
リファクタリングでは、
IMPLEMENTATION_STATUSの作成・更新を行わない。

以下のような指示が与えられた場合にのみ
本SOPを実行する。

例

- Implementation Statusを更新してください
- IMPLEMENTATION_STATUSを作成してください
- <モジュール名>の実装状況を調査してください
- SOP-003を実行してください

---

#### Source of Truth

IMPLEMENTATION_STATUSは正本ではない。

正本は以下とする。

- docs/ADR/*
- docs/Results/*

IMPLEMENTATION_STATUSの記載がADRやResultと矛盾する場合は、
ADRおよびResultを優先する。

---

#### Reconstruction Rule

既存のIMPLEMENTATION_STATUS_<Module>.mdが存在する場合、

「既存ファイルの部分編集」

ではなく、

「実装物（コード・出力）の再調査に基づく再構築」

として扱う。

既存ファイルの記載内容を
事実の根拠として利用してはならない。

これはSOP-001（Current_State）のReconstruction Ruleと同じ考え方である。

---

#### File Naming Rule

ファイル名は以下の形式とする。

IMPLEMENTATION_STATUS_<ModuleName>.md

例（Scope (a): ADR-018 Feature モジュール）

- IMPLEMENTATION_STATUS_FeatureContact.md
- IMPLEMENTATION_STATUS_FeatureDSSP.md
- IMPLEMENTATION_STATUS_FeaturePISA.md
- IMPLEMENTATION_STATUS_MergeFeatures.md

例（Scope (b): その他の独立実装モジュール）

- IMPLEMENTATION_STATUS_PDB-GrepSubunits.md
- IMPLEMENTATION_STATUS_PDB-LiteratureMining.md
- IMPLEMENTATION_STATUS_PDB-VLP-list.md

ファイル名に日付を含めない。

日付（更新履歴）はgitのコミット履歴を正本として管理する。

ModuleNameの決定方法：

- Scope (a) の場合：実装ディレクトリ名ではなく、
  ADR-018のモジュール例示名（FeatureContact等）を用いる。
  実装ディレクトリ名がADR例示名と異なる場合は、
  本文の「Module」直下に実装名・実装パスを明記する。
- Scope (b) の場合：ADR-018上の例示名を持たないため、
  実装ディレクトリ名（PDB-GrepSubunits等）をそのまま用いる。

1モジュール = 1ファイルとする。

複数モジュールを1ファイルへ統合した
IMPLEMENTATION_STATUS.md（単一ファイル）は作成しない。

---

#### Required Pre-Processing

IMPLEMENTATION_STATUS作成・更新前に、
必ず以下を実施する。

##### Step 1

対象モジュールの実装ディレクトリを特定する。

ADR-018のモジュール名と実装ディレクトリ名が異なる場合は、
対応関係をメモしておく。

##### Step 2

実装ディレクトリ配下の以下を確認する。

- *.py
- *.ipynb
- README.md
- results/* （results_<PDBID>等）
- plots/*
- 生成されたcsvファイル
- summaryファイル（summary.txt等）

##### Step 3

関連ADRを確認する。

対象：

docs/ADR/*

##### Step 4

関連Resultを確認する。

対象：

docs/Results/*

##### Step 5

複数構造（利用可能なresults_<PDBID>すべて）で
再現的に出力が生成されているかを確認する。

単一構造のみでの確認は不十分とする。

---

#### Completed判定基準

コードやNotebookの存在だけでは
Completedと判定しない。

以下が実際に確認できた機能のみ
Completedとする。

- CSV生成
- 画像生成
- summary生成

ADRで要求されているが未実装の機能は
Not Implementedへ記載する。

---

#### Template

各IMPLEMENTATION_STATUS_<Module>.mdは
以下のセクションを持つ。

```
# Implementation Status

## Module

## Purpose

## Current Status

## Completed

## In Progress

## Not Implemented

## Outputs

## Validation Status

## ADR Coverage

## Known Issues

## Next Actions

## Completion Estimate

### Current_State Summary
```

「Last Updated」セクションは設けない。
更新時期はgitのコミット履歴で確認する。

---

#### Module

Moduleセクションには以下を記載する。

- ADR-018上のモジュール名
- 実装名（実装ディレクトリ名がADR例示名と異なる場合）
- 実装パス

---

#### Current Status

以下から1つ選択する。

- Not Started
- Planning
- In Progress
- Mostly Complete
- Complete
- Maintenance

---

#### Validation Status

検証結果を要約する。

関連するResultが存在する場合は、
Result番号を明記する。

存在しない場合は、
「正式なResultは未作成」であることを明記する。

---

#### ADR Coverage

このモジュールが実装しているADRを列挙する。

正本（docs/ADR/）へのディレクトリ参照を先頭に記載する。

---

#### Next Actions

優先順位順に、

- High
- Medium
- Low

へ分類する。

---

#### Completion Estimate

以下を%で推定する。

- Design
- Implementation
- Validation
- Overall

---

#### Current_State Summary

Current_State.md更新時に重要な内容を
5〜10行で要約する。

---

#### Cross-Cutting Issues の扱い

複数モジュールに影響する内容
（例：Contact–PISAのpartner集合不一致、MergeFeatures未着手によるボトルネック）は、

関係する各モジュールファイルの
Known IssuesおよびNext Actionsに
重複して記載してよい。

全体傾向のみを要約する専用ファイル
（例：IMPLEMENTATION_STATUS_Overview.md）は
本SOPの対象外とし、
必要であれば別途Resultとして記録する。

---

#### Update Report

IMPLEMENTATION_STATUS更新後、
以下を報告する。

##### 調査対象モジュール

##### 判定が変化したモジュール（Status変化）

##### Current_Stateとの矛盾（実装は進んでいるが未着手と記載されている等）

##### 新たに検出されたKnown Issues
