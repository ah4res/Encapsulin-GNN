WARNING

このファイルは派生文書である。

正本は

- ADR
- Results
- Roadmap

である。

Current_Stateが矛盾する場合は
正本を優先する。

本ファイルはSOP-001（ver1.2）のReconstruction Ruleに基づき、
既存Current_Stateの内容を事実の根拠として用いず、
Project_Charter / Roadmap / ADR全件 / Result全件から再構築されている。

人間向けの要約は `Current_State_Summary.md` を参照すること
（Dual Dashboard Principle、SOP-001 ver1.2）。

---

# Current State

Last Updated: 2026-08-03

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
ADR-016により、GNN入力グラフはReference Chain Aを中心とした局所グラフ表現を
Trial採用する方針が示され、これを土台にADR-017〜ADR-020が採択され、
接触特徴量（partner chain別保持）・特徴量抽出パイプライン構成（独立モジュール化）・
DSSP/PISAの物理量分離・PISA特徴量の粒度（Global/Partner-specific両方保持）が
具体化された。さらにADR-021（Reference Chain A内部エッジの定義：Cα距離閾値
8Å、特徴量actual_distance/sequence_distance/ss_pair/same_ss_element）と
ADR-022（GNNノードをATOMではなくSEQRES配列基準で定義し、missing residueも
`is_missing`/`missing_segment_length`付きでノード保持する方針）が採択され、
局所グラフ表現のノード・エッジ両方の詳細設計が確定した。実装面では、
FeatureContact・FeatureDSSP・FeaturePISA（および共通入力を生成する
PDB-GrepSubunits）がいずれもMostly Completeまで進み、かつADR-022対応
（SEQRESベースのノード定義への移行）も完了している。新設のEdge-Features
モジュール（ADR-021対応）もMostly Completeだが、こちらはまだADR-022の
SEQRES移行が未着手であり、Feature側とEdge側でノード数が一致しない
（例: 7S21でFeature側301ノードに対しEdge側265ノード）という新たな
整合性課題が生じている。統合モジュールMergeFeaturesの設計・実装は
依然Not Startedで、Feature pipeline全体の最大のボトルネックである。
Infrastructure側もADR-015によりnew-HPCの構成
（AMD EPYC 9254 / RTX A5000×2、Rocky Linux 9、CryoSPARC同梱）が確定し
発注段階に進んだ。

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

---

## Infrastructure

### 現在地

Research Operating System（Research OS）の運用が開始された段階（ADR-001〜008、
いずれもAccepted）。GitHubをSingle Source of Truthとし（ADR-002）、
Current_State.mdを唯一のダッシュボードとし（ADR-003）、Track A/B/Cの3トラック構成
（ADR-004）、ADR/Resultの通し番号管理（ADR-005）、Copilot/Cursorの役割分担
（ADR-006）という基本運用ルールが確立している。

ネットワーク・計算環境・GitHub運用・AI支援開発環境（Cursor / Copilot）の
基盤整備は概ね完了しており（Result-000）、Dry Research / Wet Research双方とも
具体的な開発着手が可能な状態にある。

new-HPC（GNN解析・CryoSPARC・Nanoporeシーケンス解析・X線結晶構造解析の
統合運用を想定）はADR-015により構成が確定した（Status: Accepted）。
AMD EPYC 9254（24 Core）、NVIDIA RTX A5000 24GB×2、Memory 64GB ECC、
System Storage NVMe SSD 2TB、Scratch Storage NVMe SSD 8TB、
Data Storage HDD 10TB、OS Rocky Linux 9、CryoSPARC導入込みの構成で
リアルコンピューティングへ発注する方針が決定し、導入準備を開始した段階にある
（A6 HPC Procurement進行中）。メモリは将来的に128GB以上へ増設する方針であり、
研究データ保存は内蔵ストレージに依存せず外付けHDD運用を基本とする。

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
- new-HPCをAMD EPYC 9254 / RTX A5000 24GB×2 / Memory 64GB ECC / Rocky Linux 9 /
  CryoSPARC同梱の構成でリアルコンピューティングへ発注する（ADR-015、Accepted）

### 最近の重要結果

- Result-000: ネットワーク・計算環境・GitHub・Cursor・Google Colabの試験運用を開始し、
  Google Colab上でGNN学習パイプラインの初回動作を確認した。
- Result-001: Research OS運用方針（Project_Charter / Roadmap / Current_State / ADR / Result体系）を確立した。

### 現在の課題

- new-HPCはADR-015により仕様確定・発注方針決定済みだが、実際の発注実行・納品・
  環境構築（A6/A7）はまだ完了していない
- current-HPCはCryoEM専用でGNN用途に転用しない方針のため、old-HPC（GPU性能限定的）が
  納品までの暫定環境
- メモリ128GB以上への増設は将来対応とされており、具体的な増設時期・トリガー条件が未定
- 外付けHDDによるデータ保存・バックアップ運用の具体的な手順（頻度・世代管理等）が
  まだ整理されていない
- GitHub / Cursor / Google Colabはいずれもまだ試験運用中であり、本格運用に移行していない

### 次のアクション

- new-HPCの発注実行、納品後のセットアップ（A7 HPC Deployment）
- 外付けHDDによるデータ保存・バックアップ運用手順の具体化（A8）
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
実用レベルで機能することが確認された。同時に、(1) Caspar-Klug例外
（Rotavirus/Reovirus等の多層粒子で単純推定が破綻）、(2) Icosahedral判定の
誤検出（Cyclic/C2構造がis_icosahedral=Trueと誤判定される）、(3) 3DKT
（Encapsulin）のAssembly解釈の曖昧さ（assembly_subunit_count=120の解釈）
という3つの課題が確認された。このうち(3)の原因究明を通じて、T-number推定は
単なるアルゴリズムの問題ではなく学習対象粒子の定義（Dataset Eligibility）の
問題であることが判明し、T-number決定ロジック（Level1〜4優先順位）を提案した
ADR-011はADR-013へSupersededされた。(1)(2)の課題自体の修正状況はまだ
確認されていない。

現在はADR-012（GNN学習の段階的拡張戦略）とADR-013（Gold/Silver/Future Tierに
よるデータセット適格性基準）の2つのADRがデータセット構築の方針を規定している。
ただしADR-012はヘッダー部に「Status: Proposed」と記載される一方、文末の
Validation Results欄では「Status: Accepted」と記載されており、同一文書内で
Statusの記載が矛盾している（Result-003による検証が後から追記されたためと
みられる）。ADR-013はDecision・Eligible Dataset・Excluded Datasetまでは記述
されているが、Status欄自体が存在せず、Rationale・Alternatives Considered・
Next Actionも記載されていない。

Result-003では、Atlas由来のGold Dataset（T=1）・Silver Dataset（T=3）を対象に
Shell protein配列に基づく系統樹解析を実施した。Atlas全体（646構造、
CD-HIT後241クラスター、T=1: 403件、T=3: 243件）ではEncapsulin/Virus/VLPおよび
T=1/T=3が明確なクレードに分離しなかった一方、Encapsulinのみに絞った解析
（48構造、T=1 Encapsulin 40件、T=3 Encapsulin 8件、23種、18 shell protein）では、
T=1 Encapsulinは複数クレードに分散し比較的多様である一方、T=3 Encapsulinは
サンプル数が少なく特定系統に偏っていることが確認された。この結果を受け、
ADR-012は「Phase 1: T=1 Encapsulin単独 → Phase 2: T=1 Icosahedral Particle
Dataset（Encapsulin+Virus+VLP） → Phase 3: T=3 Dataset（追加データ収集後）→
Phase 4: T=1+T=3統合」という段階的戦略を維持し、初期GNN解析は「Dataset A:
T=1 Encapsulin」と「Dataset B: T=1 Virus」の二本立てで開始する方針が確定した。
T=3 Encapsulinは直ちに学習対象とせず、BLAST/DALI/MATRASによる追加構造探索の
対象とする。ADR-013もResult-003により方向性は支持されている
（「T=3 Encapsulinのデータ多様性不足が確認された。初期学習はGold Dataset(T=1)
を優先する」）。

B3 Graph Representation Designでは、ADR-016（Reference Chain A中心の局所グラフ
表現、Chain A全残基をノード・Chain A内部接触をエッジ・サブユニット間接触を
ノード特徴量とする方針）にValidation Resultsが記入され、方針自体は確定的に
なったが、Status自体は依然として「Trial」のままである。ADR-016にはASAの定義を
ADR-019に従うとする追記もなされた。この局所グラフ方針を土台に、2026-07-31〜
08-02にかけて特徴量設計に関する一連のADRがAccepted済みで採択された。ADR-017は
サブユニット間接触特徴量をpartner chain別（A-B, A-C, ...）に保持し、全chain
合算を基本表現としない方針を決定した（Related Results: Result-005）。ADR-018は
特徴量抽出パイプラインをFeatureContact / FeatureDSSP / FeaturePISA /
FeatureRSCC等の独立モジュールとして実装し、MergeFeaturesで統合する方針を
決定した。ADR-019はDSSP（Reference Chain A単独構造によるRSA、モノマー状態の
表面露出性）とPISA（Assembly構造によるΔASA、Assembly形成による埋没量）を
意図的に異なる物理量として分離計算する方針を決定した。

ADR-020はPISA由来界面特徴量をGlobal Feature（global_dASA等）とPartner-specific
Feature（dASA_AB等）の両方で保持する方針を示しているが、文書はQuestion/Decision
のみで終わっており、Status・Rationale・Alternatives Considered・Consequences・
Next Actionが記載されていない（ADR-013と同様のパターン）。これに対しResult-006が、
3構造でglobal_dASAとΣpartner_dASAが完全に一致すること（max|diff|=0、RMSE=0、
Pearson r=1.0）を確認し、ADR-020の方針を支持する結果を提示している。ただし
Result-006自体もDate・Track・Related ADR・Interpretation・Next Actionの記載を
欠いており、Resultテンプレート（README.md）に完全準拠していない（関連ADRは
Conclusion文中の「ADR-020を支持」という記述から推定できるのみである）。

また、Result-005のRelated ADR欄は「ADR-015」（new-HPC構成に関するADR）と
記載されているが、Result-005の内容（3DKT近傍サブユニット抽出による局所グラフ
検討）はADR-016（局所グラフ表現の採用）と直接対応しており、ADR-015（HPC）への
参照は内容と一致していない可能性がある。

局所グラフのエッジ設計についてはADR-021が、Reference Chain A内部の残基間
エッジをCα距離閾値（初期値8Å、4/6/8/10Åでアブレーション可能）で定義し、
`actual_distance`・`sequence_distance`・`ss_pair`・`same_ss_element`を
エッジ特徴量として保持する方針をAcceptedとした。Result-008はこの設計を
3構造（3DKT/7S21/9B9I）で検証し、thresholdに対するエッジ数の単調増加、
配列上遠いが空間的に近接する残基対の存在、同一二次構造要素内/間接触の
識別可能性を確認して設計を支持した。同時にResult-008は、当初のH/E/L
3分類に加えてO（T/S/P等のturn/bend/other）を追加したHELO拡張
（ss_pairをHH/EE/LL/HE/HL/EL/HO/EO/LO/OOの10種とする）を採用仕様として
結論づけたが、ADR-021本文はまだHEL 6種（HH/EE/LL/HE/HL/EL）のみを記載した
ままであり、ADR文書とResult-008・実装（Edge-Features）の間に表記差が
生じている。

ノード定義についてはResult-007が、現行のFeaturesDSSP等がATOMレコードのみを
対象としているためmissing residue（座標未確定領域）が消失していることを
3構造で確認した（3DKT: 265→264、missing 1；7S21: 301→265、missing 36、
約12%；9B9I: 281→262、missing 19）。この結果を受けてADR-022が、GNNノードを
ATOMではなくSEQRES配列を基準として定義し直し、すべてのFeature抽出モジュールが
SEQRESベースへ移行すること、missing residueも`is_missing`
（0=modeled/1=missing）および`missing_segment_length`をノード特徴量として
保持することをAcceptedとした。

実装進捗の観点では、Implementation Status（補助資料、`docs/Implementation/`）
により、上記ADR群に対応する特徴量抽出モジュールの実装が大きく進んでいることが
確認された。PDB-GrepSubunits（近傍サブユニット抽出、ADR-016の入力生成）・
FeatureContact（実装名`CountInteractionWithNCSchain`、ADR-016/017/022対応）・
FeatureDSSP（実装名`FeaturesDSSP`、ADR-019/022対応）・FeaturePISA（実装名
`FeaturesPISA`、ADR-019/020/022対応）はいずれも3構造（3DKT/7S21/9B9I）でCSV・
summary・可視化一式の生成まで確認されており、Current Status「Mostly
Complete」（Overall完成度85〜90%）である。この3モジュールはいずれも
ADR-022対応（SEQRESベースのノード展開、`is_missing`/`missing_segment_length`
列の付与）を完了しており、ノード数はSEQRES長（3DKT 265、7S21 301、
9B9I 281）と一致することが確認された。FeaturePISAの検証はResult-006
（global_dASAとΣpartner_dASAの完全一致）と整合する結果を独立に再現している。
新設のEdge-Features（実装パス`Edge-Features/`、ADR-021対応）もMostly
Complete（Overall 85%）であり、`actual_distance`・`sequence_distance`・
`ss_pair`（HELO拡張済み）・`same_ss_element`を含む`edge_features.csv`等を
3構造で生成済みだが、ADR-022のSEQRES移行が未着手であり、ノード集合が
ATOMベースのまま（例: 7S21で265ノード）となっている。この結果、Feature側
（SEQRESベース、7S21で301ノード）とEdge側（ATOMベース、7S21で265ノード）の
間で新たなノード数不一致が生じている。一方でMergeFeatures（ADR-018が
要求する統合モジュール）は実装・出力とも存在せず「Not Started」
（Overall 5%）であり、Feature pipeline全体がGNN学習用テーブルへ
到達できていない最大のボトルネックとなっている。また
FeatureContactとFeaturePISAの間でpartner chain集合が一致しない例が確認された
（3DKT: Contact側 partner B–Hの7 chain、PISA側 partner B–Fの5 chain）。
この不一致の原因（PDB-GrepSubunits側の抽出条件差か、各モジュール側の
フィルタ条件差か）は未特定であり、MergeFeatures設計前に解消が必要である。
なお、ADR-022移行の妥当性検証（before/after比較）は
`ADR022_before_after_comparison.csv`・`ADR022_Implementation_Report.md`
として横断的に存在するが、正式なResult番号がまだ採番されていない。

Icosahedral Particle Atlas（実装: `PDB-VLP-list`）についても、Phase 1
（Notebook検証）・Phase 2（src ライブラリ化：検索/metadata取得/分類/DB/
T-number/Dataset Eligibility/系統樹解析）が完了し、単体テスト43件全てが
passしていることが確認された。ただしFold分類（HK97 / Jelly-roll / Other）は
`src/analysis/`内に実装が見当たらず未実装のままであり、Dataset B（T=1全粒子）
構築のブロッカーとなっている。Phase 3（`atlas discover/update/classify/...`の
CLI化）も未着手である。

### 最近の重要決定

- 解析対象をEncapsulinに限定せず、正二十面体対称粒子全般を収集する
  Icosahedral Particle Atlasを構築する（ADR-010、Accepted）
- T-number決定ロジック（Level1〜4優先順位）を定めたADR-011は、
  3DKT誤判定の根本原因がDataset Eligibility不足にあったとの判明を受け、
  ADR-013によりSuperseded（置換）された
- GNN学習はT=1 Encapsulin単独（Phase1）→ T=1全粒子（Phase2）→ T=3（Phase3）→
  T=1+T=3統合（Phase4）の順で段階的に拡張し、T=4以上は当面除外する
  （ADR-012、Result-003により検証済み。ただしADR-012文書内でStatus記載が
  「Proposed」と「Accepted」で矛盾している）
- 初期GNN解析はDataset A（T=1 Encapsulin）とDataset B（T=1 Virus）の
  二本立てとし、T=3 Encapsulinは追加データ収集まで学習対象から除外する
  （Result-003の結論、ADR-012の運用方針として反映）
- GNN学習データセットをGold（T=1）／Silver（T=3）／Future（T=1+T=3統合）の
  Tierに階層化し、Pseudo-T粒子・多層殻粒子を除外する
  （ADR-013、Status欄なしの草稿だがResult-003により方向性は支持）
- Encapsulin-GNN初期モデルはReference Chain Aを中心とした局所グラフ表現
  （Chain A全残基をノード、Chain A内部接触をエッジ、サブユニット間接触を
  ノード特徴量）をTrial採用する（ADR-016、Status: Trial、Validation Results記入済み）
- サブユニット間接触特徴量はpartner chainごとに保持し、全chain合算は
  基本表現として採用しない（ADR-017、Accepted。実装（FeatureContact）で
  `partner_chain`列の保持を確認済み）
- 特徴量抽出パイプラインはFeatureContact / FeatureDSSP / FeaturePISA等の
  独立モジュールとして実装し、MergeFeaturesで統合する（ADR-018、Accepted。
  実装状況: Contact/DSSP/PISAはMostly Complete、統合モジュールMergeFeaturesは
  Not Started）
- DSSP（Chain A単独、RSA）とPISA（Assembly、ΔASA）は異なる物理量として
  独立に計算する（ADR-019、Accepted。実装（FeatureDSSP/FeaturePISA）で
  分離計算を確認済み。RSA–ΔASAの正式なResult化は未了）
- PISA由来界面特徴量はGlobal FeatureとPartner-specific Featureの両方を
  保持する（ADR-020、Status欄なしの草稿だがResult-006で方向性は支持）
- Reference Chain A内部の残基間エッジはCα距離閾値（初期値8Å、
  4/6/8/10Åでアブレーション可能）で定義し、actual_distance /
  sequence_distance / ss_pair / same_ss_elementをエッジ特徴量として
  保持する（ADR-021、Accepted。Result-008により設計を検証済み。
  実装（Edge-Features）はMostly Complete）
- GNNノードはATOMレコードではなくSEQRES配列を基準として定義し、
  missing residueも`is_missing`/`missing_segment_length`付きで
  ノードとして保持する（ADR-022、Accepted。Result-007が根拠。
  FeatureContact/FeatureDSSP/FeaturePISAは移行済み、Edge-Featuresは未移行）

### 最近の重要結果

- Result-002: Icosahedral対称性取得・Biological Assembly情報取得・T-number推定が
  実用レベルで機能することを確認した。Caspar-Klug例外・Icosahedral判定誤検出
  （Cyclic/C2の誤分類）・Encapsulin assembly解釈の曖昧さという3つの課題も
  確認された（ADR-012/013の発端）。
- Result-003: Atlas全体（646構造）およびEncapsulin限定（48構造）の系統樹解析を実施。
  T=3 Encapsulinのデータ多様性不足を確認し、初期GNN学習をDataset A（T=1 Encapsulin）
  とDataset B（T=1 Virus）の二本立てとする方針を導いた。
- Result-005: 3DKT Biological AssemblyのChain A近傍サブユニット抽出により、
  局所グラフ構築方式（ADR-016）の妥当性を検討した。Whole ParticleのNCS冗長性、
  局所PDBに対するPISA計算時のASA誤差リスク、A-B接触のノード特徴量化という
  知見を得た。Related ADR欄は「ADR-015」と記載されているが、内容的にはADR-016
  との対応が想定される。
- Result-006: 3構造についてPISAのglobal_dASAとΣpartner_dASAを比較し、両者が
  完全に一致すること（max|diff|=0、RMSE=0、Pearson r=1.0）を確認した。
  ADR-020（Global/Partner-specific Featureの両方を保持する方針）を支持する
  結果となった。Date・Track・Related ADR・Interpretation・Next Actionの記載を
  欠いている。
- Result-007: 3DKT/7S21/9B9Iを対象に、FeaturesDSSP等がATOMベースの実装で
  あるためmissing residueが消失していることを確認した（7S21で約12%消失）。
  この知見がADR-022（SEQRESベースのノード定義）策定の直接的根拠となった。
- Result-008: ADR-021のエッジ設計（Cα距離閾値、4種のエッジ特徴量）を
  3構造で検証し、設計の妥当性を確認した。同時にss_pairをHELO
  （H/E/L/O 4分類の組合せ10種）へ拡張する方針を採用仕様として結論づけた。

### 現在の課題

- ADR-013・ADR-020はいずれもStatus欄が存在せず、Rationale・Alternatives
  Considered・Consequences・Next Actionも未記載のまま中断している
- ADR-012はヘッダーの「Status: Proposed」とValidation Results欄の
  「Status: Accepted」が矛盾したままになっている
- ADR-016はValidation Resultsが記入されたが、Statusは依然「Trial」のままであり、
  正式なAccepted化には至っていない
- Result-005のRelated ADR欄が「ADR-015」となっているが、内容的にはADR-016
  （局所グラフ表現の採用）との対応が想定され、参照の妥当性に疑義がある
- Result-006がResultテンプレート（Date/Track/Related ADR/Interpretation/
  Next Action）に完全準拠していない
- FeatureContact・FeatureDSSP・FeaturePISA・PDB-GrepSubunitsの実装は
  Mostly Complete（3構造で検証済み、ADR-022のSEQRES移行も完了）だが、
  統合モジュールMergeFeatures（ADR-018）はNot Startedのままであり、
  Feature pipeline全体が学習用テーブルへ到達できていない
- Edge-Features（ADR-021対応）はADR-022のSEQRES移行が未着手であり、
  Feature側（SEQRESベース、例: 7S21で301ノード）とEdge側（ATOMベース、
  同265ノード）のノード数が一致しない。MergeFeaturesでのnode–edge統合前に
  解消が必要
- ADR-021本文はss_pairをHEL 6種（HH/EE/LL/HE/HL/EL）のまま記載しているが、
  Result-008 ConclusionおよびEdge-Features実装はHELO 10種
  （HH/EE/LL/HE/HL/EL/HO/EO/LO/OO）を採用仕様としている。ADR文書の
  更新が未反映
- ADR-022移行（SEQRESベースのノード定義）の妥当性検証（before/after比較）は
  `ADR022_before_after_comparison.csv`等として存在するが、正式なResult番号が
  まだ採番されていない（Result-007は移行前スナップショットのまま）
- FeatureContactとFeaturePISAの間でpartner chain集合が一致しない例がある
  （3DKT: Contact側7 chain、PISA側5 chain）。MergeFeatures設計前に
  原因切り分けと解消が必要
- FeatureDSSPで得られたRSA–global_dASAの簡易相関（r≈0.52〜0.54）は
  ADR-019 Next Actionが求める正式なResultとしてまだ記録されていない
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の最終的な構造リストが
  未確定であり、B1完了条件（解析対象構造の決定）に到達していない
- Result-002で指摘されたIcosahedral判定の誤検出（Cyclic/C2構造の誤分類）と
  Caspar-Klug例外（多層粒子）の修正状況が未確認
- Fold分類（HK97 / Jelly-roll / Other）が未実装であり、Dataset Bの構築に必要
- T=3 Encapsulinの追加構造探索（BLAST/DALI/MATRAS）が未着手
- PDB-EMDB対応付け（Result-002 Next Action）が未着手

### 次のアクション

- ADR-013・ADR-020を完成させる（Status・Rationale・Alternatives・
  Consequences・Next Actionを記載）
- ADR-012のStatus記載の矛盾（Proposed/Accepted）を解消する
- ADR-016のStatus確定に向けた検証実施（Trial→Accepted/Rejected）
- Result-005のRelated ADR参照の正確性を確認・修正する
- Result-006にDate・Track・Related ADR・Interpretation・Next Actionを補記する
- FeatureContact–FeaturePISA間のpartner chain集合不一致の解消ルールを
  定義する（MergeFeatures設計の前提。3DKTでContact 7 chain・PISA 5 chainの
  差異を確認）
- Edge-FeaturesをADR-022（SEQRESベースのノード定義）へ移行し、Feature側
  （Contact/DSSP/PISA）とノード数を一致させる
- ADR-021本文のss_pair仕様をHELO 10種（Result-008 Conclusion採用済み）へ
  更新する
- ADR-022移行（SEQRESベースのノード再計算）の妥当性検証を正式なResultとして
  採番する（`ADR022_before_after_comparison.csv`を根拠資料とする）
- RSA–ΔASA相関（FeatureDSSPでr≈0.52〜0.54を簡易確認済み）を正式な
  Resultとして記録する（ADR-019 Next Action）
- MergeFeatures設計・実装に着手する（ADR-018 Next Action。現状Not Started・
  Overall 5%であり、Feature pipeline全体のボトルネック。SEQRES主キーでの
  結合キー仕様をまず固定する）
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の構造リストを確定する
- Fold分類（HK97 / Jelly-roll / Other）をPDB-VLP-list（Atlas）に実装する
  （Dataset B構築のブロッカー）
- 初期GNNベースラインモデルの構築（Dataset A優先）
- T=3 Encapsulin候補の追加構造探索（BLAST/DALI/MATRAS）
- Icosahedral判定誤検出・Caspar-Klug例外の修正確認
- PDB-EMDB対応付けの実施
- Dataset A/B確定後、FeatureContact/FeaturePISA/PDB-GrepSubunitsの
  batch実行経路とPDB-VLP-list Phase 3（`atlas`コマンドCLI）を整備する

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

ただしImplementation Statusで実装状況を確認したところ、`PDB-LiteratureMining`
自体はADR-009のclose前後にPhase 1（Single PDB Prototype）・Phase 2（srcモジュール
化）・Phase 4（Batch Processing）まで実装済みであり、対象7 PDB（3DKT, 7MU1,
7KQ5, 7K5W, 4PT2, 7S20, 8VJO）についてEvidence付き構造化Metadata（CSV/JSON）を
実際に生成していることが確認された（Phase 3のCLI化のみ未実装）。ADR-009の
close決定（自動化戦略の運用終了、手動調査への切替）と、このコードベースが
実際に稼働し出力を残している事実との間には仕様差分があり、本コードベースを
補助ツールとして維持するか、完全に運用終了として扱うかがまだ整理されていない。

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
- ADR-009のclose決定（自動化パイプライン運用終了）と、`PDB-LiteratureMining`
  コードベースが実際にPhase 1/2/4まで実装され7 PDB分の出力を生成している
  事実との間に仕様差分がある。位置づけ（補助ツールとして維持するか、
  完全に運用終了とするか）が未整理

### 次のアクション

- C1 Gene Preparation着手: Construct-Tm-01/02、Construct-Mx-01の遺伝子合成・
  クローニング
- 発現・精製ワークフロー（硫安沈殿→SEC／Ni-NTA→SEC）の立ち上げ
- WT粒子形成評価（TEM/DLS）、熱安定性評価（DSF）、Heat Challenge評価の実施
- `PDB-LiteratureMining`の位置づけ（補助ツールとして維持 or 運用終了）を
  ADR-009の方針を踏まえて整理する

---

## Active ADR

Cursor Suggested

現時点でプロジェクト全体を支配していると考えられるADR（最大5件）。
これらはCursorの解釈であり、正本ではない。

- ADR-022: GNNノードはATOMではなくSEQRES配列を基準として定義し、missing
  residueも`is_missing`/`missing_segment_length`付きで保持する
  （Status: Accepted。FeatureContact/FeatureDSSP/FeaturePISAは移行済み、
  Edge-Featuresは未移行というプロジェクト全体の現在の主課題を生んでいる）
- ADR-021: Reference Chain A内部エッジをCα距離閾値で定義し、
  actual_distance / sequence_distance / ss_pair / same_ss_elementを
  エッジ特徴量とする（Status: Accepted。Result-008で検証済みだが
  本文のss_pair表記がHELO拡張未反映）
- ADR-016: Encapsulin-GNN初期モデルはReference Chain Aを中心とした
  局所グラフ表現を採用する（Status: Trial、Validation Results記入済みだが
  Accepted化は未了。ADR-021/022の土台となっている）
- ADR-018: 特徴量抽出パイプラインはFeatureContact / FeatureDSSP / FeaturePISA
  等の独立モジュールとして実装し、MergeFeaturesで統合する（Status: Accepted）
- ADR-017: サブユニット間接触特徴量はpartner chainごとに保持する
  （Status: Accepted、Related Results: Result-005）

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えていると考えられるResult（最大5件）。
これらはCursorの解釈であり、正本ではない。

- Result-008: ADR-021のエッジ設計（Cα距離閾値、4種のエッジ特徴量）を
  3構造で検証し妥当性を確認した。ss_pairのHELO拡張（10種）を採用仕様として
  結論づけ、ADR-021本文との表記差を生んでいる。
- Result-007: FeaturesDSSP等がATOMベースのためmissing residueが消失している
  ことを3構造で確認（7S21で約12%消失）し、ADR-022（SEQRESベースのノード
  定義）策定の直接的根拠となった。
- Result-006: PISAのglobal_dASAとΣpartner_dASAが完全に一致すること
  （RMSE=0、Pearson r=1.0）を確認し、ADR-020（Global/Partner-specific
  Feature両方保持）を支持した（テンプレート未準拠の記載欠落あり）。
- Result-005: 3DKT Biological AssemblyのChain A近傍サブユニット抽出により、
  局所グラフ構築方式（ADR-016）の妥当性を検討し、NCS冗長性の回避・
  PISA ASA誤差リスク・A-B接触の特徴量化という知見を得た（Related ADR欄の
  参照に疑義あり）。
- Result-003: Atlas全体およびEncapsulin限定の系統樹解析により、T=3 Encapsulinの
  データ多様性不足を確認し、初期GNN学習をDataset A（T=1 Encapsulin）/
  Dataset B（T=1 Virus）の二本立てとする方針を導いた。

---

## Open Questions

Cursor Generated

Project_Charter、Roadmap、ADR、Resultをもとに、
現時点で十分に解決されていないと考えられる論点（Cursorによる提案であり、正本ではない）。

- ADR-013・ADR-020はいずれもStatus欄が存在しないまま中断している。いつ、誰が
  これを完成させ、Status（Accepted等）を確定するか
- ADR-016はValidation Resultsが記入されたにもかかわらずStatusが「Trial」のまま
  である。また、Result-005のRelated ADR欄は「ADR-015」（HPC）となっているが、
  内容的にはADR-016（局所グラフ設計）との対応が想定される。この参照不整合を
  どう解消し、ADR-016のStatusをいつ確定するか
- ADR-012はヘッダー部で「Status: Proposed」、文末のValidation Results部で
  「Status: Accepted」と矛盾した記載になっている。どちらを正としてADR文書を
  修正するか
- ADR-017・018・019は明確な実験的検証（Result）を伴わずに短期間でAcceptedと
  なっている（ADR-017のみResult-005を関連付け）。実装（コード化・実データ適用）
  前にどの範囲まで追加検証が必要か
- Result-006はDate・Track・Related ADR・Interpretation・Next Actionの記載を
  欠いており、Resultテンプレートに準拠していない。誰がいつ補完するか
- FeatureContactとFeaturePISAでpartner chain集合が一致しない原因は
  PDB-GrepSubunits側の抽出条件差か、各モジュール側のフィルタ条件差か。
  MergeFeatures設計前にどちらで解消するか
- MergeFeaturesが未着手のままFeature pipeline全体が学習用テーブルへ
  到達できていない。設計（結合キー・partner集約方式・出力スキーマ）に
  誰がいつ着手するか
- Edge-FeaturesのADR-022（SEQRES）移行はいつ実施するか。未対応のまま
  MergeFeaturesを設計すると、Feature側とEdge側でノード集合が
  一致しない状態が統合モジュールに持ち込まれる
- ADR-021本文のss_pair表記（HEL 6種）をResult-008 Conclusion（HELO 10種）に
  合わせて更新するか、あるいは別ADRとして起票するか
- ADR-022移行の妥当性検証（`ADR022_before_after_comparison.csv`等）を
  正式なResultとして採番するか、Result-007を更新する形にするか
- `PDB-LiteratureMining`はADR-009のclose決定にもかかわらず実装が
  完了している。このコードベースを補助ツールとして維持するか廃止するかを
  いつ、誰が確定するか
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の最終構造リストは
  いつ確定するか（B1完了条件）
- Fold Diversity Strategy（HK97 fold / Jelly-roll fold / Other）を
  Atlas実装・分類ロジックにどう反映するか
- T=3 Encapsulinの追加構造探索（BLAST/DALI/MATRAS）はいつ、どのように実施するか
- Wet Research（ADR-014、Construct確定済み）がDry Research（B1未完了）より
  先行して具体化しているが、C1 Gene PreparationをDataset確定前に着手してよいか
- WT Stage Success Criteria（T. maritima 10項目、M. xanthus 5項目）の
  実施体制・スケジュール、およびnew-HPCの発注実行から納品・A7デプロイまでの
  スケジュールをどう組むか

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- ADR-013・ADR-020を完成させ、Statusを確定する
- ADR-012のStatus記載の矛盾（Proposed/Accepted）を解消する
- ADR-016（局所グラフ設計）の検証を実施し、StatusをTrialからAccepted/Rejectedへ確定する
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の構造リストの確定（B1完了条件）
- C1 Gene Preparation着手可否の判断（Dataset確定を待つか、並行して開始するか）
- MergeFeaturesの設計方針（結合キー・partner集約方式・出力スキーマ）を確定し、実装に着手する
- FeatureContact–FeaturePISA間のpartner chain集合不一致の解消ルールを決定する
- Edge-FeaturesのADR-022（SEQRES）移行の実施タイミングを決定する
- ADR-021本文のss_pair仕様をHELO版へ更新するか判断する

---

## Risks

- new-HPCの仕様はADR-015により確定したが、発注実行・納品・環境構築（A6/A7）が
  遅延した場合、Dry Research（GNN解析）の本格開始が遅れる可能性がある
- 現有計算資源のうち、current-HPCはCryoEM専用、old-HPCはGPU性能が限定的であり、
  GNN開発の暫定環境として能力不足のリスクがある
- GitHub / Cursor運用が試験運用段階に留まっており、記録の抜け漏れが生じるリスクがある
- Icosahedral判定の誤検出およびCaspar-Klug例外（Result-002指摘）が未修正のまま
  データセットが確定した場合、後続のGNN解析全体の妥当性に影響するリスクがある
- ADR-013・ADR-020が未完成（Status欄なし）のままの状態が続くと、学習対象の
  適格性基準・PISA特徴量仕様が確定せず、B1/B2の完了がさらに遅延するリスクがある
- ADR-016（根幹となる局所グラフ設計）がTrialのまま、それに依存するADR-017〜020
  （特徴量設計）がAcceptedとして積み上がっている。根幹設計が後で変更された場合、
  依存するADR群・実装全体に手戻りが生じるリスクがある
- Result-005のRelated ADR欄やADR-012のStatus記載など、ADR/Result間の相互参照・
  記載に誤り・矛盾が蓄積すると、将来的に意思決定のトレーサビリティが損なわれる
  リスクがある
- T=3 Encapsulinのデータ不足により、T=1/T=3比較解析（Phase3/Phase4）の
  タイムラインが当初計画より後ろ倒しになるリスクがある
- Wet Research（ADR-014）がDry Research（B1未完了）より先行して具体化しており、
  C1 Gene Preparationを先行させた場合、GNN予測結果を変異体設計へ反映する
  タイミング（C5以降）との整合が取れなくなるリスクがある
- MergeFeaturesが未着手のまま単体モジュール（Contact/DSSP/PISA）の実装が
  先行しており、統合設計の遅延がFeature pipeline全体、ひいてはB4ベースライン
  モデル構築の開始を遅らせるリスクがある
- FeatureContactとFeaturePISAのpartner chain集合不一致が未解消のまま
  MergeFeaturesを実装した場合、学習データの品質・再現性に影響するリスクがある
- Edge-FeaturesがADR-022未対応（ATOMベース）のままMergeFeaturesへ統合すると、
  Feature側（SEQRESベース）とEdge側でノード集合が不一致のまま学習データが
  構築され、GNN入力の整合性が損なわれるリスクがある
- ADR-021本文とResult-008/実装（HELO拡張）の仕様差が放置されると、ADR文書の
  信頼性・意思決定のトレーサビリティが損なわれるリスクがある

---

## Next Milestones

- Research OS正式運用の定着（ADR・Result記録の継続的更新、実装との同期）
- ADR-013・ADR-020のStatus確定、ADR-012のStatus記載統一
- ADR-016のStatus確定（Trial→Accepted/Rejected）
- MergeFeatures（Contact/DSSP/PISA/Edge統合モジュール）の設計・実装完了
  （Contact/DSSP/PISAはADR-022対応済みで3構造検証済みだがMergeFeaturesは
  Not Started）
- Edge-FeaturesのADR-022（SEQRES）移行完了、ADR-021本文のHELO版更新
- Dataset A（T=1 Encapsulin）・Dataset B（T=1 Virus）の確定（B1完了条件）
- 初期GNNベースラインモデルの構築（Dataset A優先、B4着手）
- C1 Gene Preparation完了（Construct-Tm-01/02, Construct-Mx-01のクローニング）
- WT Stage Success Criteria達成（粒子形成確認・熱安定性評価・Heat Challenge評価）
- new-HPCの発注実行・納品・A7デプロイ完了

---

## Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

現在有効な内容のみ記載する。
