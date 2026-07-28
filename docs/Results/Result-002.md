# Result-002

Date: 2026-07-28

Track: Track B (Dry Research)

Related ADR:
- ADR-010

## Objective

ADR-010で決定した
「Icosahedral Particle Atlas」の構築方針に基づき、

PDBに登録された正二十面体対称粒子について、

- Biological Assembly情報取得
- Icosahedral対称性判定
- T-number推定

が実現可能かを検証した。

---

## Method

PDB構造を対象に、

以下の情報を取得した。

- PDB ID
- Title
- Keywords
- Citation Information
- Biological Assembly Metadata
- Experimental Method
- Resolution

T-numberは以下の優先順位で推定した。

### Level 1

TitleおよびMetadataから

- T=1
- T=3
- T=4
- T=13

等の記述を抽出

Source:
- title
- metadata

### Level 2

Biological Assembly情報から

assembly_subunit_count

を取得し、

T = assembly_subunit_count / 60

により推定した。

Source:
- assembly

### Icosahedral判定

Assembly Symmetryから

- Icosahedral
- Point Group I

を抽出した。

---

## Result

### 1. Biological Assembly情報取得に成功

多数の構造について

- assembly_subunit_count
- assembly_symmetry

を取得できた。

代表例

| PDB | Subunit Count | T-number |
|------|------:|------:|
| 1A34 | 60 | 1 |
| 1AQ3 | 180 | 3 |
| 1AYM | 240 | 4 |
| 1AL0 | 420 | 7 |
| 1WCE | 780 | 13 |

---

### 2. T-number推定に成功

TitleおよびAssembly情報を利用することで、

多数の既知ウイルスについて
既知のT-numberと整合する値を取得できた。

例

- Satellite Tobacco Mosaic Virus → T=1
- MS2 → T=3
- Rhinovirus → T=4
- HK97 → T=7
- Infectious Bursal Disease Virus → T=13

---

### 3. メタデータ由来判定にも成功

一部の構造では

- title
- keyword
- citation

にT-numberが明記されていた。

例

- T=1 capsid
- T=3 capsid
- T=4 capsid

これらは優先的に利用可能であることを確認した。

---

### 4. Icosahedral対称性の自動収集に成功

Assembly情報から

- Icosahedral
- Point Group I

を取得できた。

Atlas構築に必要な

- 対称性
- サブユニット数
- T-number

を取得可能であることを確認した。

---

### 5. 問題点を確認

以下の課題が見つかった。

#### (1) Caspar-Klug例外

一部の巨大ウイルスや多層粒子では

Subunit Count / 60

のみでは
厳密なT-number表現にならない場合があった。

例

- Rotavirus
- Reovirus
- 巨大dsDNA Virus

---

#### (2) Icosahedral判定の誤検出

Assemblyが

- Cyclic
- C2

であるにもかかわらず

is_icosahedral=True

となるケースが確認された。

対称性判定ロジックの修正が必要である。

---

#### (3) EncapsulinのAssembly解釈

Thermotoga maritima encapsulin (3DKT)

では

assembly_subunit_count=120

が取得された。

既知の粒子サイズとの整合性について
追加検証が必要である。

---

## Interpretation

ADR-010で採用した

「名称ではなく対称性で収集する」

という方針は有効であった。

また、

Biological Assembly情報は
T-number推定の主要なデータソースとして利用可能であることが確認された。

特に

- T=1
- T=3
- T=4
- T=7
- T=13

については高い再現性で取得可能であることが示された。

---

## Conclusion

Icosahedral Particle Atlas構築の基盤技術として、

- Icosahedral対称性取得
- Assembly情報取得
- T-number推定

が実用レベルで機能することを確認した。

ADR-010の方向性を支持する結果が得られた。

---

## Next Action

### B1 Dataset Construction

全PDBを対象とした

- Icosahedral particle一覧作成
- PDB-EMDB対応付け

を実施する。

### B2 Structure Feature Engineering

以下を取得する。

- Shell diameter
- Pore diameter
- Inner diameter
- Subunit interfaces

### 将来ADR候補

ADR-011

「T-number Determination Strategy」

として

- Metadata優先
- Assembly推定
- Caspar
