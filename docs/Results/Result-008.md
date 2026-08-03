# Result-008

Date  
2026-08-03

Track  
Track B (Dry Research)

## Related ADR

- ADR-021: Edge Definition for Encapsulin-GNN

## Objective

ADR-021で定義したエッジ設計の妥当性を評価する。

特に、

```text
actual_distance
sequence_distance
ss_pair
same_ss_element
```

の有用性を検証する。

## Method

対象構造

```text
3DKT
7S21
9B9I
```

エッジ定義

```text
Cα distance < threshold
```

初期条件

```text
threshold = 8 Å
```

以下を実施した。

- Distance Histogram
- Sequence Distance Histogram
- Distance vs Sequence Distance Plot
- ss_pair解析
- same_ss_element解析
- Contact Map解析

さらに

```text
4 Å
6 Å
8 Å
10 Å
```

でエッジ数変化を比較した。

## Result

### Edge Count Validation

| PDB | 4 Å | 6 Å | 8 Å | 10 Å |
|------|------:|------:|------:|------:|
| 3DKT | 267 | 689 | 1233 | 2125 |
| 7S21 | 263 | 648 | 1209 | 2163 |
| 9B9I | 260 | 647 | 1197 | 2145 |

エッジ数はthreshold増加に対して単調増加した。

### Sequence Distance Validation

Distance vs Sequence Distance解析により、

```text
sequence_distance > 100
```

にもかかわらず

```text
actual_distance < 8 Å
```

となる残基対が多数存在した。

これは三次構造による長距離接触を反映している。

### same_ss_element Validation

3DKTでは

```text
HH
same = 260
different = 29
```

であり、

約90％が同一ヘリックス内接触であった。

一方、

```text
EE
same = 118
different = 175
```

であり、

約60％が異なるβストランド間接触であった。

### HELO Extension Validation

当初の

```text
H
E
L
```

分類に加えて、

```text
O
( T, S, P )
```

を導入した。

追加カテゴリーの出現頻度

| PDB | HO | EO | LO | OO |
|------|------:|------:|------:|------:|
| 3DKT | 75 | 121 | 122 | 112 |
| 7S21 | 76 | 67 | 191 | 112 |
| 9B9I | 73 | 91 | 153 | 129 |

Oカテゴリは無視できない頻度で出現した。

## Interpretation

```text
actual_distance
```

と

```text
sequence_distance
```

の併用により、

局所接触と長距離接触の区別が可能であることを確認した。

また、

```text
same_ss_element
```

により、

同一二次構造要素内接触と異なる要素間接触を識別できることを確認した。

さらに、

```text
T
S
P
```

を含むOカテゴリは十分な頻度を持つため、

Loopへ統合するより独立カテゴリとして保持する方が妥当であることが示唆された。

## Conclusion

ADR-021のエッジ設計は妥当である。

採用仕様を以下とする。

```text
Edge condition

Cα distance < threshold
```

```text
Edge features

actual_distance

sequence_distance

ss_pair

HH
EE
LL
HE
HL
EL
HO
EO
LO
OO

same_ss_element
```

## Next Action

High

- HELO版ss_pairを正式仕様へ反映
- MergeFeatures実装

Medium

- Dataset Aへの適用

Low

- Threshold最適化
- RBF距離展開の検討
