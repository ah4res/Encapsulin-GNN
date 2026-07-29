# Result-003

Date: 2026-07-29

Track: Track B (Dry Research)

## Related ADR

- ADR-012
- ADR-013

## Objective

Icosahedral Particle Atlasから抽出したT=1およびT=3粒子について、
GNN学習データセットの妥当性を評価する。

特に、

- Encapsulinの系統的多様性
- T=1とT=3の分布
- 初期GNN学習対象の決定

を目的とした。

## Method

### Atlas Dataset

対象データ

- Gold Dataset (T=1)
- Silver Dataset (T=3)

### Analysis 1

全粒子について

- Shell protein配列抽出
- CD-HIT (95%)
- MAFFT
- FastTree

を実施し、Atlas全体の系統樹を作成した。

### Analysis 2

Encapsulinのみを抽出し、

- Gold T=1 Encapsulin
- Silver T=3 Encapsulin

について同様の解析を実施した。

## Result

### Atlas Dataset Summary

- Total structures: 646
- Total clusters after CD-HIT: 241
- T=1: 403
- T=3: 243

### Encapsulin Dataset Summary

- Encapsulin structures: 48
- T=1 Encapsulin: 40
- T=3 Encapsulin: 8
- Unique Encapsulin species: 23
- Unique Encapsulin shell proteins: 18

### Atlas-wide Phylogeny

全粒子を用いた系統樹では、

- Encapsulin
- Virus
- VLP

は明確な単一クレードを形成しなかった。

また、

- T=1
- T=3

も明確には分離しなかった。

### Encapsulin-only Phylogeny

Encapsulinのみの解析では、

- T=1 Encapsulinは複数クレードに分散した
- T=3 Encapsulinは少数かつ系統的に集中した

ことが確認された。

T=3 Encapsulinは独立サンプル数が少なく、
特定系統への偏りが認められた。

## Interpretation

本結果は、

「T=1とT=3を比較する前に、
まずT=1粒子の形成原理を理解するべきである」

ことを示唆する。

特に、

T=3 Encapsulinは構造数および系統的多様性が不足しており、

初期段階のGNN学習対象としては適さない可能性が高い。

一方、

T=1 Encapsulinは比較的多様であり、
初期GNN解析対象として十分な候補である。

また、

Virus系T=1粒子を別データセットとして扱うことで、

- HK97 fold依存特徴
- Jelly-roll fold依存特徴

と、

正二十面体粒子形成に共通な特徴

を分離して評価できる可能性が示された。

## Conclusion

初期GNN解析は以下の二本立て戦略を採用する。

### Dataset A

T=1 Encapsulin Dataset

目的

- GNNパイプライン構築
- 特徴量検討
- 重要残基探索

### Dataset B

T=1 Virus Dataset

目的

- Fold多様性評価
- 粒子形成原理探索

T=3 Encapsulinは直ちに学習対象とせず、

追加構造探索
(BLAST / DALI / MATRAS)

の候補とする。

## Next Action

- T=1 Encapsulin Dataset確定
- T=1 Virus Dataset確定
- Fold分類(HK97 / Jelly-roll / Other)付与
- 初期GNNベースライン作成
- T=3 Encapsulin候補の追加探索
