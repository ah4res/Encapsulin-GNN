## SOP-004

### Feature Pipeline Canvas Regeneration Procedure

#### Purpose

本手順は、

`Feature-Pipeline-Scripts.canvas.tsx`

を再現性よく再生成・更新するための標準手順である。

本 Canvas は

- `IMPLEMENTATION_STATUS_*.md`（SOP-003）
- `structure_tools/PDB_analysis/DatasetPreparaton/modules.yaml`
- 関連 ADR（特に ADR-018 / 024 / 025 / 026）

から導かれる **スクリプト／モジュール間の関係図** であり、
ADR・Result・Current_State の代替ではない。

script / モジュールが増えた際に、
同一の書式・レイアウト規約で Dependency graph を再表示するために用いる。

---

#### Location

本SOPおよび対象 Canvas は同一ディレクトリに配置する。

```text
/Users/ahgsur/github/00_Projects/Project_02_encapsulin/06_Encapsulin-GNN/docs/Implementation/
```

| ファイル | 役割 |
|----------|------|
| `SOP-004_Feature_Pipeline_Canvas_Regeneration.md` | 本手順（正本） |
| `Feature-Pipeline-Scripts.canvas.tsx` | Canvas ソース（リポジトリ正本） |
| `Feature-Pipeline-Dependency-Graph.html` | PDF 用中間 HTML（任意） |
| `Feature-Pipeline-Dependency-Graph.pdf` | 配布用 Dependency graph（任意） |

Cursor IDE のライブ表示用パスは次とする（リポジトリ正本への symlink 推奨）。

```text
~/.cursor/projects/<workspace>/canvases/Feature-Pipeline-Scripts.canvas.tsx
  → docs/Implementation/Feature-Pipeline-Scripts.canvas.tsx
```

IDE は `canvases/` 配下の `.canvas.tsx` のみをライブ Canvas として検出する。
リポジトリ側を編集した場合は、symlink が切れていないことを確認する。

通し番号は他の SOP（SOP-001〜003）と連続させる。
配置ディレクトリのみ本SOPは生成物と同階層とする（Canvas 再生成の作業単位を1ディレクトリに閉じるため）。

---

#### Scope

対象は Encapsulin-GNN Dry Research の Feature pipeline に関わる
実装モジュールおよびその entry script である。

##### 必須（DAG に含める）

パイプライン spine（ADR-024〜026）上のモジュール。

```text
Dataset (VLP-list)
  → Orchestrator (DatasetPreparaton)
  → Feature / Preprocess modules
  → Review (FeatureExtraction_Overview)
  → GraphBuilder
  → GraphEncoder（未実装でもノードとして残す）
```

##### 表のみ（DAG から省略可）

DAG が過密になる並列・将来モジュール。
Table セクションには必ず載せる。

例

- PDB-LiteratureMining（Wet 並列）
- FeatureRSCC（未着手・PDB_analysis 外）
- 専用 MergeFeatures ディレクトリ（未作成；GraphBuilder 注記で足りる）

##### 対象外

- モジュール内部のヘルパ `.py` 全列挙
- `working/` やキャッシュディレクトリ
- ADR / Result 本文の再解釈

---

#### Invocation Rule

本SOPは常時実行しない。

以下の指示がある場合にのみ実行する。

例

- Feature Pipeline Canvas を更新してください
- Dependency graph を再生成してください
- SOP-004 を実行してください
- script / モジュールを追加したので Canvas を直してください

通常の IMPLEMENTATION_STATUS 更新（SOP-003）だけでは
本 Canvas を自動更新しない。
SOP-003 完了後に本SOPを続けて実行してよい。

---

#### Source of Truth

Canvas は正本ではない。

優先順位：

1. `docs/ADR/*`（設計・依存関係の方針）
2. `DatasetPreparaton/modules.yaml`（実行順・`depends_on`・entry script）
3. `docs/Implementation/IMPLEMENTATION_STATUS_*.md`（Status・entry・主要出力）
4. 実装ディレクトリ上の実 entry script 名・実出力ファイル（上記と矛盾する場合は実装を確認し、矛盾を Known Issues / Update Report に書く）

Canvas の記載が ADR / modules.yaml / IMPLEMENTATION_STATUS と矛盾する場合は、
正本側を優先し Canvas を修正する。

---

#### Reconstruction Rule

既存 `Feature-Pipeline-Scripts.canvas.tsx` が存在する場合、

「見た目の部分編集だけ」

ではなく、

「MODULES / EDGES / Table 行の再調査に基づく再構築」

として扱う。

禁止：

- 旧 Canvas の MODULES / EDGES を事実の根拠として流用する
- Status だけを推測で書く（IMPLEMENTATION_STATUS を見ない）

許可：

- レイアウト用コンポーネント構成（Stack / Card / computeDAGLayout の使い方）の再利用
- EDGE_STYLE・凡例文言の維持

これは SOP-001 / SOP-003 の Reconstruction Rule と同じ考え方である。

---

#### Required Canvas Structure

`Feature-Pipeline-Scripts.canvas.tsx` は以下をこの順で持つ。

```text
1. import（cursor/canvas のみ。外部 npm 禁止）
2. type PillToneSafe / ModuleNode
3. const MODULES: ModuleNode[]
4. const EDGES: { from, to, kind }[]
5. PipelineDAG() … computeDAGLayout + SVG
6. default export … タイトル / Stat / Callout / DAG / Table / depends_on Card
```

##### ModuleNode 必須フィールド

| フィールド | 内容 |
|------------|------|
| `id` | 英小文字短号（EDGES の from/to に使う。一意） |
| `label` | IMPLEMENTATION_STATUS の Module 名（表示名） |
| `script` | entry script または主要入力パス |
| `status` | Current Status（IMPLEMENTATION_STATUS と一致） |
| `tone` | `success` / `info` / `warning` / `neutral`（PillToneSafe） |
| `layer` | Dataset / Orchestrator / Feature / Preprocess / Review / Merge / Dataset / Export / Future / Wet (parallel) 等 |
| `note` | 任意（depends・ADR番号・件数など短く） |

##### EDGES.kind

| kind | 意味 | 描画 |
|------|------|------|
| `data` | オーケストレーションまたは成果物消費 | 実線 |
| `depends` | modules.yaml の `depends_on` | 破線（強調色） |
| `review` | Overview への集約（symlink / QC） | 点線 |
| `future` | 未実装の予定リンク | 粗い破線 |

##### DAG に載せないノード

`PipelineDAG` 内で `MODULES.filter` により DAG 除外する id を明示する
（現行: `rscc`, `lit`）。

新規に「表のみ」モジュールを追加したら、
同じ filter に id を追加する。

##### Table

DAG の有無に関わらず、対象モジュールをすべて列挙する。

列：

```text
Module | Entry script | Key output | Status
```

##### Stat（先頭メトリクス）

再生成時に実数へ更新する。

- Tracked modules 数
- gold_T1-enc 規模（成功 PDB 数のレンジ可）
- Graph-* データセット数
- Not Started 等の要約

---

#### Required Pre-Processing

Canvas 再生成前に必ず以下を実施する。

##### Step 1 — IMPLEMENTATION_STATUS 一覧

```text
docs/Implementation/IMPLEMENTATION_STATUS_*.md
```

各ファイルから Module / Current Status / entry script / 主要 Outputs を抽出する。

SOP-003 が未実行で Status が古い疑いがある場合は、
先に SOP-003 を実行するか、その旨を Update Report に書く。

##### Step 2 — modules.yaml

```text
structure_tools/PDB_analysis/DatasetPreparaton/modules.yaml
```

確認項目：

- 実行順（list order）
- `directory` / `script` / `argv`
- `depends_on`
- `enabled` / `reports_also`

##### Step 3 — 新規ディレクトリの有無

```text
structure_tools/PDB_analysis/
```

IMPLEMENTATION_STATUS 未作成の新ディレクトリがあれば、
Canvas へ入れる前に SOP-003 で Status ファイルを作成することを推奨する。

##### Step 4 — ADR 依存関係の確認

少なくとも次を確認する。

- ADR-018（独立モジュール）
- ADR-024（Review）
- ADR-025（DatasetPreparation）
- ADR-026（GraphBuilder / MergeFeatures 吸収）

---

#### Procedure: モジュール／script 追加時

##### A. MODULES に1要素追加

1. `id` を新規採番（既存と衝突しない短号）
2. `label` / `script` / `status` / `layer` / `tone` / `note` を正本から記入
3. Table 行を同じ内容で追加
4. Stat の件数を更新

##### B. EDGES を更新

| 関係の種類 | kind | 例 |
|------------|------|-----|
| Orchestrator が呼ぶ | `data` | orch → new_module |
| modules.yaml `depends_on` | `depends` | upstream → new_module |
| Overview が集約する | `review` | new_module → overview |
| GraphBuilder が読む | `data` | new_module → graph |
| 将来のみ | `future` | graph → encoder |

孤立ノード（入出辺ゼロ）を DAG に残さない。
表のみモジュールは EDGES を張らず filter で除外する。

##### C. Overview / GraphBuilder 側のドキュメント整合

新 Feature を Overview や GraphBuilder registry に入れた場合のみ
`review` / `data` 辺を追加する。
入れていない場合は辺を捏造しない。

##### D. レイアウト調整

`computeDAGLayout` の `nodeWidth` / `rankGap` / `nodeGap` は
ノード数が増えて重なる場合のみ変更する。
色・コンポーネント種別の大幅変更はしない（書式再現性のため）。

##### E. IDE symlink 確認

```bash
ls -la ~/.cursor/projects/<workspace>/canvases/Feature-Pipeline-Scripts.canvas.tsx
```

リポジトリ正本を指していること。切れていれば再 symlink する。

##### F. （任意）PDF 再生成

Dependency graph の配布が必要な場合：

1. `Feature-Pipeline-Dependency-Graph.html` の SVG / 表を Canvas の MODULES・EDGES に合わせて更新
2. Chrome headless 等で PDF 出力

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="docs/Implementation/Feature-Pipeline-Dependency-Graph.pdf" \
  "file://$(pwd)/docs/Implementation/Feature-Pipeline-Dependency-Graph.html"
```

PDF / HTML は Canvas の派生物であり、正本は `.canvas.tsx` とする。

---

#### Status → tone 対応

| Current Status（IMPLEMENTATION_STATUS） | tone |
|------------------------------------------|------|
| Complete / Mostly Complete / Maintenance（安定稼働） | `success` |
| Maintenance（運用終了寄り） / Review 専用 | `info` または `neutral` |
| In Progress / Planning / Not Started | `warning` |
| その他 | `neutral` |

---

#### Consistency Check

再生成後に確認する。

- MODULES の label が IMPLEMENTATION_STATUS の Module 名と一致するか
- status 文字列が Current Status と一致するか
- `depends` 辺が modules.yaml の `depends_on` と一致するか
- DAG filter 除外 id が「表のみ」方針と一致するか
- Table に全対象モジュールがあるか
- `cursor/canvas` 以外の import が無いか
- Canvas TypeScript check がエラー無いか（エージェント編集時）
- IDE symlink がリポジトリ正本を指すか

---

#### Update Report

Canvas 更新後、以下を報告する。

##### 追加・削除・改名したモジュール（MODULES）

##### 追加・変更した EDGES（kind 付き）

##### IMPLEMENTATION_STATUS / modules.yaml との矛盾

##### PDF / HTML を更新したか

##### IDE symlink の状態

---

#### Non-Goals

本SOPは次を行わない。

- IMPLEMENTATION_STATUS の作成（→ SOP-003）
- Current_State の更新（→ SOP-001）
- ADR / Result の新規作成（→ SOP-002）
- パイプライン実装コードの変更
