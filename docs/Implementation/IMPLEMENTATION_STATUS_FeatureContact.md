# Implementation Status

## Module

FeatureContact

（実装名: `CountInteractionWithNCSchain`）

実装パス: `structure_tools/PDB_analysis/CountInteractionWithNCSchain/`

共有基盤: `structure_tools/PDB_analysis/common/seqres.py`

---

## Purpose

Reference Chain A の各残基について、近傍 NCS partner chain との
Cα距離帯別接触数・最短距離を特徴量化する。

ADR-016 / ADR-017 に従い、サブユニット間相互作用はエッジではなく
ノード特徴量として保持し、partner chain 情報を合算せず残す。

入力は `PDB-GrepSubunits/results_<PDBID>/neighbor_cluster.pdb`。
SEQRES 取得用 mmCIF は FeaturesDSSP `data/<PDB>.cif` を参照。

ADR-022 により参照残基 Node = SEQRES（missing 含む）。
missing 残基の接触量は計算不可のため NaN。

本書は ADR / Result の代替ではない。
`docs/ADR/`・`docs/Results/` が正本であり、
`Current_State.md` 更新時に参照する実装進捗の補助資料である。

更新履歴は git のコミット履歴を正本とする（本文に日付を固定記載しない）。

---

## Current Status

Mostly Complete

---

## Completed

- neighbor_cluster.pdb 自動探索
- Cαのみによる距離計算（ATOM / polymer）
- 距離帯別累積接触数（2 / 4 / 6 / 8 / 10 Å）
- partner chain 別レコード保持（`partner_chain` 列）
- ADR-022: SEQRES 参照残基への展開、`is_missing` / `missing_segment_length`
- Missing 残基の距離・接触カウント = NaN（partner 行は維持）
- `contact_features.csv` / `contact_features_summary.csv` 生成
- `seqres_nodes.csv` 生成
- `summary.txt` 生成
- 可視化（heatmap / distance / profile / histogram / top residues / contribution）
- CLI（`count_interaction_with_ncs_chain.py`）
- DatasetPreparation 経由の batch 実行（`done.flag` 運用）

確認 PDB: gold_T1-enc 由来 **39 構造**（全 results_* で CSV + summary.txt + plots 完備）
判定基準: CSV・画像・summary の実生成まで確認できたもののみ Completed

代表例の参照ノード数: 3DKT 265、7S21 301、9B9I 281（SEQRES 長と一致）

---

## In Progress

- なし（単体モジュールとしてのコア実装・Dataset A 規模の再計算は完了）

---

## Not Implemented

- 対称軸分類（2-fold / 3-fold / 5-fold）へのマッピング
- Contact–PISA partner 集合の整合ルール実装
- モジュール専用 README.md（仕様は `cursor_input.md` / CLI docstring）
- ADR 命名ディレクトリ（`FeatureContact/`）への配置・同期
- Notebook の step パスは ATOM 時代の `compute_contact_features` のまま（CLI/`run_analysis` のみ SEQRES 対応）
- `feature_manifest.csv` は summary 列のみ（partner 列・ADR-022 列は未列挙）

---

## Outputs

生成確認済み（39 PDB）:

- `contact_features.csv`
  （列に is_missing, missing_segment_length を含む）
- `contact_features_summary.csv`
- `seqres_nodes.csv`
- `summary.txt`
- `done.flag`（DatasetPreparation が書込）
- `plots/contact_heatmap.png`
- `plots/minimum_distance_heatmap.png`
- `plots/total_contact_profile.png`
- `plots/distance_histogram.png`
- `plots/top_contact_residues.png`
- `plots/partner_chain_contribution.png`
- （3DKT/7S21/9B9I のみ）`plots/Figure_missing_overlay.png`

---

## Validation Status

- ADR-017 要求の partner 列保持を CSV で確認
- 距離帯列（n_2A … n_10A）および `normalized_n_10A` を確認
- ADR-022: ノード数・missing 数が期待値と一致（代表 3 構造＋全 39 完備）
- Contact partner 数と PISA partner 数が一致しない
  （例: 3DKT Contact B–H vs PISA B–F；Contact = 全 non-A CA chain、PISA = A 関与 interface）
- 対称軸別再分類や学習前集約の妥当性検証は未実施

関連 Result: Result-005（近傍サブユニット・局所グラフ）。Result-007（SEQRES 移行根拠）。
ADR-022 移行後比較: `ADR022_before_after_comparison.csv`（正式 Result 番号は未採番）

---

## ADR Coverage

正本: `docs/ADR/`

- ADR-016 / ADR-017（局所グラフ、相互作用はノード特徴）
- ADR-018（独立 Feature モジュール）
- ADR-022（SEQRES Node、missing 特徴量）
- ADR-025（DatasetPreparation batch）

---

## Known Issues

- Contact と PISA の partner 集合不一致（Contact ⊃ PISA の傾向）
- GrepSubunits / FeaturesDSSP mmCIF への依存
- Notebook step パスが ADR-022 未追従（CLI は追従済み）
- `feature_manifest.csv` が partner スキーマを未反映
- 8IKA / 9RY4 は CIF に Chain A の `_pdbx_poly_seq_scheme` が無く DatasetPreparation で error

---

## Next Actions

High

- Contact–PISA partner 整合ルールを ADR / 設計として固定
- GraphBuilder 結合時の partner 粒度方針を確定

Medium

- Notebook を CLI と同じ SEQRES パスへ揃える
- `feature_manifest.csv` を partner / ADR-022 列まで拡張
- モジュール README / ADR 命名同期

Low

- 対称軸分類マッピング

---

## Completion Estimate

Design: 95%

Implementation: 95%

Validation: 85%

Overall: 90%

---

### Current_State Summary

- FeatureContact は ADR-022 対応済み。gold_T1-enc 由来 39 構造で CSV/summary/plots 完備。
- partner 列保持は継続；PISA との partner 集合不一致は未解消。
- DatasetPreparation 経由の batch / done.flag 運用済み。
- Notebook の step パスのみ ATOM 時代のまま残っている。
- Current_State では Contact を Mostly Complete（SEQRES 移行済・Dataset A 規模展開済）と扱う。
