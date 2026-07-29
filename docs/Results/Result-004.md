# Result-004

Date: 2026-07-29

Track: Track C (Wet Research)

## Related ADR

- ADR-009
- ADR-012
- ADR-013

## Objective

Thermotoga maritima Encapsulinおよび
Myxococcus xanthus EncAについて、

構造解析に使用された既報コンストラクト、
発現条件および精製条件を調査し、

初期Wet実験系の構築方針を決定する。

## Method

以下のPDBおよび対応論文について調査した。

### Thermotoga maritima

- 3DKT
- 7MU1
- 7KQ5
- 7K5W

### Myxococcus xanthus

- 4PT2
- 7S20
- 8VJO

調査項目

- 発現宿主
- ベクター
- タグ位置
- 発現条件
- 精製条件
- 粒子形成評価方法

## Result

### Thermotoga maritima

既報では複数の構築体および精製法が使用されていた。

#### 3DKT

- Tag-freeと推定
- ショ糖密度勾配遠心
- MonoQ

#### 7KQ5

- Tag-free
- 硫安沈殿
- SEC

#### 7MU1

- His-tag利用
- SEC

#### 7K5W

- C-terminal His-tag
- Ni-NTA
- SEC

構造情報から、

- N末端は粒子内腔側
- C末端は粒子外表面側

を向くことを確認した。

### Myxococcus xanthus

#### 4PT2

- 天然粒子解析
- CsCl密度勾配遠心

#### 7S20

- EncAをpETDuet-1へクローニング
- N-terminal His-tag
- SQDP linker付加
- Ni-NTA
- SEC

#### 8VJO

- EncAをpETDuet-1へクローニング
- N-terminal His-tag
- Ni-NTA
- SEC

両論文とも、

N-terminal His-tag付きEncAで
粒子形成およびCryoEM構造解析に成功していた。

## Interpretation

Thermotoga maritimaについては、

Tag-free構築体でも粒子形成および構造解析が可能であり、
Tagは必須ではないことが示唆された。

また、

N末端が粒子内部を向くため、

His-tagを用いる場合は

C-terminal His-tag

の方が合理的であると判断した。

一方、

Myxococcus xanthus EncAは

複数の独立した研究で

N-terminal His-tag

が使用されており、

同条件で粒子形成が確認されている。

## Conclusion

初期実験系として以下の構築体を採用する。

### Thermotoga maritima

Construct-Tm-01

- 3DKT Chain A
- WT
- Tag-free

Construct-Tm-02

- 3DKT Chain A
- WT
- C-terminal His6

ベクター

- pET28

### Myxococcus xanthus

Construct-Mx-01

- 8VJO Chain A
- WT
- N-His
- TEV site

ベクター

- 自作 pET21 N-His-TEV

発現宿主

- BL21(DE3) CodonPlus-RILP

## Next Action

ADR-014にて、

- 採用コンストラクト
- 発現戦略
- 精製戦略
- WT評価系

を正式決定する。
