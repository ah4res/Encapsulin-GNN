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

Last Updated: 2026-07-29

## Project Summary

Encapsulin-GNNは、正二十面体対称粒子形成を規定する構造原理を
Graph Neural Network（GNN）により解析し、
その予測結果をWet実験によって検証するプロジェクトである。

対象はT=1 Encapsulin（Myxococcus xanthus由来、Thermotoga maritima由来）を起点とするが、
ADR-010により解析対象データセットはEncapsulinに限定せず、
正二十面体対称粒子全般（Virus / VLP / Engineered Nanocage等）を含む
Icosahedral Particle Atlasとして構築する方針へ拡張された。

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

---

## Infrastructure

### 現在地

Research Operating System（Research OS）の運用が開始された段階。

ネットワーク・計算環境・GitHub運用・AI支援開発環境（Cursor / Copilot）の
基盤整備は概ね完了しており、Dry Research / Wet Research双方とも
具体的な開発着手が可能な状態にある。

new-HPC（GNN解析主用途）は選定・導入準備中。

Wet Research側では、PDB起点の文献マイニングパイプライン方針（ADR-009）が確立され、
`PDB-LiteratureMining`配下での実装が開始可能な状態にある。

### 最近の重要決定

- Research Operating System（Research OS）を採用する（ADR-001）
- GitHub RepositoryをSingle Source of Truthとする（ADR-002）
- Current_State.mdを唯一のダッシュボードとする（ADR-003）
- Track A / B / C の3トラック構成を採用する（ADR-004）
- ADRおよびResultは通し番号で管理する（ADR-005）
- Copilot（壁打ち・ADR作成支援）とCursor（実装・Repository参照・Current_State更新支援）を役割分担する（ADR-006）
- すべてのResultに関連ADRを記載する（ADR-007）
- Copilotとの壁打ちはProject_Charter.mdとCurrent_State.mdを標準入力とする（ADR-008）
- PDB登録構造起点の文献マイニングパイプラインを標準戦略とし、作業ディレクトリを`PDB-LiteratureMining`に固定する（ADR-009）

### 最近の重要結果

- Result-000: ネットワーク・計算環境・GitHub・Cursor・Google Colabの試験運用を開始し、
  Google Colab上でGNN学習パイプラインの初回動作を確認した。
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State / ADR / Result体系）を確立した。

### 現在の課題

- new-HPCの仕様が未確定であり、導入が完了していない
- current-HPCはCryoEM専用でGNN用途に転用しない方針のため、old-HPC（GPU性能限定的）が暫定環境
- GitHub / Cursor / Google Colabはいずれもまだ試験運用中であり、本格運用に移行していない
- ADR-009のValidation Resultsは「未実施」のままであり、初回検証対象（3DKT）のパイプラインがまだ動作確認されていない

### 次のアクション

- new-HPC仕様確定・導入
- Research OS運用の本格化（ADR・Result記録の継続）
- `PDB-LiteratureMining`にて3DKTを対象としたSingle PDB First自動化の初回検証

---

## Dry Research

### 現在地

ADR-010により、解析対象データセットの管理基盤として
「Icosahedral Particle Atlas」を構築する方針が採択された。
収集条件はEncapsulinという名称ではなく、正二十面体対称性
（Icosahedral symmetry / Point Group I / Icosahedral biological assembly /
Icosahedral EM reconstruction）とし、PDB/EMDBを対象にEncapsulin・Virus・
VLP・Engineered Nanocage等を横断的に収集する。

Result-002により、Biological Assembly情報の取得、Icosahedral対称性判定、
T-number推定（Title/Metadata優先 → Assembly推定）が実用レベルで機能することが
代表例（1A34, 1AQ3, 1AYM, 1AL0, 1WCE等）で確認された。一方で、
Caspar-Klug例外（Rotavirus/Reovirus等の多層殻粒子）、Icosahedral判定の誤検出、
Encapsulin（3DKT）のAssembly解釈の曖昧さが課題として確認された。

これを受けADR-011がT-number決定ロジック（Level 1〜4の優先順位）を提案したが、
3DKTの誤判定（assembly_subunit_count=120 → T=2と誤推定）の原因を調査した結果、
これは推定アルゴリズム自体の欠陥ではなく、
「EncA shell protein 60コピー + cargo protein 60コピー」を
区別せず合算していたことによる**学習対象粒子の定義（Dataset Eligibility）不足**が
根本原因であると判明した（ADR-013）。この判明を受け、ADR-011はADR-013へ
Superseded（置換）された。

現在は以下の2件の新しいADRが、GNN学習データセットの範囲と適格性基準を
定義しつつある。

- ADR-012（Status: Proposed）: AtlasはEncapsulin・Virus・VLPを対象として構築するが、
  GNN学習は「T=1 Encapsulin単独」→「T=1全粒子」→「T=3」→「T=1+T=3統合」の
  4段階（Phase 1〜4）で拡張する。T=4以上は当面学習対象から除外する
  （Atlasには保存するが学習には使わない）。Fold多様性（HK97 fold / Jelly-roll fold /
  その他）を積極的に利用し、Fold固有特徴と粒子形成原理を区別することを狙う。
- ADR-013（Status未記載・ドラフト段階）: GNN学習データセットをGold（Tier 1: T=1かつ
  単一Shell/Major Capsid Proteinで構成される粒子。Encapsulin, AAV, Parvovirus,
  STNV, MS2, VLP等）、Silver（Tier 2: T=3かつ単一Major Capsid Protein。MS2,
  Calicivirus, Norovirus, 植物ウイルス群等）、Future（Tier 3: T=1+T=3統合）に階層化し、
  Pseudo-T粒子（Poliovirus, Enterovirus, Rhinovirus, Coxsackievirus等）および
  多層殻粒子（Rotavirus, Reovirus等）を当面除外する方針を示す。
  ただし本文書はRationale・Alternatives Considered・Status・Next Actionが
  未記載のまま途中で終わっており、正式な意思決定としては未確定である。

（Cursor所見・未Result化）実装リポジトリ `PDB-VLP-list` では、Superseded前の
ADR-011方針に沿ってNotebook 01〜07およびsrc配下のapi/database/analysis/export
ライブラリが構築され、RCSB検索でPoint Group I構造1,712件を取得、全件について
Title/Assembly優先のT-number推定バッチ処理を実行済みである（単体テストで検証）。
この結果、Encapsulin候補としてT=1: 37件、T=3: 5件が暫定抽出されているが、
これはADR-013のTier基準（単一Shell/Capsid Protein限定、cargo protein等の除外）を
反映しておらず、Tier1/Tier2データセットとしてそのまま採用できるかは未検証である。
またこの進捗はまだResultとして正式記録されておらず、正本には未反映である。

Dataset Construction（B1）は、収集技術面の検証（Result-002）を経て、
学習対象の適格性基準（ADR-012/ADR-013）を定義する段階に進んだが、
両ADRとも未確定（Proposed／ドラフト）であり、B1完了条件（解析対象構造の決定）には
未到達である。Graph Representation Design（B3）の正式な着手前段階にある。

### 最近の重要決定

- 解析対象をEncapsulinに限定せず、正二十面体対称粒子全般を収集する
  Icosahedral Particle Atlasを構築する（ADR-010）
- T-number決定ロジック（Level1〜4優先順位）を定めたADR-011は、
  3DKT誤判定の根本原因がDataset Eligibility不足にあったとの判明を受け、
  ADR-013によりSuperseded（置換）された
- GNN学習はT=1 Encapsulin単独から段階的にT=1全粒子・T=3・T=1+T=3統合へ拡張し、
  T=4以上は当面学習対象から除外する（ADR-012、Status: Proposed）
- GNN学習データセットをGold（T=1・単一Shell/Capsid Protein）／Silver（T=3・単一
  Capsid Protein）／Future（T=1+T=3統合）のTierに階層化し、Pseudo-T粒子・
  多層殻粒子を除外する（ADR-013、ドラフト・Status未記載）

### 最近の重要結果

- Result-002: Icosahedral対称性取得・Biological Assembly情報取得・T-number推定が
  実用レベルで機能することを確認した。一方でCaspar-Klug例外、対称性誤検出、
  Encapsulin assembly解釈の曖昧さという課題も確認された（この課題はADR-012/013の
  発端となった）。
- （未Result化）`PDB-VLP-list`実装においてPhase 1（Notebook 01〜07、ライブラリ化、
  1,712件の全件T-number推定バッチ実行）が完了し、Encapsulin候補（T=1: 37件、
  T=3: 5件）が暫定抽出された。ただしADR-013のTier基準に基づく再評価は未実施。

### 現在の課題

- ADR-013が未完成（Rationale・Alternatives Considered・Status・Next Action未記載）
  であり、正式な意思決定として確定していない
- ADR-012もStatus: Proposedのままであり、Accepted判断が行われていない
- 暫定抽出されたEncapsulin候補（T=1: 37件、T=3: 5件）がADR-013のTier基準
  （単一Shell/Capsid Protein限定、cargo protein等の除外）を満たすか未検証であり、
  B1完了条件（解析対象構造の決定）に対する最終採否ができない
- Result-002で指摘されたIcosahedral判定の誤検出（Cyclic/C2構造の誤分類）の
  修正状況が未確認
- Pseudo-T粒子・多層殻粒子の除外ロジックが実装（`PDB-VLP-list`）に反映されているか未確認
- PDB-EMDB対応付け、粒子分類ルールの全件適用、SQLite DBへの本番統合が未完了
- B2 Structure Feature Engineering（buried surface area等）は未着手
- B3 Graph Representation Design（ノード・エッジ・属性の正式定義）は未着手
- 実装（コード）の進捗速度に対し、ADR/Result記録が追いついていない

### 次のアクション

- ADR-013を完成させ（Rationale/Alternatives/Next Action記載）、Statusを確定する
- ADR-012のStatus確定（Accepted判断）
- ADR-013のTier基準（Gold/Silver/Exclusion）に基づき、`PDB-VLP-list`実装側で
  Shell Protein Firstの原則を反映した再分類・再抽出を実施
- Icosahedral判定誤検出の修正確認
- `PDB-VLP-list`実装進捗のResult化（Result-003候補）
- B2 Structure Feature Engineering / B3 Graph Representation Designの着手検討

---

## Wet Research

### 現在地

ADR-009により、PDB登録構造起点の文献マイニングを標準戦略とし、
Wet検証系として以下の2種類のEncapsulinを構築する方針が決定された。

- Thermotoga maritima Encapsulin（T=1）
- Myxococcus xanthus Encapsulin（T=3）

初期対象PDBは3DKT、4PT2、7MU1、8VJOとし、Cargo共発現系ではなく
Shell protein単独発現系を優先する。実装はNotebook First / Single PDB First
戦略に基づき、まず3DKTを対象とした自動化パイプライン
（PDB → DOI取得 → 論文取得 → PDF保存 → Methods抽出 → Evidence付きMetadata生成）の
検証を行う計画だが、Validation Resultsは「未実施」のままであり、
Gene Preparation（C1）着手前の段階にある。

### 最近の重要決定

- PDB起点の文献マイニングをWet実験系構築の標準戦略とし、
  Thermotoga maritima（T=1）とMyxococcus xanthus（T=3）の2系統を
  初期Wet検証対象とする（ADR-009）

### 最近の重要結果

現時点でWet Research固有のResultは無い。

### 現在の課題

- 実験系（遺伝子・発現ベクター）の構築が未着手
- ADR-009のValidation Results（3DKTを対象とした自動化パイプライン検証）が未実施

### 次のアクション

- `PDB-LiteratureMining`にて3DKTを対象としたSingle PDB First自動化の検証
- 検証成功後、4PT2 / 7MU1 / 8VJOへの拡張とBatch処理の実装
- C1 Gene Preparation着手の検討（Dry ResearchでのDataset確定後を想定）

---

## Active ADR

Cursor Suggested

現時点でプロジェクト全体を支配していると考えられるADR（最大5件）。
これらはCursorの解釈であり、正本ではない。

- ADR-010: Icosahedral Particle Atlasを採用し、解析対象をEncapsulin限定から
  正二十面体対称粒子全般へ拡張する
- ADR-013: GNN学習データセットをGold（T=1）/Silver（T=3）/Future（T=1+T=3）の
  Tierに階層化し、Pseudo-T粒子・多層殻粒子を除外する（ドラフト・Status未記載）
- ADR-012: GNN学習をT=1 Encapsulin単独から段階的にT=1全粒子・T=3・統合へ拡張し、
  T=4以上を当面除外する（Status: Proposed）
- ADR-009: PDB起点の文献マイニングパイプラインとWet検証系（T=1/T=3 Encapsulin）
  の方針を採用する
- ADR-006: Copilotは壁打ち・ADR作成支援、Cursorは実装・Repository参照・
  Current_State更新支援を担う

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えていると考えられるResult（最大5件）。
これらはCursorの解釈であり、正本ではない。

- Result-002: Icosahedral Particle Atlas構築の基盤技術（Assembly情報取得・
  Icosahedral対称性判定・T-number推定）が実用レベルで機能することを確認。
  Caspar-Klug例外・対称性誤検出・Encapsulin assembly解釈という課題も確認した。
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State /
  ADR / Result体系、3トラック構成、AI役割分担）の確立
- Result-000: Research OS導入以前の研究基盤整備、およびGoogle Colab上での
  GNN学習パイプライン初回動作確認

---

## Open Questions

Cursor Generated

Project_Charter、Roadmap、ADR、Resultをもとに、
現時点で十分に解決されていないと考えられる論点（Cursorによる提案であり、正本ではない）。

- ADR-013はRationale・Alternatives・Status・Next Actionが未記載のドラフトで
  中断しているが、いつ、誰がこれを完成させ確定するか
- ADR-012のStatus（Proposed）をAcceptedにするための条件・判断基準は何か
- 暫定抽出されたEncapsulin候補（T=1: 37件、T=3: 5件）は、ADR-013のTier基準
  （単一Shell/Capsid Protein限定）に照らして再分類・再抽出が必要か
- Fold Diversity Strategy（HK97 fold / Jelly-roll fold / Other）を
  Atlas実装・分類ロジックにどう反映するか
- Pseudo-T粒子・多層殻粒子の除外を実装（`PDB-VLP-list`）レベルでどう反映するか
- Result-002で指摘されたIcosahedral判定の誤検出（Cyclic/C2の誤分類）を
  どのように修正するか
- 実装（コード）がADR/Result記録より先行している状況をどう解消するか
  （Result-003作成のタイミング）
- new-HPCの具体的な仕様（GPU構成・メモリ容量等）をいつ、どのように確定するか（A5/A6）
- `PDB-LiteratureMining`側の3DKT検証はいつ完了するか、B1（Dataset確定）と
  C1（Gene Preparation）の依存関係をどう管理するか
- GitHub / Cursor / Google Colabの試験運用を、いつ・どのような基準で
  本格運用へ移行するか

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- ADR-013を完成させ、Status（Accepted等）を確定する
- ADR-012のStatus確定（Accepted判断）
- 暫定Encapsulin候補データセット（T=1: 37件、T=3: 5件）のADR-013 Tier基準に
  基づく再評価・採否判断（B1完了条件）
- new-HPCの仕様（GPU構成・メモリ容量）確定
- `PDB-LiteratureMining`における3DKT初回検証の実施

---

## Risks

- new-HPC導入遅延により、Dry Research（GNN解析）の本格開始が遅れる可能性がある
- 現有計算資源のうち、current-HPCはCryoEM専用、old-HPCはGPU性能が限定的であり、
  GNN開発の暫定環境として能力不足のリスクがある
- GitHub / Cursor運用が試験運用段階に留まっており、記録の抜け漏れが生じるリスクがある
- 実装（コード）の進捗がADR/Result記録より先行しており、意思決定の
  追跡可能性（Research OS本来の目的）が損なわれるリスクがある
- Icosahedral判定の誤検出（Result-002指摘）が未修正のままデータセットが
  確定した場合、後続のGNN解析全体の妥当性に影響するリスクがある
- ADR-013が未完成（ドラフト中断）のままの状態が続くと、学習対象の適格性基準が
  確定せず、B1 Dataset Constructionの完了がさらに遅延するリスクがある
- ADR-013のTier基準（Shell Protein First等）が確定した際、既存の暫定抽出済み
  データ（Cursor所見のEncapsulin候補等）に手戻りが発生するリスクがある

---

## Next Milestones

- Research OS正式運用の定着（ADR・Result記録の継続的更新、実装との同期）
- ADR-012 / ADR-013のStatus確定
- Tier 1（Gold Dataset）データセットの確定（B1完了条件の具体化）
- new-HPC導入完了
- Dataset Construction完了（Encapsulin候補データセットの確定を含む、B1完了条件）
- `PDB-LiteratureMining` 3DKT初回検証の完了
- Graph Builder完成（全構造のグラフ化、B3完了条件）

---

## Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

現在有効な内容のみ記載する。
