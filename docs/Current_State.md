WARNING

このファイルは派生文書である。

正本は

- ADR
- Results
- Roadmap

である。

Current_Stateが矛盾する場合は
正本を優先する。

---

# Current State

Last Updated: 2026-07-27

## Project Summary

Encapsulin-GNNは、正二十面体対称粒子形成を規定する構造原理を
Graph Neural Network（GNN）により解析し、
その予測結果をWet実験によって検証するプロジェクトである。

対象はT=1 Encapsulin（Myxococcus xanthus由来、Thermotoga maritima由来）。

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

---

## Infrastructure

### 現在地

Research Operating System（Research OS）の運用が開始された段階。

ネットワーク・計算環境・GitHub運用・AI支援開発環境（Cursor / Copilot）の
基盤整備は概ね完了しており、Dry Research着手可能な状態にある。

new-HPC（GNN解析主用途）は選定・導入準備中。

### 最近の重要決定

- Research Operating System（Research OS）を採用する（ADR-001）
- GitHub RepositoryをSingle Source of Truthとする（ADR-002）
- Current_State.mdを唯一のダッシュボードとする（ADR-003）
- Track A / B / C の3トラック構成を採用する（ADR-004）
- ADRおよびResultは通し番号で管理する（ADR-005）
- Copilot（壁打ち・ADR作成支援）とCursor（実装・Repository参照・Current_State更新支援）を役割分担する（ADR-006）
- すべてのResultに関連ADRを記載する（ADR-007）
- Copilotとの壁打ちはProject_Charter.mdとCurrent_State.mdを標準入力とする（ADR-008）

### 最近の重要結果

- Result-000: ネットワーク・計算環境・GitHub・Cursor・Google Colabの試験運用を開始し、
  Google Colab上でGNN学習パイプラインの初回動作を確認した。
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State / ADR / Result体系）を確立した。

### 現在の課題

- new-HPCの仕様が未確定であり、導入が完了していない
- current-HPCはCryoEM専用でGNN用途に転用しない方針のため、old-HPC（GPU性能限定的）が暫定環境
- GitHub / Cursor / Google Colabはいずれもまだ試験運用中であり、本格運用に移行していない

### 次のアクション

- new-HPC仕様確定・導入
- Research OS運用の本格化（ADR・Result記録の継続）
- Dataset Construction（Roadmap B1）着手

---

## Dry Research

### 現在地

Google Colab上でGNNプロトタイプの初回実行に成功し、
学習パイプラインが動作することを確認した段階。

初回プロトタイプの構造表現は以下の通り（正式決定ではない）。

- Node: アミノ酸残基
- Node Feature: アミノ酸種類
- Edge: Cα距離10Å未満

Dataset Construction（B1）およびGraph Representation Design（B3）の
正式な着手前段階にある。

### 最近の重要決定

現時点でDry Research固有のADRは無い。

### 最近の重要結果

- Result-000: Google Colab上でGNN学習パイプラインの初回動作を確認した。
  この成功によりDry Research開始可能な状態となった。

### 現在の課題

- 解析対象とするEncapsulin構造データセットが未確定（B1未完了）
- ノード・エッジ・属性の正式な定義が未決定（B3未着手）
- 粒子形成関連特徴量（buried surface area、hydrophobic interaction等）の抽出パイプライン未整備（B2未着手）

### 次のアクション

- B1 Dataset Construction: 解析対象Encapsulin構造一覧・文献一覧の確定
- B2 Structure Feature Engineering: 特徴量抽出パイプラインの検討
- B3 Graph Representation Design: ノード・エッジ・属性定義の正式決定

---

## Wet Research

### 現在地

未着手。Gene Preparation（C1）以前の段階。

### 最近の重要決定

現時点でWet Research固有のADRは無い。

### 最近の重要結果

現時点でWet Research固有のResultは無い。

### 現在の課題

- 実験系（遺伝子・発現ベクター）の構築が未着手

### 次のアクション

- C1 Gene Preparation着手の検討（Dry ResearchでのDataset確定後を想定）

---

## Active ADR

Cursor Suggested

現時点でプロジェクト全体を支配していると考えられるADR（最大5件）。
これらはCursorの解釈であり、正本ではない。

- ADR-001: Research Operating System（Research OS）を採用する
- ADR-002: GitHub RepositoryをSingle Source of Truthとする
- ADR-003: Current_State.mdを唯一のダッシュボードとする
- ADR-004: Track A / B / C の3トラック構成を採用する
- ADR-006: Copilotは壁打ち・ADR作成支援、Cursorは実装・Repository参照・Current_State更新支援を担う

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えていると考えられるResult（最大5件）。
これらはCursorの解釈であり、正本ではない。

- Result-000: Research OS導入以前の研究基盤（ネットワーク・計算環境・GitHub・Cursor・Colab）整備、およびGoogle Colab上でのGNN学習パイプライン初回動作確認
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State / ADR / Result体系、3トラック構成、AI役割分担）の確立

---

## Open Questions

Cursor Generated

Project_Charter、Roadmap、ADR、Resultをもとに、
現時点で十分に解決されていないと考えられる論点（Cursorによる提案であり、正本ではない）。

- new-HPCの具体的な仕様（GPU構成・メモリ容量等）をいつ、どのように確定するか（A5/A6）
- 解析対象とするEncapsulin構造（PDBエントリ）の範囲をどのように決定するか（B1）
- ノード・エッジ・属性定義を含むGraph Representationをどう設計するか（B3、将来ADR化される可能性がある論点）
- GNNモデル選定（GCN/GAT等、B4）をどのような基準で進めるか
- old-HPC（GPU性能限定的）がDataset Construction / Feature Engineeringの進行速度に与える影響をどう見積もるか
- Dry Researchのどの段階でWet Research（C1 Gene Preparation）に着手するか、トラック間の依存関係をどう管理するか
- GitHub / Cursor / Google Colabの試験運用を、いつ・どのような基準で本格運用へ移行するか

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- new-HPCの仕様（GPU構成・メモリ容量）確定
- 解析対象とするEncapsulin構造（PDBエントリ）の範囲確定（B1）
- Graph表現（ノード・エッジ・属性定義）の正式決定（B3）

---

## Risks

- new-HPC導入遅延により、Dry Research（GNN解析）の本格開始が遅れる可能性がある
- 現有計算資源のうち、current-HPCはCryoEM専用、old-HPCはGPU性能が限定的であり、
  GNN開発の暫定環境として能力不足のリスクがある
- GitHub / Cursor運用が試験運用段階に留まっており、記録の抜け漏れが生じるリスクがある

---

## Next Milestones

- Research OS正式運用の定着（ADR・Result記録の継続的更新）
- new-HPC導入完了
- Dataset Construction完了（解析対象構造の決定、B1完了条件）
- Graph Builder完成（全構造のグラフ化、B3完了条件）

---

## Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

現在有効な内容のみ記載する。
