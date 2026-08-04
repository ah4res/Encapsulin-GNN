# Implementation Status

## Module

FeatureExtraction_Overview

（Scope (b): 実装ディレクトリ名を ModuleName とする）

実装パス: `structure_tools/PDB_analysis/FeatureExtraction_Overview/`

ADR-024 の Feature Review Gallery の既存実装基盤として ADR-025 からも参照される。
特徴量そのものは生成せず、上流モジュール成果物への相対シンボリックリンクと
`gallery.html` を集約する。

---

## Purpose

Feature 抽出モジュール（DSSP / AA / PISA / Contact / Edge / GrepSubunits）の
notebook・script・出力を横断参照するための集約ディレクトリ。

- By PDB ビュー（`by_pdb/<PDBID>/`）
- gallery（`gallery.html` + `gallery_assets/`）
- By Feature / By Module 入口（`by_module/`）

新規特徴量や新規 plot は生成しない（ADR-024 の Gallery 方針と整合）。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- `sync_links.sh`（by_pdb / gallery_assets / gallery.html / by_module 再生成）
- `gallery.html`（約 1.17 MB、41 PDB セクション）
- `by_pdb/` 41 PDB、シンボリックリンク 945・broken 0
- `gallery_assets/` 41 PDB、リンク 743・broken 0
- `by_module/` → DSSP / AA / PISA / Contact / Edge / GrepSubunits（全て解決）
- `overview.ipynb`
- README.md

判定基準: gallery / リンク集約の実生成を確認

---

## In Progress

- なし（コア Gallery は稼働）

---

## Not Implemented

- ADR-024 が求める本格 By Feature ビューの自動特徴量一覧（CSV ヘッダ / manifest 駆動）
  （現状は主要 QC 図中心の gallery）
- Feature 採否履歴・Review コメント保存（ADR-024 Low）
- 上流未生成 PDB（例: 8IKA は Grep のみ）のカバレッジ均一化

---

## Outputs

- `gallery.html`
- `by_pdb/<PDBID>/{DSSP,AA,PISA,Contact,Edge,GrepSubunits}/...`（相対リンク）
- `gallery_assets/`
- `by_module/`
- `notebooks/` / `scripts/` へのリンク

---

## Validation Status

- シンボリックリンク健全性: broken 0 を確認
- gold_T1-enc と同規模の 41 PDB を gallery に掲載
- 8IKA 等は上流 Feature 未生成のためスカスカ（リンク切れではなく欠落）

正式な Result は未作成。ADR-024 Validation Results は N/A。

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-024（Feature Review Gallery）
- ADR-025（Overview を Review に利用）

---

## Known Issues

- By Feature の完全自動一覧は未達（ADR-024 High の一部）
- PDB ごとのモジュールカバレッジ差（Grep のみの PDB）
- sync 後の git 管理方針（大量 symlink）が未整理の可能性

---

## Next Actions

High

- ADR-024 By Feature ビューを manifest/CSV ヘッダ駆動で強化

Medium

- Feature Selection 記録との連携設計
- カバレッジ欠落 PDB の明示（gallery 上の missing 表示）

Low

- Review コメント保存

---

## Completion Estimate

Design: 90%

Implementation: 80%

Validation: 70%

Overall: 80%

---

### Current_State Summary

- FeatureExtraction_Overview は ADR-024 Gallery の実装基盤として稼働（41 PDB、リンク健全）。
- 本格 By Feature 自動一覧は未達。Current_State に Feature Review 工程の実装進捗として追記可能。
