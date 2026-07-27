# Project Charter

## Project Name

Encapsulin-GNN

正二十面体対称粒子形成を規定する構造原理のGraph Neural Network解析

---

## Vision

正二十面体対称粒子の形成原理を理解し、
粒子形成に支配的な残基および界面特性を抽出する。

将来的には、

- ウイルス粒子形成機構の理解
- ウイルス形成阻害戦略
- ウイルス様粒子設計
- 自己集合タンパク質設計

へ展開可能な基盤技術を確立する。

---

## Scientific Question

エンカプスリン粒子形成は、

- 界面相互作用
- 殻曲率
- 局所構造歪み

など複数の物理要因によって規定されると考えられる。

これらの物理量のうち、

- 何が重要なのか
- どの組み合わせが重要なのか

を明らかにする。

---

## Scope

本研究で扱う対象

- T=1 Encapsulin
- PDB登録構造
- Myxococcus xanthus由来Encapsulin
- Thermotoga maritima由来Encapsulin

---

## Core Strategy

1. 構造データ収集
2. 物理量抽出
3. GNN解析
4. 重要残基抽出
5. Wet実験検証

---

## Expected Outputs

- 再現可能なGNN解析パイプライン
- 粒子形成に重要な残基ランキング
- 検証済み変異体データ
- 論文
- オープンな解析手法

---

## Success Criteria

最低成功ライン

- Encapsulin構造をGNNで表現可能
- 重要残基候補の抽出

成功

- AI予測とWet結果の一致

大成功

- 粒子形成の支配原理を説明可能
- 論文化
