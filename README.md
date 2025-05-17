# langgraph-re
# DeepResearch × LangManus ― 気象データ拡張プロジェクト README

## プロジェクト概要

**DeepResearch** は、オープンソースのマルチエージェント自動化フレームワーク **LangManus** を基盤に、気象データと高度な外部 API（OpenAI、Anthropic、Tavily、Weather API など）を統合し、研究者・データサイエンティスト向けにドメイン特化型のリサーチ支援を行うプロジェクトです。

* **主ターゲット**: 気象・環境・エネルギー・災害対策など、天候の影響を受ける領域で高度なインサイトを必要とする研究者・実務家。
* **アウトプット**: Markdown／PDF レポート、またはインタラクティブダッシュボード。
* **キーテーマ**: 気象トレンド解析、極端気象と需要予測、災害リスク評価、環境影響分析など。

---

## 目的

1. **気象データ統合** – OpenWeatherMap 等の API から取得したリアルタイム・予報・過去の気象データを、研究ワークフローに組み込み。
2. **LLM 活用** – OpenAI (GPT‑4 など) と Anthropic Claude を用い、データ解析・要約・報告書生成を自動化。
3. **検索拡張** – Tavily Search API で最新ニュース・論文を取得し、定量データを定性情報で補強。
4. **柔軟なアウトプット** – レポート／ダッシュボード形式で分かりやすく可視化・共有。
5. **モジュール化・拡張性** – エージェント単位で機能追加しやすい構成により、将来的なデータ源やツール追加を容易化。

---

## システムアーキテクチャ

### エージェント構成

| 役割                            | 主な責務                                      |
| ----------------------------- | ----------------------------------------- |
| **Coordinator / Planner**     | ユーザ要求を受け取り、ワークフローを計画。                     |
| **WeatherAgent**              | Weather API から気象データを取得し、前処理して共有コンテキストへ格納。 |
| **Researcher / BrowserAgent** | Tavily API で外部検索・情報取得を行い、要点抽出。            |
| **Coder / AnalysisAgent**     | Python コードを生成・実行し、統計解析・可視化を実施。            |
| **LLM (GPT‑4 / Claude)**      | 各ステップでの推論・要約・レポート文生成。                     |
| **Reporter**                  | すべての成果物を統合し、Markdown レポートまたはダッシュボードを生成。   |

### データフロー例

1. Planner がタスクを分解 → 2. WeatherAgent が指定期間の気象データを取得 → 3. Coder がデータ解析・グラフ生成 → 4. BrowserAgent が外部情報を検索 → 5. LLM が洞察を文章化 → 6. Reporter がレポート／ダッシュボードとしてまとめ、ユーザへ提示。

---

## API 統合計画

### OpenAI / Anthropic

* 高度な推論・長文生成に利用。
* LiteLLM などの統一ラッパー経由で呼び出し、モデル切替を容易に。
* コスト管理・レート制限・エラー処理を実装。

### Tavily Search API

* LLM 最適化済みのリアルタイム検索。
* 信頼度の高いソースを優先し、取得結果は引用元 URL と共に保存。
* フォールバックとして他検索エンジンも選択可。

### Weather API（OpenWeatherMap）

* 現在／予報／過去データを統一フォーマットで取得。
* 大量データ取得時は期間分割・キャッシュでレート制限を回避。
* 単位変換（K→℃ など）と欠損補完を行い、DataFrame 化。

---

## データソースと取り扱い

* **気象データ**: OpenWeatherMap など。キャッシュ保存して再利用。
* **外部テキスト**: Tavily 検索結果から取得し、LLM で要約。出典を明示。
* **ユーザ提供データ**: CSV 等でアップロード可。Weather データと日時キーで結合。
* **セキュリティ**: API キーは .env で管理。機密データは外部 LLM へ送信しないモードを用意。

---

## 出力形式

1. **Markdown / PDF レポート**

   * 見出し構造、図表・キャプション、引用付き。
   * Pandoc で PDF／DOCX 変換も可能。
2. **インタラクティブダッシュボード**

   * Streamlit または LangManus Web UI 拡張で実装。
   * 時系列ズーム、フィルタ、チャット型 Q\&A などを提供。
3. **プログラマブル API**

   * Python SDK から DataFrame や JSON を直接取得できるインターフェースを用意。

---

## 技術要件

* **言語 / ランタイム**: Python 3.12+
* **主要ライブラリ**: LangManus, LiteLLM, pandas, numpy, matplotlib/plotly, requests, streamlit (任意)
* **ハードウェア**: CPU 依存。RAM 8 GB 以上推奨。GPU 不要（LLM はクラウド実行）。
* **API キー**: OPENAI\_API\_KEY, ANTHROPIC\_API\_KEY, TAVILY\_API\_KEY, WEATHER\_API\_KEY
* **環境構築**: `uv pip install -r requirements.txt` または Docker。
* **テスト**: pytest によるユニットテスト、モック API で統合テスト。

---

## 将来拡張性

* **新データドメイン**: 金融、医療、GIS など追加エージェントで対応。
* **新 LLM / 検索エンジン**: PaLM, Cohere, Vector DB 検索などをプラグイン化。
* **ML 予測機能**: scikit‑learn やローカルモデルによる需要予測、シミュレーション機能。
* **コラボレーション**: マルチユーザ対応 UI、共有ダッシュボードリンク。
* **プラグインシステム**: 外部開発者が簡単にエージェントを追加できる構造。

---

## リスクと考慮事項

| リスク          | 対策                                        |
| ------------ | ----------------------------------------- |
| データ欠損・品質     | 取得範囲・欠測値をレポートに明示。複数ソースで検証。                |
| LLM ハルシネーション | プロンプトで「提供データのみに基づく」指示。出典明示で検証容易化。         |
| 外部 API 依存    | フォールバック経路、キャッシュ活用、コスト上限設定。                |
| 処理時間         | 並列実行・タスク統合・結果キャッシュで高速化。                   |
| セキュリティ       | API キー秘匿、コード実行サンドボックス、機密データのオフライン処理オプション。 |
| メンテナンス       | OSS ガイドライン整備、テスト継続、コミュニティ貢献促進。            |

---

## クイックスタート

```bash
# 1. リポジトリ clone
$ git clone https://github.com/your-org/deepresearch-langmanus.git
$ cd deepresearch-langmanus

# 2. 環境構築
$ uv pip install -r requirements.txt  # または Docker 利用

# 3. API キー設定
$ cp .env.example .env  # 必要なキーを入力

# 4. 実行例
$ python main.py \
    --query "過去5年間の首都圏における猛暑日と電力需要の関係を調べて" \
    --location "Tokyo,JP" \
    --output-format "report"

# 5. 結果
./outputs/YYYYMMDD_HHMM_report.md  が生成されます。
```

---

## ライセンス

MIT License

---

## コントリビュート方法

1. Issue もしくは Discussion で提案を投稿。
2. `feature/your-feature` ブランチを切り、実装後 Pull Request。
3. CI でテストが通過し、レビュー後にマージ。

お気軽にご参加ください 🎉
