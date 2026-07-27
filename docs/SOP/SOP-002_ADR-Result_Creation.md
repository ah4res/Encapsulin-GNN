# SOP-002

## ADR and Result Creation Procedure

### Purpose

本手順は、壁打ち・研究活動・実験・解析の結果を Research OS へ記録するための標準手順である。

本SOPの対象は以下とする。

- ADR（Architecture Decision Record）
- Result

本SOPは Copilot による ADR および Result 草案生成の標準ルールを定義する。

---

# Input Documents

壁打ち開始時には以下を参照する。

## Required

- Project_Charter.md
- Current_State.md

## Optional

必要に応じて参照する。

- 関連ADR
- 関連Result
- 関連Roadmap

---

# Output Rules

壁打ち終了後、以下のいずれかを出力する。

- ADR案
- Result案
- ADR不要
- Result不要

出力はMarkdown形式とする。

---

# Invocation Rule

本SOPは常時実行しない。

通常の研究相談、アイデア検討、文献調査、壁打ちでは、
ADRおよびResultの必要性について判断しない。

ADRまたはResultの作成は、
ユーザーから明示的な要求があった場合のみ実施する。

以下のような指示が与えられた場合にのみ
本SOPを実行する。

例

- ADRとしてまとめてください
- Resultとしてまとめてください
- ADR案を作成してください
- Result案を作成してください
- 記録化してください
- SOP-002を実行してください

上記の指示がない場合は、
通常の壁打ちや研究相談として対応し、
ADRおよびResultの生成や要否判定は行わない。

本SOPは、

「議論モード」

ではなく

「記録モード」

に切り替えるための手順書である。

---

# ADR

## Definition

ADR（Architecture Decision Record）は、

プロジェクトにおける重要な意思決定を記録する文書である。

対象はソフトウェア開発に限定しない。

以下もADRとして扱う。

- 研究方針
- 実験方針
- データセット方針
- モデル選択
- 評価方針
- Wet実験戦略
- 検証戦略

---

## ADRを書く基準

### 記録する

- ノード定義
- エッジ定義
- 特徴量定義
- モデル選択
- 学習方針
- 評価方針
- Wet実験方針
- 検証戦略
- 研究上重要な判断

### 記録しない

- 軽微な実装変更
- バグ修正
- ファイル整理
- 一時的試行
- 日常作業

---

## ADR作成条件

以下を満たした場合のみADRを提案する。

- 明確な意思決定が存在する
- 今後の研究方針へ影響する
- 1か月後に見返す価値がある

条件を満たさない場合は

ADR不要

と出力する。

---

## ADR Template

### ADR-XXX

Date

Track

Question

Decision

Rationale

Alternatives Considered

Status

Validation Results

---

## Track

必ず以下のいずれかを選択する。

### Track A

Infrastructure

例

- GitHub
- HPC
- Cursor
- Colab
- Research OS

---

### Track B

Dry Research

例

- Dataset
- Feature
- GNN
- Learning

---

### Track C

Wet Research

例

- Cloning
- Expression
- Purification
- Mutagenesis
- Validation

---

## Status

以下のみ使用する。

### Proposed

議論中

---

### Trial

試験運用中

---

### Accepted

採用済み

---

### Rejected

却下

---

### Superseded → ADR-XXX

後続ADRに置換済み

---

# Result

## Definition

Resultは、

何を行い

何が分かったか

を記録する文書である。

Resultは実験ノートではない。

研究方針に影響する成果のみを対象とする。

---

## Resultを書く基準

### 記録する

- GNN性能評価
- モデル比較
- 特徴量比較
- データセット評価
- 変異体評価
- 粒子形成評価
- AI予測の検証結果
- Infrastructure構築成果

### 記録しない

- 日常作業
- 作業ログ
- 軽微な設定変更
- 一時的試行

---

## Result作成条件

以下を満たした場合のみResultを提案する。

- 新しい知見が得られた
- 研究計画に影響する
- 将来参照する価値がある

条件を満たさない場合は

Result不要

と出力する。

---

## Result Template

### Result-XXX

Date

Track

Related ADR

Objective

Method

Result

Interpretation

Conclusion

Next Action

---

## Related ADR

原則として、

すべてのResultは関連するADRを1件以上持つ。

例

ADR-009

ADR-011

---

### 例外

Result-000

Research OS導入前の環境整備結果を記録する特例Resultとする。

---

# Copilot Output Requirements

本SOPは Invocation Rule に該当する
明
