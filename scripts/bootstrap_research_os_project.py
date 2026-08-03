#!/usr/bin/env python3
"""
bootstrap_research_os_project.py

Encapsulin-GNN で運用している Research OS
(SOP で ADR / Result を管理し、Current_State(+Summary) へ集約し、
Implementation Status で実装進捗を追跡するプロジェクト管理システム)
を、新しいプロジェクトへそのまま移植するためのブートストラップスクリプト。

必要な入力は3種類のみ。

    - Project_Charter.md
    - Result-000.md
    - Roadmap (Roadmap_A_Infrastructure.md / Roadmap_B_DryResearch.md /
      Roadmap_C_WetResearch.md)

この3種類のドキュメントから、06_Encapsulin-GNN と同じ
ディレクトリ構成・SOP・README を備えた新規プロジェクトを生成する。

Usage (推奨: 入力ディレクトリ方式)
-----------------------------------
入力ディレクトリに以下のファイルを置く。

    <input_dir>/Project_Charter.md
    <input_dir>/Result-000.md
    <input_dir>/Roadmap_A_Infrastructure.md
    <input_dir>/Roadmap_B_DryResearch.md
    <input_dir>/Roadmap_C_WetResearch.md

    または <input_dir>/Roadmap/ 以下に上記3ファイルを置いてもよい。

    python scripts/bootstrap_research_os_project.py \\
        --input-dir /path/to/new_project_inputs \\
        --output /path/to/00_Projects/Project_XX_foo/NN_NewProjectName

Usage (個別ファイル指定方式)
-----------------------------------
    python scripts/bootstrap_research_os_project.py \\
        --project-charter /path/to/Project_Charter.md \\
        --result-000 /path/to/Result-000.md \\
        --roadmap-a /path/to/Roadmap_A_Infrastructure.md \\
        --roadmap-b /path/to/Roadmap_B_DryResearch.md \\
        --roadmap-c /path/to/Roadmap_C_WetResearch.md \\
        --output /path/to/00_Projects/Project_XX_foo/NN_NewProjectName

Notes
-----
- 標準ライブラリのみに依存する（サードパーティ依存なし）。
- SOP-001 (ver1.2) / SOP-002 / SOP-003 および README.md は、本スクリプトが
  同梱されている Research OS 参照プロジェクト（デフォルトではこのスクリプトが
  置かれている 06_Encapsulin-GNN。--source-root で変更可能）から読み込み、
  ほぼそのまま新規プロジェクトへ転用する（パス等の固有情報のみ置換する）。
- ADR/*, Results/*（Result-000を除く）, Current_State.md,
  Current_State_Summary.md は転用元からコピーしない。新規プロジェクトは
  「ADRゼロ・Result-000のみ」のクリーンな状態から開始する。
- Current_State.md / Current_State_Summary.md は SOP-001 の
  Required Sections に従った初期スケルトンとして生成される。
  ADRが蓄積した段階で、SOP-001に従った本来の「再構築」を
  Cursor等に実行させることを前提とする（本スクリプトはあくまで初期足場）。
- git init は行わない（--git-init を指定した場合のみ実行）。
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_SOURCE_ROOT = SCRIPT_PATH.parent.parent  # scripts/.. -> 06_Encapsulin-GNN

REQUIRED_DIRS = [
    "docs/ADR",
    "docs/Results",
    "docs/Roadmap",
    "docs/Implementation",
    "docs/SOP",
    "src",
    "data",
    "analysis",
    "manuscript",
]

# .gitkeep を置くディレクトリ（コンテンツが最初から入るディレクトリは除く）
GITKEEP_DIRS = [
    "docs/ADR",
    "docs/Implementation",
    "src",
    "data",
    "analysis",
    "manuscript",
]

GITIGNORE_CONTENT = """__pycache__/
*.pyc

.ipynb_checkpoints/

.env

.DS_Store

data/raw/

results/tmp/

*.log
"""


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s*(.+?)\s*$")


def extract_section(text: str, heading_pattern: str) -> str | None:
    """
    見出しテキストが heading_pattern（正規表現、大文字小文字無視）に
    マッチする最初の見出しを探し、その本文（次の同レベル以下の見出しまで）
    を返す。見つからない場合は None。
    """
    lines = text.splitlines()
    start_idx = None
    start_level = None
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m and re.search(heading_pattern, m.group(2), re.IGNORECASE):
            start_idx = i
            start_level = len(m.group(1))
            break
    if start_idx is None:
        return None
    body: list[str] = []
    for line in lines[start_idx + 1 :]:
        m = _HEADING_RE.match(line)
        if m and len(m.group(1)) <= start_level:
            break
        body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body).strip() or None


# ADR/Result templates（README.md / SOP-002 参照）は、フィールド名を
# Markdown見出し（## Objective 等）としてではなく、独立した行の
# プレーンテキストラベル（Objective\n\n本文...）として書く運用になっている。
# そのため通常の見出し検出（extract_section）だけでは Objective / Conclusion /
# Next Action 等を拾えない。以下のラベルベース抽出と併用する。
RESULT_FIELD_LABELS = [
    "Date",
    "Track",
    "Related ADR",
    "Objective",
    "Method",
    "Result",
    "Interpretation",
    "Conclusion",
    "Next Action",
]


def _field_label_at(line: str, labels: list[str]) -> str | None:
    stripped = line.strip().lstrip("#").strip()
    for label in labels:
        if stripped.lower() == label.lower():
            return label
    return None


def extract_plain_field(text: str, label: str, labels: list[str] = RESULT_FIELD_LABELS) -> str | None:
    """
    'Objective' のように、独立した行に書かれたプレーンテキストラベルを探し、
    次のラベル行（またはテキスト末尾）までの本文を返す。
    """
    lines = text.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if _field_label_at(line, [label]) is not None:
            start_idx = i
            break
    if start_idx is None:
        return None
    body: list[str] = []
    for line in lines[start_idx + 1 :]:
        if _field_label_at(line, labels) is not None:
            break
        body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body).strip() or None


def extract_result_field(text: str, label: str) -> str | None:
    """
    プレーンラベル形式（推奨/標準）とMarkdown見出し形式の両方に対応した
    フィールド抽出。プレーンラベル形式を優先する。
    """
    return extract_plain_field(text, label) or extract_section(text, rf"^{re.escape(label)}$")


def extract_title(text: str, default: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else default


def extract_track_label(text: str, default: str) -> str:
    """Roadmap H1（例: '# Roadmap A: Infrastructure'）からトラック名のみを取り出す。"""
    title = extract_title(text, default)
    if ":" in title:
        return title.split(":", 1)[1].strip()
    return title


def first_meaningful_line(text: str | None) -> str | None:
    if not text:
        return None
    for line in text.splitlines():
        line = line.strip().strip("#").strip()
        if line and line != "---":
            return line
    return None


def first_sentence(text: str | None) -> str | None:
    """
    セクション本文を1文（句点まで）にまとめて返す。
    Vision等が複数行に折り返されている場合でも、文が途中で
    切れないようにするためのヘルパー。
    """
    if not text:
        return None
    flattened = "".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#") and line.strip() != "---"
    )
    if not flattened:
        return None
    for sep in ("。", "\n"):
        if sep in flattened:
            return flattened.split(sep, 1)[0].strip() + ("。" if sep == "。" else "")
    return flattened.strip()


def extract_bullets(text: str | None, limit: int = 5) -> list[str]:
    if not text:
        return []
    bullets = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("- ", "* ")):
            bullets.append(line[2:].strip())
        if len(bullets) >= limit:
            break
    return bullets


def indent(text: str, prefix: str = "  ") -> str:
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())


# ---------------------------------------------------------------------------
# Input data model
# ---------------------------------------------------------------------------


@dataclass
class ProjectInputs:
    charter_path: Path
    result000_path: Path
    roadmap_a_path: Path
    roadmap_b_path: Path
    roadmap_c_path: Path

    charter_text: str = field(default="", init=False)
    result000_text: str = field(default="", init=False)
    roadmap_a_text: str = field(default="", init=False)
    roadmap_b_text: str = field(default="", init=False)
    roadmap_c_text: str = field(default="", init=False)

    def load(self) -> None:
        self.charter_text = self.charter_path.read_text(encoding="utf-8")
        self.result000_text = self.result000_path.read_text(encoding="utf-8")
        self.roadmap_a_text = self.roadmap_a_path.read_text(encoding="utf-8")
        self.roadmap_b_text = self.roadmap_b_path.read_text(encoding="utf-8")
        self.roadmap_c_text = self.roadmap_c_path.read_text(encoding="utf-8")


def get_source_project_name(source_root: Path) -> str:
    """転用元プロジェクトの表示名をREADME.mdのH1から推定する。"""
    readme = source_root / "README.md"
    default = source_root.name
    if not readme.is_file():
        return default
    title = extract_title(readme.read_text(encoding="utf-8"), default)
    return re.sub(r"\s*Research Operating System\s*$", "", title).strip() or default


def resolve_inputs(args: argparse.Namespace) -> ProjectInputs:
    input_dir = Path(args.input_dir).resolve() if args.input_dir else None

    def pick(explicit: str | None, filename_candidates: list[str]) -> Path:
        if explicit:
            p = Path(explicit).resolve()
            if not p.is_file():
                sys.exit(f"[ERROR] 指定されたファイルが見つかりません: {p}")
            return p
        if input_dir is None:
            sys.exit(
                "[ERROR] --input-dir か、個別の --project-charter 等の"
                "いずれかで入力ファイルを指定してください。"
            )
        for name in filename_candidates:
            for base in (input_dir, input_dir / "Roadmap"):
                p = base / name
                if p.is_file():
                    return p
        sys.exit(
            f"[ERROR] {input_dir} 配下に {filename_candidates} が見つかりません。"
        )

    charter = pick(args.project_charter, ["Project_Charter.md"])
    result000 = pick(args.result_000, ["Result-000.md"])
    roadmap_a = pick(args.roadmap_a, ["Roadmap_A_Infrastructure.md"])
    roadmap_b = pick(args.roadmap_b, ["Roadmap_B_DryResearch.md"])
    roadmap_c = pick(args.roadmap_c, ["Roadmap_C_WetResearch.md"])

    inputs = ProjectInputs(charter, result000, roadmap_a, roadmap_b, roadmap_c)
    inputs.load()
    return inputs


# ---------------------------------------------------------------------------
# README generation
# ---------------------------------------------------------------------------


def build_readme(
    inputs: ProjectInputs, project_title: str, project_dir_name: str, source_project_name: str
) -> str:
    vision = extract_section(inputs.charter_text, r"^Vision$")
    vision_sentence = first_sentence(vision)
    purpose_clause = (
        vision_sentence.rstrip("。")
        if vision_sentence
        else "docs/Project_Charter.md に記載された目的を達成する"
    )

    roadmap_a_title = extract_track_label(inputs.roadmap_a_text, "Infrastructure")
    roadmap_b_title = extract_track_label(inputs.roadmap_b_text, "Dry Research")
    roadmap_c_title = extract_track_label(inputs.roadmap_c_text, "Wet Research")

    return f"""# {project_title} Research Operating System

## Purpose

本プロジェクトは、{purpose_clause}ことを目的とする。

詳細な研究目的・科学的問い・研究範囲・成功条件は `docs/Project_Charter.md` を正本とする。

本研究では、

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

研究期間を通じて、

- なぜその意思決定を行ったのか
- 何が分かったのか
- 現在どこまで進んでいるのか
- コーディング・実装がどこまで進んでいるのか

を追跡可能とするため、本 Research Operating System（Research OS）を採用する。

本Research OSは {source_project_name} プロジェクトで確立されたものを転用しており、
ADR/Result/Roadmap による意思決定管理に加えて、
Implementation Status による実装進捗管理、
Current_State / Current_State_Summary によるAI向け・人間向け
デュアルダッシュボードまでを標準装備する。

---

# Basic Principles

本プロジェクトでは GitHub Repository を唯一の正本（Single Source of Truth）とする。

チャット履歴は保存対象としない。

保存対象は以下とする。

- Project Charter
- Roadmap
- Current State（+ Current State Summary）
- ADR
- Result
- Implementation Status（補助資料）

AIとの対話履歴そのものではなく、

- 意思決定
- 実験結果
- 解析結果
- 実装進捗

を記録する。

---

# Repository Structure

```text
{project_dir_name}/

README.md

docs/

├─ Project_Charter.md
├─ Current_State.md
├─ Current_State_Summary.md

├─ Roadmap/
│  ├─ Roadmap_A_Infrastructure.md
│  ├─ Roadmap_B_DryResearch.md
│  └─ Roadmap_C_WetResearch.md

├─ ADR/
│  ├─ ADR-001.md
│  └─ ...

├─ Results/
│  ├─ Result-000.md
│  └─ ...

├─ Implementation/
│  └─ IMPLEMENTATION_STATUS_<Module>.md

└─ SOP/
   ├─ SOP-001_Current_State_Update.md
   ├─ SOP-002_ADR-Result_Creation.md
   └─ SOP-003_Implementation_Status_Update.md

src/
data/
analysis/
manuscript/
```

---

# Document Roles

## Project_Charter.md

プロジェクトの憲章。

定義する内容

- 研究目的
- 科学的問い
- 研究範囲
- 成功条件

原則として頻繁に変更しない。

研究目的そのものが変更される場合のみ更新する。

---

## Roadmap

中長期計画を管理する。

以下の3トラックで構成する。

### Track A: {roadmap_a_title}

研究基盤整備

---

### Track B: {roadmap_b_title}

AI・計算解析

---

### Track C: {roadmap_c_title}

実験検証

---

Roadmap は中長期計画を示す。

日常的には更新しない。

大きな方針変更が生じた場合のみ更新する。

---

## Current_State.md

プロジェクト全体のダッシュボード（AI向け詳細版）。

最重要ファイル。

壁打ち開始時には必ず参照する。

記載内容

- 現在位置
- 最近の重要決定
- 最近の重要結果
- 現在の課題
- 次の意思決定事項
- 次のアクション

Current_State は ADR と Result（および Implementation Status）を
要約したものとする。

---

## Current_State_Summary.md

プロジェクト全体のダッシュボード（人間向け要約版）。

PI・開発者・将来の自分が短時間で現在地を把握するための
エグゼクティブサマリー。

Current_State.md の要約であり、ADR・Resultの代替ではない。

Current_State.md と同時に更新する（Dual Dashboard Principle）。

---

## Implementation Status（docs/Implementation/）

コーディング・実装の達成度を確認するための補助資料。

ADRやResultの代替ではなく、
Current_State更新時に参照する実装進捗レポートとして扱う。

1モジュール = 1ファイル（`IMPLEMENTATION_STATUS_<Module>.md`）とする。

---

# ADR

ADR = Architecture Decision Record

本プロジェクトにおける重要な意思決定を記録する。

ソフトウェア開発だけではなく、

- 研究方針
- 実験方針
- データセット方針
- モデル選択
- 検証戦略

もADRとして扱う。

---

## ADRを書く基準

記録するもの

- ノード定義
- エッジ定義
- モデル選択
- 学習方針
- 評価方針
- Wet実験方針
- 検証戦略
- 研究上重要な判断

記録しないもの

- 軽微な実装変更
- バグ修正
- ファイル整理
- 一時的試行

---

## ADR命名規則

```text
ADR-001.md
ADR-002.md
ADR-003.md
...
```

通し番号とする。

Trackごとの番号体系は採用しない。

---

## ADRテンプレート

```markdown
# ADR-XXX

Date

Track

Question

Decision

Rationale

Alternatives Considered

Status

Validation Results / ex.) - Results-###
```

statusには以下を記載する
Proposed/Trial/Accepted/Rejected/Superseded -> ADR###

---

# Results

Result は

「何を行い、何が分かったか」

を記録する。

Result は実験ノートではない。

研究方針に影響を与える重要な結果のみ記録する。

---

## Resultを書く基準

記録するもの

- モデル性能評価
- 特徴量比較
- モデル比較
- 変異体評価
- 粒子形成評価（該当する場合）
- AI予測の検証結果
- Infrastructure構築成果

記録しないもの

- 日常実験記録
- 単なる作業ログ
- 一時的な失敗

---

## Result命名規則

```text
Result-001.md
Result-002.md
Result-003.md
...
```

通し番号とする。

Trackごとの番号体系は採用しない。

---

Result-000はResearch OS導入以前の運用方針確立を記録する例外的なResultである。
Result-001以降は、関連するADRを少なくとも1件持つものとする。

---

## Resultテンプレート

```markdown
# Result-XXX

Date

Track

Related ADR / ex.) ADR-###

Objective

Method

Result

Interpretation

Conclusion

Next Action
```

すべてのResultは、関連するADRを最低1件記載する。
関連ADRが存在しない場合は "None" と記載する。

---

# Relationship Between Documents

```text
Discussion

↓

ADR

↓

Experiment / Analysis / Implementation

↓

Result / Implementation Status

↓

Current_State (+ Current_State_Summary)

↓

Next Discussion
```

Current_State は常に現在地を示す。

ADR と Result は履歴保管庫である。

Implementation Status は実装進捗の補助資料である。

---

# AI Usage Policy

## Copilot

役割

- 壁打ち
- アイデア検討
- 批判的レビュー
- ADR作成支援

Copilotは長期記憶を持たない。

壁打ち時には

- Project_Charter
- Current_State（またはCurrent_State_Summary）

を入力として利用する。

---

## Cursor

役割

- コーディング
- 実装
- 文書解析
- Current_State / Current_State_Summary 更新支援
- Implementation Status 更新支援

Cursorは

- Project_Charter
- Roadmap
- ADR
- Result
- Implementation Status

を参照する。

定期的にADR・Result・Implementation Statusを統合し、

Current_State および Current_State_Summary を更新する。

---

# Operational Rules

重要な議論を行った場合

1. ADR作成
2. Current_State更新
3. Git Commit

重要な結果が得られた場合

1. Result作成
2. Current_State更新
3. Git Commit

実装が節目まで進んだ場合

1. Implementation Status更新（SOP-003）
2. Current_State更新
3. Git Commit

---

# Guiding Principle

未来の自分が、

「なぜその判断をしたのか」

を理解できることを最優先とする。

記録の目的は保存ではない。

研究の再現性、継続性、共有可能性を高めることである。

## File Ownership Policy

### Human Managed

以下のファイルは人間のみが編集する。

- Project_Charter.md
- Roadmap/*
- ADR/*
- Results/*
- README.md
- SOP/*

### Cursor Managed

以下のファイルはCursorによる更新を許可する。

- Current_State.md
- Current_State_Summary.md
- Implementation/*（IMPLEMENTATION_STATUS_*.md）

これらはプロジェクトの現在地・実装進捗を示す
ダッシュボード／補助資料であり、

ADR
Result
Roadmap

から生成される派生文書として扱う。
"""


# ---------------------------------------------------------------------------
# Current_State.md / Current_State_Summary.md initial skeletons
# ---------------------------------------------------------------------------


def build_current_state(inputs: ProjectInputs, project_title: str, today: str) -> str:
    vision = extract_section(inputs.charter_text, r"^Vision$")
    result000_objective = extract_result_field(inputs.result000_text, "Objective")
    result000_conclusion = extract_result_field(inputs.result000_text, "Conclusion")
    result000_next = extract_result_field(inputs.result000_text, "Next Action")

    project_summary = first_sentence(vision) or (
        f"{project_title}の目的は docs/Project_Charter.md を参照。"
    )
    infra_now = (
        first_sentence(result000_conclusion)
        or first_sentence(result000_objective)
        or "Result-000により研究基盤の初期整備が行われた。"
    )
    next_actions = extract_bullets(result000_next, limit=10)
    next_actions_block = (
        "\n".join(f"- {a}" for a in next_actions)
        if next_actions
        else "- （Result-000のNext Actionを参照し、最初のADR/Resultを作成してください）"
    )

    return f"""WARNING

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
Project_Charter / Roadmap / ADR全件 / Result全件から再構築する運用とする。

本ファイルはプロジェクト立ち上げ時の初期スケルトンである。
ADRが蓄積した段階で、SOP-001に従った本来の再構築を実施すること。

---

# Current State

Last Updated: {today}

## Project Summary

{project_summary}

- AI解析（Dry Research）
- 実験検証（Wet Research）
- 研究基盤整備（Infrastructure）

を並行して進める。

---

## Infrastructure

### 現在地

{infra_now}

### 最近の重要決定

- （まだADRが存在しない）

### 最近の重要結果

- Result-000: {first_sentence(result000_objective) or "研究基盤整備の初期結果"}

### 現在の課題

- ADRがまだ1件も作成されていない
- Research OS運用が試験開始段階である

### 次のアクション

{next_actions_block}

---

## Dry Research

### 現在地

Roadmap_B_DryResearch.md に記載の計画段階であり、具体的な着手はまだ記録されていない。

### 最近の重要決定

- （まだADRが存在しない）

### 最近の重要結果

- （まだResultが存在しない）

### 現在の課題

- Dataset Constructionが未着手（B1相当）

### 次のアクション

- Roadmap_B_DryResearch.mdの最初のマイルストーンに着手し、ADR/Resultを作成する

---

## Wet Research

### 現在地

Roadmap_C_WetResearch.md に記載の計画段階であり、具体的な着手はまだ記録されていない。

### 最近の重要決定

- （まだADRが存在しない）

### 最近の重要結果

- （まだResultが存在しない）

### 現在の課題

- 実験系構築が未着手（C1相当）

### 次のアクション

- Roadmap_C_WetResearch.mdの最初のマイルストーンに着手し、ADR/Resultを作成する

---

## Active ADR

Cursor Suggested

- （まだADRが存在しない）

---

## Important Results

Cursor Suggested

- Result-000: {first_sentence(result000_objective) or "研究基盤整備の初期結果"}

---

## Open Questions

Cursor Generated

- Dry Research / Wet Researchのどちらから着手するか
- 最初に必要なADRは何か（データセット定義／実験系定義等）
- Infrastructure整備のうち、Research活動開始前に必須なものは何か

---

## Top Priority Decisions

今後1〜2週間で決定すべき事項

- 最初のADRの作成（研究方針・データセット方針等）

---

## Risks

- Research OS運用が試験開始段階であり、記録の抜け漏れが生じるリスクがある

---

## Next Milestones

- 最初のADR作成
- 最初のResult作成
- Research OS本格運用の定着

---

## Update Policy

SupersededされたADRは反映しない。

RejectedされたADRは反映しない。

Resultによって否定された仮説は
Current_Stateから除去する。

現在有効な内容のみ記載する。
"""


def build_current_state_summary(inputs: ProjectInputs, project_title: str, today: str) -> str:
    result000_objective = extract_result_field(inputs.result000_text, "Objective")

    return f"""WARNING

本ファイルは `Current_State.md` の要約版（エグゼクティブサマリー）である。

詳細な根拠・議論は `Current_State.md`、
および正本である ADR / Results / Roadmap を参照すること。

矛盾がある場合は `Current_State.md` および正本（ADR/Results/Roadmap）を優先する。

SOP-001（ver1.2）に基づき生成。プロジェクト立ち上げ時の初期スケルトンである。

---

# Current State Summary

## Last Updated

{today}

## Executive Summary

{project_title}は立ち上げ段階であり、Research基盤整備（Result-000）が完了した状態。
ADRはまだ1件も作成されておらず、Dry Research / Wet Researchともに未着手。
最初のADR作成が最優先事項。

---

## Current Position

### Infrastructure

Result-000により初期の研究基盤整備が完了。Research OS運用を開始した段階。

### Dry Research

Roadmap_B_DryResearch.mdの計画段階。未着手。

### Wet Research

Roadmap_C_WetResearch.mdの計画段階。未着手。

---

## Implementation Status

- （まだ実装モジュールが存在しない）

---

## Current Bottlenecks

- 最初のADRが未作成であり、具体的な研究方針が確定していない

---

## Recent Important Decisions

- （まだADRが存在しない）

---

## Recent Important Results

- Result-000: {first_sentence(result000_objective) or "研究基盤整備の初期結果"}

---

## Top Priority Decisions

- 最初のADR（研究方針・データセット方針・実験方針等）の作成

---

## Risks

- Research OS運用が試験開始段階であり、記録の抜け漏れが生じるリスクがある

---

## Next Milestones

- 最初のADR作成
- 最初のResult作成

---

詳細は `Current_State.md` を参照。
"""


# ---------------------------------------------------------------------------
# SOP templating (reuse almost as-is, only path / provenance substitution)
# ---------------------------------------------------------------------------

SOP_RELATIONSHIP_SECTION_RE = re.compile(
    r"(##### Relationship to Previous Versions\n\n).*?(\n---\n)",
    re.DOTALL,
)


def build_sop_copies(source_root: Path, output_root: Path, source_project_name: str) -> dict[str, str]:
    """
    source_root配下のSOP-001(ver1.2)/SOP-002/SOP-003を読み込み、
    新規プロジェクト向けにパス等の固有情報のみ置換したテキストを返す。
    戻り値: {出力ファイル名: 本文}
    """
    sop_dir = source_root / "docs" / "SOP"
    sop1_src = sop_dir / "SOP-001_Current_State_Update_ver1.2.md"
    sop2_src = sop_dir / "SOP-002_ADR-Result_Creation.md"
    sop3_src = sop_dir / "SOP-003_Implementation_Status_Update.md"

    for p in (sop1_src, sop2_src, sop3_src):
        if not p.is_file():
            sys.exit(f"[ERROR] 転用元SOPが見つかりません: {p}")

    provenance_note = (
        f"> 本ファイルは {source_project_name} プロジェクトの Research OS で確立された "
        "{name} を元にしたテンプレートである。転用にあたり、配置パス等の"
        "プロジェクト固有情報のみ置換している。\n\n"
    )

    new_sop_dir = output_root / "docs" / "SOP"

    # --- SOP-001 ---
    sop1_text = sop1_src.read_text(encoding="utf-8")
    sop1_text = sop1_text.replace(str(source_root), str(output_root))
    sop1_text = SOP_RELATIONSHIP_SECTION_RE.sub(
        lambda m: m.group(1)
        + (
            f"本SOPは {source_project_name} プロジェクトの SOP-001（ver1.2）を"
            "元にしたテンプレートである。\n\n"
            "本プロジェクトではver1.1からの移行履歴を持たないため、"
            "ver1.2の内容をそのまま初期運用ルールとして採用する。\n"
        )
        + m.group(2),
        sop1_text,
        count=1,
    )
    sop1_text = provenance_note.format(name="SOP-001_Current_State_Update_ver1.2.md") + sop1_text

    # --- SOP-002 ---
    sop2_text = sop2_src.read_text(encoding="utf-8")
    sop2_text = sop2_text.replace(str(source_root), str(output_root))
    sop2_text = provenance_note.format(name="SOP-002_ADR-Result_Creation.md") + sop2_text

    # --- SOP-003 ---
    sop3_text = sop3_src.read_text(encoding="utf-8")
    sop3_text = sop3_text.replace(str(source_root), str(output_root))
    sop3_text = provenance_note.format(name="SOP-003_Implementation_Status_Update.md") + sop3_text
    sop3_text += (
        "\n\n---\n\n"
        "#### Adaptation Note\n\n"
        "Scope配下のモジュール例（FeatureContact等）はEncapsulin-GNN固有の例である。\n\n"
        "新規プロジェクトで最初にIMPLEMENTATION_STATUSを作成する際は、\n"
        "自プロジェクトの実装モジュール構成を定義するADRを参照し、\n"
        "本SOPのScope/File Naming Ruleの例を自プロジェクトのモジュール名へ置き換えて運用する。\n"
    )

    return {
        "SOP-001_Current_State_Update.md": sop1_text,
        "SOP-002_ADR-Result_Creation.md": sop2_text,
        "SOP-003_Implementation_Status_Update.md": sop3_text,
    }


# ---------------------------------------------------------------------------
# Main bootstrap logic
# ---------------------------------------------------------------------------


def create_dirs(output_root: Path) -> None:
    for d in REQUIRED_DIRS:
        (output_root / d).mkdir(parents=True, exist_ok=True)
    for d in GITKEEP_DIRS:
        keep = output_root / d / ".gitkeep"
        if not any((output_root / d).iterdir()):
            keep.write_text("", encoding="utf-8")


def write_if_absent(path: Path, content: str, force: bool, created: list[str], skipped: list[str]) -> None:
    if path.exists() and not force:
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))


def copy_if_absent(src: Path, dst: Path, force: bool, created: list[str], skipped: list[str]) -> None:
    if dst.exists() and not force:
        skipped.append(str(dst))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    created.append(str(dst))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Project_Charter.md / Result-000.md / Roadmap から、"
            "06_Encapsulin-GNNと同一構成のResearch OSプロジェクトを新規生成する。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input-dir", help="Project_Charter.md等をまとめて置いたディレクトリ")
    parser.add_argument("--project-charter", help="Project_Charter.md への個別パス")
    parser.add_argument("--result-000", help="Result-000.md への個別パス")
    parser.add_argument("--roadmap-a", help="Roadmap_A_Infrastructure.md への個別パス")
    parser.add_argument("--roadmap-b", help="Roadmap_B_DryResearch.md への個別パス")
    parser.add_argument("--roadmap-c", help="Roadmap_C_WetResearch.md への個別パス")
    parser.add_argument("--output", required=True, help="新規プロジェクトの出力先ディレクトリ")
    parser.add_argument(
        "--source-root",
        default=str(DEFAULT_SOURCE_ROOT),
        help="転用元Research OSプロジェクトのルート（デフォルト: 06_Encapsulin-GNN）",
    )
    parser.add_argument("--project-name", help="README等に使うプロジェクト表示名（省略時はProject_Charter.mdから抽出）")
    parser.add_argument("--git-init", action="store_true", help="生成後に git init を実行する")
    parser.add_argument(
        "--force",
        action="store_true",
        help="出力先に既存ファイルがあっても上書きする（デフォルトは既存ファイルをスキップ）",
    )
    args = parser.parse_args()

    inputs = resolve_inputs(args)
    source_root = Path(args.source_root).resolve()
    if not (source_root / "docs" / "SOP").is_dir():
        sys.exit(f"[ERROR] --source-root が Research OS プロジェクトに見えません: {source_root}")

    source_project_name = get_source_project_name(source_root)

    output_root = Path(args.output).resolve()
    project_dir_name = output_root.name
    project_title = args.project_name or extract_title(
        inputs.charter_text, default=project_dir_name
    )
    # "# Project Charter" のような汎用タイトルだった場合は Project Name セクションを見る
    if project_title.strip().lower() in {"project charter", "プロジェクト憲章"}:
        name_section = extract_section(inputs.charter_text, r"^Project Name$")
        project_title = first_meaningful_line(name_section) or project_dir_name

    today = date.today().isoformat()

    created: list[str] = []
    skipped: list[str] = []

    create_dirs(output_root)

    # --- 入力ドキュメントの配置 ---
    copy_if_absent(inputs.charter_path, output_root / "docs" / "Project_Charter.md", args.force, created, skipped)
    copy_if_absent(inputs.result000_path, output_root / "docs" / "Results" / "Result-000.md", args.force, created, skipped)
    copy_if_absent(inputs.roadmap_a_path, output_root / "docs" / "Roadmap" / "Roadmap_A_Infrastructure.md", args.force, created, skipped)
    copy_if_absent(inputs.roadmap_b_path, output_root / "docs" / "Roadmap" / "Roadmap_B_DryResearch.md", args.force, created, skipped)
    copy_if_absent(inputs.roadmap_c_path, output_root / "docs" / "Roadmap" / "Roadmap_C_WetResearch.md", args.force, created, skipped)

    # --- SOP転用 ---
    for filename, text in build_sop_copies(source_root, output_root, source_project_name).items():
        write_if_absent(output_root / "docs" / "SOP" / filename, text, args.force, created, skipped)

    # --- .gitignore ---
    write_if_absent(output_root / ".gitignore", GITIGNORE_CONTENT, args.force, created, skipped)

    # --- README.md ---
    readme_text = build_readme(inputs, project_title, project_dir_name, source_project_name)
    write_if_absent(output_root / "README.md", readme_text, args.force, created, skipped)

    # --- Current_State.md / Current_State_Summary.md 初期スケルトン ---
    cs_text = build_current_state(inputs, project_title, today)
    write_if_absent(output_root / "docs" / "Current_State.md", cs_text, args.force, created, skipped)

    css_text = build_current_state_summary(inputs, project_title, today)
    write_if_absent(output_root / "docs" / "Current_State_Summary.md", css_text, args.force, created, skipped)

    if args.git_init:
        subprocess.run(["git", "init"], cwd=output_root, check=True)
        created.append(f"(git repository initialized at {output_root})")

    # --- レポート ---
    print(f"Research OS project bootstrapped at: {output_root}\n")
    print(f"Project title: {project_title}")
    print(f"Source SOP root: {source_root}\n")
    print(f"Created ({len(created)}):")
    for c in created:
        print(f"  - {c}")
    if skipped:
        print(f"\nSkipped (already existed, use --force to overwrite) ({len(skipped)}):")
        for s in skipped:
            print(f"  - {s}")
    print(
        "\nNext steps:\n"
        "  1. docs/Project_Charter.md / Roadmap を確認する\n"
        "  2. Copilotとの壁打ちで最初のADRを作成する（SOP-002）\n"
        "  3. ADR/Resultが蓄積したら SOP-001 に従って Current_State を本格再構築する\n"
        "  4. 実装が進んだら SOP-003 に従って Implementation Status を作成する\n"
    )


if __name__ == "__main__":
    main()
