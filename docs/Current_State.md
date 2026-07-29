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

Result-003の系統解析により、初期GNN学習はT=1 Encapsulin単独および
T=1 Virusの二本立てで開始する方針が固まり、Wet Research側もADR-014により
T. maritima / M. xanthus 両Encapsulinの初期構築体・発現戦略が具体化された。

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

Wet Research側で計画していたPDB起点の自動文献マイニングパイプライン
（ADR-009、`PDB-LiteratureMining`）は、対象がT. maritima / M. xanthusの
2系統に絞られたことを受け、パイプライン自動化ではなく手動文献調査で
運用可能と判断され、closeとなった（実際の文献調査はResult-004として
手動で実施・完了している）。

### 最近の重要決定

- Research Operating System（Research OS）を採用する（ADR-001）
- GitHub RepositoryをSingle Source of Truthとする（ADR-002）
- Current_State.mdを唯一のダッシュボードとする（ADR-003）
- Track A / B / C の3トラック構成を採用する（ADR-004）
- ADRおよびResultは通し番号で管理する（ADR-005）
- Copilot（壁打ち・ADR作成支援）とCursor（実装・Repository参照・Current_State更新支援）を役割分担する（ADR-006）
- すべてのResultに関連ADRを記載する（ADR-007）
- Copilotとの壁打ちはProject_Charter.mdとCurrent_State.mdを標準入力とする（ADR-008）
- PDB起点の自動文献マイニングパイプライン方針（ADR-009）は、対象系統が
  2系統のみであるため手動調査で十分と判断され、close（運用終了）となった

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

---

## Dry Research

### 現在地

ADR-010により、解析対象データセットの管理基盤として
「Icosahedral Particle Atlas」を構築する方針が採択された。
収集条件はEncapsulinという名称ではなく、正二十面体対称性
（Icosahedral symmetry / Point Group I / Icosahedral biological assembly /
Icosahedral EM reconstruction）とし、PDB/EMDBを対象にEncapsulin・Virus・
VLP・Engineered Nanocage等を横断的に収集する。

Result-002でAtlas構築の基盤技術（Assembly情報取得・T-number推定）が
実用レベルで機能することが確認された後、3DKTのT-number誤判定の原因究明を
通じて、T-number推定は単なるアルゴリズムの問題ではなく学習対象粒子の
定義（Dataset Eligibility）の問題であることが判明した。この結果、
T-number決定ロジックを提案したADR-011はADR-013へSupersededされ、
現在はADR-012（GNN学習の段階的拡張戦略）とADR-013（Gold/Silver/Future Tierに
よるデータセット適格性基準）の2つのADRがデータセット構築の方針を規定している。

Result-003では、Atlas由来のGold Dataset（T=1）・Silver Dataset（T=3）を対象に
Shell protein配列に基づく系統樹解析を実施した。Atlas全体（646構造、
CD-HIT後241クラスター、T=1: 403件、T=3: 243件）ではEncapsulin/Virus/VLPおよび
T=1/T=3が明確なクレードに分離しなかった一方、Encapsulinのみに絞った解析
（48構造、T=1 Encapsulin 40件、T=3 Encapsulin 8件、23種、18 shell protein）では、
T=1 Encapsulinは複数クレードに分散し比較的多様である一方、T=3 Encapsulinは
サンプル数が少なく特定系統に偏っていることが確認された。

この結果を受け、ADR-012（Status: Accepted、Result-003で検証済み）は
「Phase 1: T=1 Encapsulin単独 → Phase 2: T=1 Icosahedral Particle Dataset
（Encapsulin+Virus+VLP） → Phase 3: T=3 Dataset（追加データ収集後）→
Phase 4: T=1+T=3統合」という段階的戦略を維持し、初期GNN解析は
「Dataset A: T=1 Encapsulin」と「Dataset B: T=1 Virus」の二本立てで
開始する方針が確定した。T=3 Encapsulinは直ちに学習対象とせず、
BLAST/DALI/MATRASによる追加構造探索の対象とする。

ADR-013（Gold/Silver/Future Tierの定義、Pseudo-T粒子・多層殻粒子の除外方針）は
Result-003の検証結果（Validation Results追記済み: 「T=3 Encapsulinのデータ
多様性不足が確認された。初期学習はGold Dataset(T=1)を優先する」）により
方向性は支持されているが、文書自体はRationale・Alternatives Considered・
Status・Next Actionが未記載のまま中断しており、正式なStatus確定には
至っていない。

（Cursor所見・未Result化）実装リポジトリ `PDB-VLP-list` では、Phase 1実装
（Notebook 01〜07、api/database/analysis/exportライブラリ）が構築され、
Point Group I構造1,712件のT-number推定バッチ処理を実行済みである。
Result-003のEncapsulin集計（T=1: 40件、T=3: 8件、計48件）は、この実装で
暫定抽出されていた数値（T=1: 37件、T=3: 5件）から更新された、より精緻な値と
みられるが、両者の対応関係（再分類・追加抽出の詳細）はまだResultとして
明文化されていない。

### 最近の重要決定

- 解析対象をEncapsulinに限定せず、正二十面体対称粒子全般を収集する
  Icosahedral Particle Atlasを構築する（ADR-010）
- T-number決定ロジック（Level1〜4優先順位）を定めたADR-011は、
  3DKT誤判定の根本原因がDataset Eligibility不足にあったとの判明を受け、
  ADR-013によりSuperseded（置換）された
- GNN学習はT=1 Encapsulin単独（Phase1）→ T=1全粒子（Phase2）→ T=3（Phase3）→
  T=1+T=3統合（Phase4）の順で段階的に拡張し、T=4以上は当面除外する
  （ADR-012、**Status: Accepted**、Result-003により検証済み）
- 初期GNN解析はDataset A（T=1 Encapsulin）とDataset B（T=1 Virus）の
  二本立てとし、T=3 Encapsulinは追加データ収集まで学習対象から除外する
  （Result-003の結論、ADR-012の運用方針として反映）
- GNN学習データセットをGold（T=1）／Silver（T=3）／Future（T=1+T=3統合）の
  Tierに階層化し、Pseudo-T粒子・多層殻粒子を除外する
  （ADR-013、ドラフト・Status未記載だがResult-003により方向性は支持）

### 最近の重要結果

- Result-002: Icosahedral対称性取得・Biological Assembly情報取得・T-number推定が
  実用レベルで機能することを確認した。Caspar-Klug例外・対称性誤検出・
  Encapsulin assembly解釈の曖昧さという課題も確認された（ADR-012/013の発端）。
- Result-003: Atlas全体（646構造）およびEncapsulin限定（48構造）の系統樹解析を実施。
  T=3 Encapsulinのデータ多様性不足を確認し、初期GNN学習をDataset A（T=1 Encapsulin）
  とDataset B（T=1 Virus）の二本立てとする方針を導いた。
- （未Result化）`PDB-VLP-list`実装においてPhase 1（Notebook 01〜07、ライブラリ化、
  1,712件の全件T-number推定バッチ実行）が完了している。

### 現在の課題

- ADR-013が未完成（Rationale・Alternatives Considered・Status・Next Action未記載）
  であり、Result-003による裏付けはあるものの正式なStatusが確定していない
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の最終的な構造リストが
  未確定であり、B1完了条件（解析対象構造の決定）に到達していない
- Result-002で指摘されたIcosahedral判定の誤検出（Cyclic/C2構造の誤分類）の
  修正状況が未確認
- Result-003のEncapsulin集計（T=1:40件, T=3:8件）と、`PDB-VLP-list`実装での
  暫定抽出値（T=1:37件, T=3:5件）との差分・対応関係が明文化されていない
- Fold分類（HK97 / Jelly-roll / Other）が未実装であり、Dataset Bの構築に必要
- T=3 Encapsulinの追加構造探索（BLAST/DALI/MATRAS）が未着手
- PDB-EMDB対応付け、粒子分類ルールの全件適用、SQLite DBへの本番統合が未完了
- B2 Structure Feature Engineering（buried surface area等）は未着手
- B3 Graph Representation Design（ノード・エッジ・属性の正式定義）は未着手

### 次のアクション

- ADR-013を完成させ（Rationale/Alternatives/Next Action記載）、Statusを確定する
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の構造リストを確定する
- Fold分類（HK97 / Jelly-roll / Other）の実装
- 初期GNNベースラインモデルの構築（Dataset A優先）
- T=3 Encapsulin候補の追加構造探索（BLAST/DALI/MATRAS）
- Icosahedral判定誤検出の修正確認
- `PDB-VLP-list`実装進捗（Phase 1完了、1,712件バッチ処理）のResult化

---

## Wet Research

### 現在地

ADR-014（Status: Accepted）により、初期Wet検証系の構築方針が具体化された。
Result-004の文献調査（3DKT, 7MU1, 7KQ5, 7K5W / 4PT2, 7S20, 8VJO）に基づき、
以下の構築体・発現宿主が確定している。

- Thermotoga maritima Encapsulin（T=1、PDB: 3DKT Chain A, Maritimacin）
  - Construct-Tm-01: WT, Tag-free
  - Construct-Tm-02: WT, C-terminal His6
  - ベクター: pET28
- Myxococcus xanthus EncA（T=3、PDB: 8VJO Chain A）
  - Construct-Mx-01: WT, N-terminal His6-TEV
  - ベクター: 自作 pET21 N-His-TEV
- 共通発現宿主: E. coli BL21(DE3) CodonPlus-RILP

変異体作製に先立ち、WT粒子形成・熱安定性（DSF）・Heat Challenge耐性を
評価するWT Stage Success Criteria（T. maritima 10項目、M. xanthus 5項目）が
定義されているが、これらはまだ計画段階であり、実験室での実行（クローニング・
発現・精製・評価）はいずれも未着手である。

ADR-009（PDB起点の自動文献マイニングパイプライン）はcloseとなり、
`PDB-LiteratureMining`による自動化ではなく、手動文献調査（Result-004）で
運用する方針に変更された。

### 最近の重要決定

- 初期Wet検証系としてT. maritima Encapsulin（Tag-free / C-terminal His6の
  2構築体）とM. xanthus EncA（N-terminal His6-TEV）を採用し、共通発現宿主を
  BL21(DE3) CodonPlus-RILPとする（ADR-014、Accepted）
- 変異体作製前にWT粒子形成・熱安定性・Heat Challenge耐性を評価する
  WT Stage Success Criteriaを定義する（ADR-014）
- PDB起点の自動文献マイニングパイプライン方針（ADR-009）はcloseとし、
  手動文献調査（2系統のみのため）で運用する

### 最近の重要結果

- Result-004: T. maritima Encapsulin（3DKT, 7MU1, 7KQ5, 7K5W）およびM. xanthus
  EncA（4PT2, 7S20, 8VJO）の既報構築体・発現条件・精製条件を調査し、
  初期構築体（Construct-Tm-01/02, Construct-Mx-01）と発現・精製戦略を確定した。
  この結果はADR-014の正本的根拠となっている。

### 現在の課題

- Construct-Tm-01/02、Construct-Mx-01の遺伝子合成・クローニングが未着手
  （C1 Gene Preparation未開始）
- WT Stage Success Criteria（T. maritima 10項目、M. xanthus 5項目）は
  定義されたのみで、実験による達成はまだ一件も無い
- Dry Research側のDataset確定（B1）を待たずにWet実験計画（ADR-014）が
  先行して具体化されており、両トラックの進行速度の差をどう管理するか未整理

### 次のアクション

- C1 Gene Preparation着手: Construct-Tm-01/02、Construct-Mx-01の遺伝子合成・
  クローニング
- 発現・精製ワークフロー（硫安沈殿→SEC／Ni-NTA→SEC）の立ち上げ
- WT粒子形成評価（TEM/DLS）、熱安定性評価（DSF）、Heat Challenge評価の実施

---

## Active ADR

Cursor Suggested

現時点でプロジェクト全体を支配していると考えられるADR（最大5件）。
これらはCursorの解釈であり、正本ではない。

- ADR-012: GNN学習をT=1 Encapsulin単独から段階的に拡張する戦略
  （Status: Accepted、Result-003で検証済み）
- ADR-014: Wet Research初期検証系（構築体・発現宿主・WT評価基準）
  （Status: Accepted）
- ADR-010: Icosahedral Particle Atlasを採用し、解析対象をEncapsulin限定から
  正二十面体対称粒子全般へ拡張する
- ADR-013: GNN学習データセットをGold（T=1）/Silver（T=3）/Future（T=1+T=3）の
  Tierに階層化し、Pseudo-T粒子・多層殻粒子を除外する
  （ドラフト・Status未記載だがResult-003で方向性は支持）
- ADR-006: Copilotは壁打ち・ADR作成支援、Cursorは実装・Repository参照・
  Current_State更新支援を担う

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えていると考えられるResult（最大5件）。
これらはCursorの解釈であり、正本ではない。

- Result-003: Atlas全体およびEncapsulin限定の系統樹解析により、T=3 Encapsulinの
  データ多様性不足を確認し、初期GNN学習をDataset A（T=1 Encapsulin）/
  Dataset B（T=1 Virus）の二本立てとする方針を導いた。
- Result-004: T. maritima / M. xanthus Encapsulinの既報構築体・発現・精製条件を
  調査し、初期Wet検証系（ADR-014）の根拠となった。
- Result-002: Icosahedral Particle Atlas構築の基盤技術（Assembly情報取得・
  Icosahedral対称性判定・T-number推定）が実用レベルで機能することを確認。
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State /
  ADR / Result体系、3トラック構成、AI役割分担）の確立
- Result-000: Research OS導入以前の研究基盤整備、およびGoogle Colab上での
  GNN学習パイプライン初回動作確認

---

## Open Questions

Cursor Generated

Project_Charter、Roadmap、ADR、Resultをもとに、
現時点で十分に解決されていないと考えられる論点（Cursorによる提案であり、正本ではない）。

- ADR-013はResult-003による裏付けがあるが、Rationale・Alternatives・Status・
  Next Actionが未記載のまま中断している。いつ、誰がこれを完成させ確定するか
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の最終構造リストと
  `PDB-VLP-list`実装の暫定抽出値（T=1:37件/T=3:5件）およびResult-003の集計値
  （T=1:40件/T=3:8件）との差分をどう整合させるか
- Fold Diversity Strategy（HK97 fold / Jelly-roll fold / Other）を
  Atlas実装・分類ロジックにどう反映するか
- T=3 Encapsulinの追加構造探索（BLAST/DALI/MATRAS）はいつ、どのように実施するか
- Wet Research（ADR-014、Construct確定済み）がDry Research（B1未完了）より
  先行して具体化しているが、C1 Gene PreparationをDataset確定前に着手してよいか
- WT Stage Success Criteria（T. maritima 10項目、M. xanthus 5項目）の
  実施体制・スケジュールをどう組むか
- Result-002で指摘されたIcosahedral判定の誤検出（Cyclic/C2の誤分類）を
  どのように修正するか
- new-HPCの具体的な仕様（GPU構成・メモリ容量等）をいつ、どのように確定するか（A5/A6）
- GitHub / Cursor / Google Colabの試験運用を、いつ・どのような基準で
  本格運用へ移行するか

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- ADR-013を完成させ、Status（Accepted等）を確定する
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の構造リストの確定（B1完了条件）
- C1 Gene Preparation着手可否の判断（Dataset確定を待つか、並行して開始するか）
- new-HPCの仕様（GPU構成・メモリ容量）確定

---

## Risks

- new-HPC導入遅延により、Dry Research（GNN解析）の本格開始が遅れる可能性がある
- 現有計算資源のうち、current-HPCはCryoEM専用、old-HPCはGPU性能が限定的であり、
  GNN開発の暫定環境として能力不足のリスクがある
- GitHub / Cursor運用が試験運用段階に留まっており、記録の抜け漏れが生じるリスクがある
- Icosahedral判定の誤検出（Result-002指摘）が未修正のままデータセットが
  確定した場合、後続のGNN解析全体の妥当性に影響するリスクがある
- ADR-013が未完成（ドラフト中断）のままの状態が続くと、学習対象の適格性基準が
  確定せず、B1 Dataset Constructionの完了がさらに遅延するリスクがある
- T=3 Encapsulinのデータ不足により、T=1/T=3比較解析（Phase3/Phase4）の
  タイムラインが当初計画より後ろ倒しになるリスクがある
- Wet Research（ADR-014）がDry Research（B1未完了）より先行して具体化しており、
  C1 Gene Preparationを先行させた場合、GNN予測結果を変異体設計へ反映する
  タイミング（C5以降）との整合が取れなくなるリスクがある

---

## Next Milestones

- Research OS正式運用の定着（ADR・Result記録の継続的更新、実装との同期）
- ADR-013のStatus確定
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の確定（B1完了条件）
- 初期GNNベースラインモデルの構築（Dataset A優先、B4着手）
- C1 Gene Preparation完了（Construct-Tm-01/02, Construct-Mx-01のクローニング）
- WT Stage Success Criteria達成（粒子形成確認・熱安定性評価・Heat Challenge評価）
- new-HPC導入完了

---

## Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

現在有効な内容のみ記載する。
