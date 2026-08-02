Date
2026-07-30
Track
Track B
Related ADR
ADR-015
Objective
Encapsulin-GNN入力グラフの定義方法を決定する。
Method
3DKT Biological AssemblyからReference Chain A近傍サブユニットを抽出した。
近傍サブユニットを用いた局所グラフ構築方法について検討した。
Result
以下が確認された。

Whole ParticleはNCS対称性により高い冗長性を持つ
近傍サブユニット抽出は可能
PISA計算時に局所PDBではASA誤差が発生する可能性がある
A-B接触をエッジとして保持するより、Chain A残基の特徴量として表現する方が自然である

Interpretation
初期モデルでは、

Chain A全残基をノード
A内部接触をエッジ
サブユニット間接触を特徴量

として扱うことが妥当と判断された。
Conclusion
局所グラフ方式を試験採用する。
Next Action

接触残基数計算実装
距離帯別接触数計算実装
PISA特徴量取得実装
