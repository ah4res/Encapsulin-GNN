WARNING

このファイルは派生文書である。

正本は

- ADR
- Results
- Roadmap
- Project_Charter

である。

Current_Stateが矛盾する場合は
正本を優先する。

本ファイルはSOP-001（ver1.2）のReconstruction Ruleに基づき、
既存Current_Stateの内容を事実の根拠として用いず、
Project_Charter / Roadmap / ADR全件 / Result全件から再構築されている。

Implementation Status（`docs/Implementation/`）は実装進捗の補助資料としてのみ参照し、
研究上の意思決定・結果の根拠には用いない。

人間向けの要約は `Current_State_Summary.md` を参照すること
（Dual Dashboard Principle、SOP-001 ver1.2）。

---

# Current State

Last Updated: 2026-08-03

## Project Summary

Encapsulin-GNNは、正二十面体対称粒子形成を規定する構造原理を
Graph Neural Network（GNN）により解析し、
その予測結果をWet実験によって検証するプロジェクトである
（Project_Charter）。

対象はT=1 Encapsulin（Myxococcus xanthus由来、Thermotoga maritima由来）を起点とするが、
ADR-010により解析対象データセットはEncapsulinに限定せず、
正二十面体対称粒子全般（Virus / VLP / Engineered Nanocage等）を含む
Icosahedral Particle Atlasとして構築する方針へ拡張された。

Result-003の系統解析により、初期GNN学習はT=1 Encapsulin単独および
T=1 Virusの二本立てで開始する方針が固まり、Wet Research側もADR-014により
T. maritima / M. xanthus 両Encapsulinの初期構築体・発現戦略が具体化された。

Dry Researchのグラフ設計は、ADR-016（Reference Chain A中心の局所グラフ、Status: Trial）を土台に、
ADR-017〜020（接触・モジュール分離・DSSP/PISA分離・PISA粒度）、
ADR-022（ノード=SEQRES、missing保持）、
ADR-023（エッジ特徴 `ss_pair` の HELO 10分類；ADR-021をSupersede）
までAcceptedとして積み上がっている。

パイプライン設計はさらにADR-024（Feature Review）、
ADR-025（DatasetPreparation batch）、
ADR-026（GraphBuilder: Feature Selection / Merge / Dataset Construction / Experiment Tracking）
がAcceptedとなり、ADR-018で想定された単純MergeFeaturesは
GraphBuilderへ吸収・拡張された（ADR-026 Decision）。

実装進捗の補助資料（Implementation Status）によれば、
FeatureContact / FeatureDSSP / FeaturePISA / FeaturesAA / Edge-Features /
PDB-GrepSubunits は gold_T1-enc 規模（概ね39〜41構造）でCSV・summary・plotsまで完備し、
いずれもADR-022（SEQRES）対応済みである。
DatasetPreparationとFeatureExtraction_Overview（Review Gallery基盤）も稼働し、
GraphBuilderは試作Graph-001〜004を生成済みである。
専用MergeFeaturesディレクトリは未作成のままだが、Feature Merge自体はGraphBuilderで進行中である。
残課題は Contact–PISA partner集合不一致、gold_T1-enc全量Graphの正式化、
PyG Export（ADR-028はタイトルのみの草稿）、Training着手、Fold分類未実装によるDataset B遅延などである。

Infrastructure側はADR-015によりnew-HPC構成が確定し発注段階にある。

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

---

## Infrastructure

### 現在地

Research Operating System（Research OS）の運用が開始された段階（ADR-001〜008）。
GitHubをSingle Source of Truthとし（ADR-002）、
Current_State.mdをダッシュボードとし（ADR-003；ver1.2ではSummaryとのDual Dashboard）、
Track A/B/Cの3トラック構成（ADR-004）、ADR/Resultの通し番号管理（ADR-005）、
Copilot/Cursorの役割分担（ADR-006）という基本運用ルールが確立している。

ネットワーク・計算環境・GitHub運用・AI支援開発環境の基盤整備は概ね完了しており
（Result-000）、Dry / Wet とも具体的な開発着手が可能な状態にある。

new-HPCはADR-015（Accepted）により構成確定：
AMD EPYC 9254、RTX A5000 24GB×2、Memory 64GB ECC、Rocky Linux 9、CryoSPARC同梱。
発注方針決定済みだが、発注実行・納品・A7デプロイは未完了。

Wet向け自動文献マイニング方針（ADR-009）はAccepted後、
2系統のみのため手動調査で十分と判断され close となった
（手動調査はResult-004として完了）。

### 最近の重要決定

- Research OS採用および運用ルール（ADR-001〜008）
- ADR-009 close（自動化パイプライン運用終了、手動調査へ）
- new-HPC構成確定・発注方針（ADR-015、Accepted）

### 最近の重要結果

- Result-000: ネットワーク・計算環境・GitHub・Cursor・Colab試験運用開始、Colab上GNN初回動作確認
- Result-001: Research OS運用方針確立

### 現在の課題

- new-HPCの発注実行・納品・環境構築（A6/A7）未完了
- current-HPCはCryoEM専用、old-HPCは暫定環境
- メモリ128GB増設の時期・トリガー未定
- 外付けHDDバックアップ手順未整理
- GitHub / Cursor / Colabは試験運用から本格運用への移行途上

### 次のアクション

- new-HPC発注実行および納品後セットアップ（A7）
- 外付けHDDバックアップ運用手順の具体化（A8）
- Research OS運用の本格化（ADR・Result・Implementation Statusの継続同期）

---

## Dry Research

### 現在地

#### データセット（B1）

ADR-010によりIcosahedral Particle Atlasを構築する方針がAccepted。
Result-002でAssembly取得・T-number推定の実用性を確認すると同時に、
Caspar-Klug例外・Icosahedral誤検出・Encapsulin Assembly解釈の曖昧さを指摘した。
ADR-011（T-number Level1〜4）はADR-013によりSuperseded。

ADR-012（段階的学習拡張）とADR-013（Gold/Silver/Future適格性）が方針を規定するが、
ADR-012はヘッダー「Proposed」とValidation欄「Accepted」が矛盾し、
ADR-013はStatus欄が欠落した草稿である。
Result-003により、初期学習はDataset A（T=1 Encapsulin）とDataset B（T=1 Virus）の二本立て、
T=3 Encapsulinは追加収集まで学習対象外とする方向が支持された。

実装補助資料では、Atlas実装（`PDB-VLP-list`）Phase 1–2が完了し、
`gold_T1-enc.csv`（41件）がDatasetPreparation / GraphBuilderの既定入力として稼働中。
Fold分類（HK97 / Jelly-roll / Other）とPhase 3 CLIは未実装で、Dataset B構築のブロッカーである。

#### グラフ表現・特徴量設計（B2/B3）

ADR-016（局所グラフ: Chain A全残基=ノード、A内部接触=エッジ、サブユニット間接触=ノード特徴）は
Validation Results記入済みだがStatusはTrialのまま。

Acceptedの特徴量方針:

- ADR-017: partner chain別接触特徴（合算を基本としない）
- ADR-018: 独立Featureモジュール + 統合（後にADR-026でGraphBuilderへ拡張）
- ADR-019: DSSP RSA（モノマー）とPISA ΔASA（Assembly）を分離
- ADR-020: PISA Global + Partner-specific 両方保持（Status欄欠落の草稿；Result-006が支持）
- ADR-022: ノード=SEQRES、`is_missing` / `missing_segment_length` 保持（Accepted）
- ADR-023: `ss_pair` を HELO 10分類へ置換（Accepted；ADR-021をSupersede）

ADR-021はSupersededであり、現行のエッジ仕様正本はADR-023である
（Result-008がHELO拡張の根拠）。

#### パイプライン設計（B2/B3運用）

- ADR-024: Feature Generationと統合の間にFeature Review（Gallery）を導入（Accepted）
- ADR-025: DatasetPreparationによるbatch Feature Generation（Accepted；入力=`gold_T1-enc.csv`）
- ADR-026: GraphBuilder導入（Feature Selection / Merge / Dataset Construction / Experiment Tracking）（Accepted）
  - 単純MergeFeaturesのみの実装はRejected；GraphBuilderはそれより広い責務
  - 初期出力はmerged CSV；PyG変換は後続モジュール

ADR-027（PrepPLM / FeaturesPLM二層）はDecision途中で本文が途切れておりStatusなし（不完全草稿）。
ADR-028（PyTorch Geometric Export）・ADR-029（GraphEncoder）はタイトルのみの草稿であり、
採択済み方針としては扱わない。

#### 実装進捗（補助資料；研究判断の根拠ではない）

Implementation StatusおよびFeatureExtraction_Overviewの確認結果（補助）:

| モジュール | Status（補助） | 要点 |
|-----------|----------------|------|
| PDB-GrepSubunits | Mostly Complete | gold_T1-enc 41件で`neighbor_cluster.pdb`生成 |
| FeatureContact | Mostly Complete | ADR-022済、39件でCSV/summary/plots |
| FeatureDSSP | Mostly Complete | ADR-019/022済、39件完備 |
| FeaturePISA | Mostly Complete | ADR-019/020/022済、39件＋validation |
| FeaturesAA | Mostly Complete | SEQRES配列のみ、39件、GraphBuilder登録済 |
| Edge-Features | Mostly Complete | ADR-023 HELO＋ADR-022 SEQRES済、39件完備 |
| FeatureRSCC | Not Started | PDB_analysisモジュールなし（探索コードのみ） |
| DatasetPreparaton | Mostly Complete | ADR-025稼働；41件バッチ実績（8IKA/9RY4 error） |
| FeatureExtraction_Overview | Mostly Complete | ADR-024 Gallery基盤；41 PDB、リンク健全 |
| GraphBuilder | Mostly Complete | Graph-001〜004生成；PyG未実装 |
| MergeFeatures（専用dir） | Not Started | Merge責務はGraphBuilderへ吸収（ADR-026） |
| PDB-VLP-list | Mostly Complete | gold_T1-enc供給中；Fold分類未実装 |
| PDB-LiteratureMining | Maintenance | ADR-009 close後の補助資産；rule_basedで7 PDB |

重要な乖離解消（旧Current_Stateからの更新点）:

- Edge-FeaturesのADR-022未対応・Feature側とのノード数不一致は、補助資料上は解消済み
  （例: 7S21でFeature/EdgeともSEQRES長301）
- 「MergeFeatures未着手が最大ボトルネック」は、専用dir未作成という意味では正しいが、
  Feature Merge自体はGraphBuilderで試作済み。現在のボトルネックは
  （1）Contact–PISA partner整合、（2）gold_T1-enc全量Graphの正式化とResult化、
  （3）PyG Export / Training未着手、へ移行している。

### 最近の重要決定

- Icosahedral Particle Atlas構築（ADR-010）
- ADR-011はADR-013によりSuperseded
- 段階的学習拡張（ADR-012；文書内Status矛盾あり）／Gold・Silver適格性（ADR-013；Status欠落）
- 初期学習 Dataset A / B 二本立て（Result-003結論）
- 局所グラフ表現 Trial（ADR-016）
- partner別接触（ADR-017）、独立モジュール（ADR-018）、DSSP/PISA分離（ADR-019）、
  PISA Global+Partner（ADR-020草稿）、SEQRESノード（ADR-022）
- エッジ仕様の正本はADR-023（HELO）；ADR-021はSuperseded
- Feature Review（ADR-024）、DatasetPreparation（ADR-025）、GraphBuilder（ADR-026）

### 最近の重要結果

- Result-002: Atlas基盤技術の実用性確認と3課題（誤検出・Caspar-Klug例外・Assembly解釈）
- Result-003: 系統樹解析 → Dataset A/B方針
- Result-005: 3DKT近傍サブユニット抽出による局所グラフ検討（Related ADR欄はADR-015と記載だが内容はADR-016系）
- Result-006: global_dASAとΣpartner_dASA完全一致 → ADR-020支持（テンプレート欠落あり）
- Result-007: ATOMベースによりmissingが消失 → ADR-022策定根拠
- Result-008: エッジ設計妥当性確認＋HELO拡張 → ADR-023へ反映

### 現在の課題

- ADR-013・ADR-020のStatus/Rationale等欠落；ADR-012のStatus矛盾；ADR-016がTrialのまま
- ADR-027不完全草稿；ADR-028/029はタイトルのみ
- Result-005 Related ADR疑義；Result-006テンプレート未準拠
- Dataset A/B最終構造リスト未確定（B1完了条件未達）；Fold分類未実装
- Result-002指摘の誤検出・Caspar-Klug例外の修正状況未確認
- Contact–PISA partner集合不一致（例: 3DKT Contact 7 vs PISA 5）が未解消
- GraphBuilder全量Dataset A正式化・Experiment Result化が未了
- PyG Export / GraphEncoder / Training未着手（B4未達）
- RSA–ΔASA相関の正式Result未記録（ADR-019 Next Action）
- ADR-022移行妥当性検証の正式Result未採番
- 補助資料上、8IKA/9RY4がSEQRES構築不可でbatch error；一部モジュールがgit未追跡

### 次のアクション

- ADR-012/013/020の文書完成（Status確定）
- ADR-016のStatus確定に向けた検証
- Result-005/006のテンプレート・参照修正
- Contact–PISA partner整合ルールの決定（GraphBuilder本格化の前提）
- gold_T1-enc成功構造でのGraphBuilder全量構築と正式Result化
- Feature Review（ADR-024 By Feature強化）の継続
- Dataset A/B構造リスト確定；Fold分類実装（Dataset B）
- PyG Export方針のADR化（ADR-028草稿の完成）とBaseline GNN（B4）着手
- RSA–ΔASA相関およびADR-022移行検証のResult採番
- Icosahedral誤検出・Caspar-Klug例外の修正確認；T=3追加探索

---

## Wet Research

### 現在地

ADR-014（Accepted）により初期Wet検証系が具体化。
Result-004の文献調査に基づき構築体・発現宿主が確定:

- T. maritima Encapsulin（3DKT系）: Construct-Tm-01（Tag-free）、Construct-Tm-02（C-His6）、pET28
- M. xanthus EncA（8VJO系）: Construct-Mx-01（N-His6-TEV）、自作pET21
- 宿主: E. coli BL21(DE3) CodonPlus-RILP

WT Stage Success Criteriaは定義済みだが実験実行は未着手（C1未開始）。

ADR-009はclose。手動調査（Result-004）がWet設計の正本的根拠。
実装補助資料では`PDB-LiteratureMining`がrule_basedで7 PDB分の出力を持つが、
位置づけ（維持/廃止）は未整理。

### 最近の重要決定

- 初期構築体・宿主の確定（ADR-014）
- WT Stage Success Criteria定義（ADR-014）
- ADR-009 close（手動文献調査運用）

### 最近の重要結果

- Result-004: T. maritima / M. xanthus既報条件調査 → ADR-014根拠

### 現在の課題

- C1 Gene Preparation未着手
- WT Criteria未達成（実験ゼロ件）
- Dry（B1未完）とWet（設計先行）の進行差の管理未整理
- `PDB-LiteratureMining`の位置づけ未決（ADR-009 closeとの差分）

### 次のアクション

- C1着手可否判断（Dataset確定待ちか並行か）
- Construct-Tm-01/02、Construct-Mx-01の遺伝子合成・クローニング
- 発現・精製・TEM/DLS・DSF・Heat Challengeの立ち上げ
- LiteratureMiningの維持/廃止決定

---

## Active ADR

Cursor Suggested

現時点でプロジェクト全体を支配していると考えられるADR（最大5件）。
これらはCursorの解釈であり、正本ではない。

- ADR-026: GraphBuilder（Feature Selection / Merge / Dataset / Experiment Tracking）。
  ADR-018の統合責務を拡張吸収し、現状のDryパイプライン到達点を規定する（Accepted）
- ADR-023: エッジ`ss_pair`をHELO 10分類へ置換（Accepted；ADR-021をSupersede。Result-008根拠）
- ADR-022: ノード=SEQRES、missing保持（Accepted。全主要Feature/Edge実装の前提）
- ADR-025: DatasetPreparationによるbatch Feature Generation（Accepted。`gold_T1-enc`運用の根拠）
- ADR-016: Reference Chain A中心の局所グラフ（Trial。上記ADR群の土台だがAccepted未了）

---

## Important Results

Cursor Suggested

現在のプロジェクトに最も影響を与えていると考えられるResult（最大5件）。
これらはCursorの解釈であり、正本ではない。

- Result-008: エッジ設計検証＋HELO拡張 → ADR-023へ直結
- Result-007: missing消失の確認 → ADR-022根拠
- Result-006: global⇔Σpartner dASA一致 → ADR-020支持
- Result-003: 系統樹 → Dataset A/B方針
- Result-005: 近傍サブユニット抽出 → 局所グラフ（ADR-016）検討の empiricallyな起点

---

## Open Questions

Cursor Generated

Project_Charter、Roadmap、ADR、Resultをもとに、
現時点で十分に解決されていないと考えられる論点（Cursorによる提案であり、正本ではない）。

- ADR-012/013/020の文書不完全（Status矛盾・欠落）をいつ誰が完成させるか
- ADR-016をTrialからAccepted/Rejectedへいつ確定するか（依存ADRが先行Accepted）
- Contact–PISA partner集合不一致をGrep側と下流フィルタのどちらで解消するか
- GraphBuilder全量Dataset Aをいつ正式Result化し、B4（Baseline GNN）へ進むか
- PyG Export（ADR-028草稿）とGraphEncoder（ADR-029草稿）をいつ仕様確定するか
- ADR-027（PLM二層）を完成させて採択するか、後回しにするか
- Dataset A/B最終リストとFold分類の完了時期（B1完了条件）
- `PDB-LiteratureMining`を維持するか廃止するか
- WetのC1をDryのDataset確定前に着手してよいか

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- ADR-012/013/020のStatus確定（文書完成）
- Contact–PISA partner整合ルールの決定
- gold_T1-encに対するGraphBuilder正式データセット方針（Feature Set選択）
- ADR-016 Status確定に向けた検証計画
- C1 Gene Preparation着手可否（Dataset確定待ちか並行か）
- PyG Export / Baseline GNN着手タイミング

---

## Risks

- new-HPC発注・納品遅延によりDry本格計算が遅れる
- ADR-016がTrialのまま依存ADR・実装が進み、根幹変更時に手戻りする
- ADR-013/020未完成のまま適格性・PISA仕様のトレーサビリティが損なわれる
- Contact–PISA partner不一致のまま学習データを構築すると品質・再現性が低下する
- GraphBuilder未コミット／一部モジュール未追跡により再現可能な版管理が崩れる
- Fold分類未実装のままDataset Bを進めると系統バイアスが残る
- WetがDryより先行し、GNN予測を変異体設計へ反映するタイミングがずれる
- Result/ADR相互参照の誤りが蓄積し意思決定の追跡性が低下する

---

## Next Milestones

- Research OS運用定着（ADR/Result/Implementation/Current_State同期）
- ADR-012/013/020完成、ADR-016 Status確定
- Contact–PISA partner整合の解消
- GraphBuilderによるDataset A正式Graph構築とResult化
- Feature Review（ADR-024）の定常運用
- Baseline GNN（B4）着手（PyG Export含む）
- Dataset A/B確定およびFold分類実装
- C1 Gene Preparation完了、WT Stage Criteria達成開始
- new-HPC発注・A7デプロイ完了

---

## Update Policy

SupersededされたADRは反映しない（例: ADR-011、ADR-021は現行仕様として採用しない）。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

Implementation Statusの内容がADR・Resultと矛盾する場合は反映しない。

現在有効な内容のみ記載する。
