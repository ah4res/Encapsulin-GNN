# Result-000

Date

2026-07-27

Track

A: Infrastructure

Related ADR

None

Objective

Encapsulin-GNNプロジェクト開始に先立ち、
AI解析およびWet実験を支える研究基盤を整備する。

Method

研究計算環境、データ管理環境、
AI支援開発環境について検討し、
ネットワーク・計算機・開発環境の導入および試験運用を実施した。

Result

## Network Infrastructure

10GbE Hub を導入し以下の機器を統合した。

### 1. MacBook Pro 14-inch

導入時期

2026年4月

用途

- 主作業環境
- Copilot
- Cursor
- GitHub管理

---

### 2. MacBook Pro 13-inch

導入時期

2022年

用途

- 補助端末
- 外出先運用

---

### 3. old-HPC

構成

- Ubuntu
- CPU 24 core
- Memory 128 GB
- GPU性能は限定的

用途

- GNN開発初期の試験環境
- New-HPC導入までの暫定環境
- X線結晶構造解析関連の既存ソフト資産運用

---

### 4. current-HPC

構成

- 高性能CPU
- 高性能GPU ×2
- Memory 384 GB

用途

- CryoEM解析専用

備考

GNN用途には利用しない。

---

### 5. new-HPC（計画中）

構成案

- GPU ×2
- Memory 128 GB

用途

- GNN解析（主用途）
- CryoEM解析
- X線結晶解析
- Nanoporeシーケンス解析

備考

現在選定・導入準備中。

---

### 6. Mac Studio

構成

- SSD 2TB

用途

- File Server
- Backup Storage
- Wetデータ蓄積
- Dryデータ保管

役割

研究室内のデータ集約ハブ

---

## Software Infrastructure

以下のサービス利用を開始した。

### GitHub

用途

- Single Source of Truth

状態

試験運用中

---

### Cursor Pro

用途

- AI支援開発
- Repository解析
- Current_State生成

状態

試験運用中

---

### Google Colab

プラン

Free

将来計画

Google Colab Pro+

用途

- GNN開発
- プロトタイピング

状態

試験運用中

---

## Initial AI Experiment

Google Colab上で
初回GNN解析を実施した。

構造表現

Node

- アミノ酸残基

Node Feature

- アミノ酸種類

Edge

- Cα距離 10Å 未満

結果

GNN学習パイプラインが動作することを確認した。

Interpretation

Infrastructure Track は概ね稼働可能な状態に到達した。

研究基盤は

- ネットワーク
- 計算環境
- GitHub運用
- AI支援開発環境

まで整備された。

また、GNNプロトタイプの実行成功により
Dry Research開始可能な状態となった。

Conclusion

Research OS導入前段階の基盤整備は完了した。

今後は

- Research OS正式運用開始
- Dataset Construction
- Graph Representation Design

へ移行する。

Next Action

- Project_Charter正式版作成
- Current_State初版作成
- ADR運用開始
- Dataset Construction開始
- new-HPC仕様確定
