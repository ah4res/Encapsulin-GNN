# SOP-001

## Current_State Update Procedure

### Purpose

Current_State.md を最新状態へ更新する。

Current_State はプロジェクト全体の
唯一のダッシュボードとする。

---

## Location

本SOPは以下に配置する。

```text
/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/SOP
```

Current_State 更新時には
必ず本SOPを参照する。

---

## Input Documents

必ず以下を参照する。

### Required

- Project_Charter.md
- Roadmap_A_Infrastructure.md
- Roadmap_B_DryResearch.md
- Roadmap_C_WetResearch.md
- ADR/*
- Results/*

### Optional

- README.md

---

## Rules

Current_State は履歴ではない。

Current_State は

「今現在」

を表す。

過去の詳細は ADR および Result へ残す。

Current_State は

- Project_Charter
- Roadmap
- ADR
- Result

から生成される派生文書である。

---

## Required Sections

# Current State

## Project Summary

---

## Infrastructure

現在地

最近の重要決定

最近の重要結果

現在の課題

次のアクション

---

## Dry Research

現在地

最近の重要決定

最近の重要結果

現在の課題

次のアクション

---

## Wet Research

現在地

最近の重要決定

最近の重要結果

現在の課題

次のアクション

---

## Active ADR

Cursor Suggested

現在プロジェクトを支配していると考えられる
ADRを最大5件抽出する。

抽出基準

- 現在の意思決定に強く影響している
- Current_Stateの内容に直接関係する
- 現在の研究方針を規定している

例

- ADR-009 Dataset Definition
- ADR-010 Node Definition

これらは Cursor の解釈であり、
正本ではない。

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えている
Result を最大5件抽出する。

抽出基準

- 現在の研究方針に影響している
- Current_Stateの理解に重要である
- 今後の研究計画に影響している

例

- Result-000 Research Infrastructure Setup
- Result-001 Research OS Establishment

これらは Cursor の解釈であり、
正本ではない。

---

## Open Questions

Cursor Generated

Project_Charter、
Roadmap、
ADR、
Result をもとに、

現在十分に解決されていない重要課題を
3〜10件程度抽出する。

Open Questions は
正本ではない。

Current_State生成時点での
Cursorによる提案である。

以下を含めてもよい。

- 未決定の研究課題
- 将来ADRとなる可能性のある論点
- トラック間の依存関係
- 見落とされている可能性のある課題
- 将来のボトルネック

PIやCopilotがすでに認識している課題だけでなく、
Cursorが新しく発見した論点も含めてよい。

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

## Update Policy
SupersededされたADRは反映しない。
RejectedされたADRは反映しない。
Resultによって否定された仮説は
Current_Stateから除去する。
Current_State.md ファイルの編集だけであれば実行の可否を問い合わせる必要はない。
