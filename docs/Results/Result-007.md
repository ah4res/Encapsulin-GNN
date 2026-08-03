# Result-007

Date  
2026-08-03

Track  
Track B (Dry Research)

## Related ADR

- ADR-019: DSSPとPISAを異なる物理量として扱う
- ADR-022: Missing Residue Handling Strategy

## Objective

FeaturesDSSPおよび特徴量抽出パイプラインにおいて、missing residue（non-model region）がどのように扱われているかを調査する。

## Method

以下の3構造を対象とした。

```text
3DKT
7S21
9B9I
```

各構造について、

```text
SEQRES residues
ATOM residues
DSSP residues
FeaturesDSSP rows
```

を比較した。

さらにFeaturesDSSPのソースコードを調査し、

```text
SEQRES参照の有無
missing residue保持の有無
```

を確認した。

## Result

### Residue Count Comparison

| PDB | SEQRES | ATOM | DSSP | FeaturesDSSP | Missing |
|------|------:|------:|------:|------:|------:|
| 3DKT | 265 | 264 | 264 | 264 | 1 |
| 7S21 | 301 | 265 | 265 | 265 | 36 |
| 9B9I | 281 | 262 | 262 | 262 | 19 |

以下を確認した。

```text
ATOM residues
=
DSSP residues
=
FeaturesDSSP rows
```

であった。

また、

```text
SEQRES > ATOM
```

であり、missing residueが存在することを確認した。

7S21では

```text
N-terminal missing region
1–15

Internal missing region
74–85

C-terminal missing region
293–301
```

を確認した。

## Interpretation

現在のFeaturesDSSPおよび特徴量抽出パイプラインは、

```text
Node = ATOM residue
```

を暗黙的に採用していた。

その結果、

```text
missing residue
```

はDSSP出力から消失し、

特徴量テーブルにも存在していなかった。

特に7S21では約12％の残基が消失しており、無視できない規模であった。

missing residueは単なる欠測ではなく、

```text
高い柔軟性
未観測ループ
未観測ドメイン
```

を反映する生物学的情報である可能性がある。

## Conclusion

特徴量抽出パイプラインは

```text
SEQRESベース
```

ではなく

```text
ATOMベース
```

で実装されていることを確認した。

この結果を受け、

```text
Node = SEQRES residue
```

へ変更するADR-022を策定した。

## Next Action

High

- ADR-022実装
- SEQRESベースのNode定義導入
- missing residue特徴量追加

Medium

- FeatureDSSP改修
- FeatureContact改修
- FeaturePISA改修

Low

- AlphaFold由来情報の活用可能性検討
