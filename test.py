import yfinance as yf
import streamlit as st
from google import genai
from google.genai import types
import pandas as pd 

# ==========================================
# 1. 画面の初期設定（スマホ専用レイアウト）
# ==========================================
st.set_page_config(page_title="AI個別株究極エージェント", layout="centered") 
st.title("🤖 AI個別株・二刀流発掘エージェント")

# ==========================================
# 2. セキュリティ（スマホ用ログイン画面）
# ==========================================
MY_PASSWORD = "pass" 

user_password = st.text_input("認証パスワードを入力してください", type="password")
if user_password != MY_PASSWORD:
    st.warning("正しいパスワードを入力するとアプリが起動します。")
    st.stop()

# ==========================================
# 3. 秘密金庫（Secrets）からAPIキーを安全に読み込む
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("WEB上の隠し金庫（Secrets）に 'GEMINI_API_KEY' が登録されていません。")
    st.stop()

# ==========================================
# 4. 画面上に「タブ（切り替え機能）」を作成
# ==========================================
tab1, tab2 = st.tabs(["📊 堅実：350社スクリーニング", "🔥 攻め：リアルタイム急増株発掘"])

# ==========================================
# 【タブ1】従来の堅実スクリーニング機能
# ==========================================
with tab1:
    st.write("### 350社機械的スクリーニング")
    st.write("事前に登録した主要350社をすべて健康診断し、割安・高配当・高成長・1000円以下株をオーディションします。")
    
    tickers_350 = [
        "1332.T", "1605.T", "1801.T", "1802.T", "1803.T", "1812.T", "1925.T", "1928.T", "1951.T", "1963.T",
        "2127.T", "2212.T", "2267.T", "2269.T", "2282.T", "2502.T", "2503.T", "2531.T", "2801.T", "2802.T",
        "2871.T", "2914.T", "3088.T", "3092.T", "3197.T", "3288.T", "3289.T", "3401.T", "3402.T", "3405.T",
        "3407.T", "3626.T", "3769.T", "3861.T", "3863.T", "3941.T", "4004.T", "4005.T", "4021.T", "4042.T",
        "4043.T", "4061.T", "4063.T", "4151.T", "4182.T", "4183.T", "4185.T", "4188.T", "4204.T", "4208.T",
        "4272.T", "4307.T", "4452.T", "4502.T", "4503.T", "4507.T", "4516.T", "4519.T", "4523.T", "4527.T",
        "4528.T", "4536.T", "4543.T", "4568.T", "4578.T", "4612.T", "4613.T", "4661.T", "4684.T", "4704.T",
        "4732.T", "4751.T", "4755.T", "4768.T", "4901.T", "4911.T", "4912.T", "4921.T", "5019.T", "5020.T",
        "5101.T", "5108.T", "5201.T", "5203.T", "5214.T", "5301.T", "5332.T", "5333.T", "5401.T", "5406.T",
        "5411.T", "5631.T", "5703.T", "5706.T", "5711.T", "5713.T", "5714.T", "5801.T", "5802.T", "5803.T",
        "5831.T", "5901.T", "6098.T", "6103.T", "6113.T", "6141.T", "6178.T", "6268.T", "6273.T", "6301.T",
        "6302.T", "6305.T", "6326.T", "6367.T", "6370.T", "6383.T", "6448.T", "6471.T", "6472.T", "6473.T",
        "6501.T", "6503.T", "6504.T", "6506.T", "6586.T", "6594.T", "6645.T", "6674.T", "6701.T", "6702.T",
        "6707.T", "6723.T", "6724.T", "6752.T", "6754.T", "6755.T", "6758.T", "6762.T", "6770.T", "6841.T",
        "6845.T", "6857.T", "6861.T", "6902.T", "6920.T", "6923.T", "6952.T", "6954.T", "6963.T", "6965.T",
        "6971.T", "6976.T", "6981.T", "6988.T", "7011.T", "7012.T", "7013.T", "7167.T", "7180.T", "7182.T",
        "7184.T", "7186.T", "7201.T", "7202.T", "7203.T", "7205.T", "7211.T", "7259.T", "7261.T", "7267.T",
        "7269.T", "7270.T", "7272.T", "7337.T", "7453.T", "7459.T", "7532.T", "7731.T", "7733.T", "7735.T",
        "7741.T", "7751.T", "7752.T", "7762.T", "7832.T", "7911.T", "7912.T", "7951.T", "7974.T", "8001.T",
        "8002.T", "8015.T", "8031.T", "8035.T", "8053.T", "8056.T", "8058.T", "8113.T", "8233.T", "8252.T",
        "8267.T", "8304.T", "8306.T", "8308.T", "8309.T", "8316.T", "8331.T", "8332.T", "8354.T", "8355.T",
        "8369.T", "8377.T", "8411.T", "8473.T", "8591.T", "8593.T", "8601.T", "8604.T", "8630.T", "8725.T",
        "8750.T", "8766.T", "8795.T", "8801.T", "8802.T", "8804.T", "8830.T", "9020.T", "9021.T", "9022.T",
        "9041.T", "9042.T", "9064.T", "9101.T", "9104.T", "9107.T", "9143.T", "9201.T", "9202.T", "9301.T",
        "9432.T", "9433.T", "9434.T", "9501.T", "9502.T", "9503.T", "9504.T", "9508.T", "9513.T", "9531.T",
        "9532.T", "9602.T", "9613.T", "9684.T", "9719.T", "9735.T", "9766.T", "9843.T", "9983.T", "9984.T",
        "130A.T", "141A.T", "143A.T", "147A.T", "151A.T", "153A.T", "155A.T", "165A.T", "175A.T", "180A.T",
        "186A.T", "193A.T", "198A.T", "215A.T", "218A.T", "233A.T", "240A.T", "248A.T", "250A.T", "5595.T",
        "5871.T", "9166.T", "9348.T", "5253.T"
    ]
    if st.button("🚀 350社スクリーニングを開始", type="primary", key="btn_scr"):
        with st.spinner("350銘柄を調査中...（約2分かかります）"):
            client = genai.Client(api_key=API_KEY)
            high_dividend_stocks = []
            high_growth_stocks = []
            under_1000_stocks = []

            for ticker in tickers_350:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    
                    # 【修正箇所】英語名(shortName)を避け、東証登録の日本語社名(longName)を取得します
                    name = info.get('longName')
                    if not name or name == ticker:
                        name = info.get('shortName', ticker)
                    
                    # 「CO.,LTD.」などの英語の不要な末尾を消してスッキリ日本語名にするトリミング
                    name = name.split(" Co")[0].split(" CO")[0].split(" Ltd")[0].split(" LTD")[0].strip()
                    
                    per = info.get('trailingPE')
                    pbr = info.get('priceToBook')
                    revenue_growth = info.get('revenueGrowth', 0)
                    earnings_growth = info.get('earningsGrowth', 0)
                    
                    df = stock.history(period="3mo")
                    if df.empty:
                        continue
                    latest_price = df['Close'].iloc[-1]
                    dividend_per_share = info.get('dividendRate', 0)
                    dividend_yield = (dividend_per_share / latest_price * 100) if (dividend_per_share and latest_price) else 0.0

                    if per is None or pbr is None or per == 'N/A' or pbr == 'N/A':
                        continue

                    if per <= 15.0 and pbr <= 1.2 and dividend_yield >= 3.5:
                        high_dividend_stocks.append({
                            "ticker": ticker, "name": name, "price": latest_price,
                            "per": per, "pbr": pbr, "yield": dividend_yield
                        })

                    if (revenue_growth and revenue_growth >= 0.20) or (earnings_growth and earnings_growth >= 0.20):
                        high_growth_stocks.append({
                            "ticker": ticker, "name": name, "price": latest_price,
                            "per": per, "pbr": pbr, "growth": max(revenue_growth or 0, earnings_growth or 0) * 100
                        })

                    if latest_price <= 1000.0 and pbr <= 1.5:
                        under_1000_stocks.append({
                            "ticker": ticker, "name": name, "price": latest_price,
                            "per": per, "pbr": pbr, "yield": dividend_yield
                        })
                except Exception:
                    continue

            # AIへのデータ受け渡し用（※ここでは価格を載せず、AI側のオーディション結果にだけ株価を入れさせます）
            dividend_data = "".join([f"・{s['name']} ({s['ticker']}): PER {s['per']:.1f}倍 / PBR {s['pbr']:.1f}倍 / 配当 {s['yield']:.2f}% / [現在株価 {s['price']:.1f}円]\n" for s in high_dividend_stocks[:10]])
            growth_data = "".join([f"・{s['name']} ({s['ticker']}): PER {s['per']:.1f}倍 / PBR {s['pbr']:.1f}倍 / 成長率 {s['growth']:.1f}% / [現在株価 {s['price']:.1f}円]\n" for s in high_growth_stocks[:10]])
            under_1000_data = "".join([f"・{s['name']} ({s['ticker']}): PER {s['per']:.1f}倍 / PBR {s['pbr']:.1f}倍 / 配当 {s['yield']:.2f}% / [現在株価 {s['price']:.1f}円]\n" for s in under_1000_stocks[:15]])

            # 【修正箇所】通過数をシンプルに示すだけの見やすい画面配置に変更
            st.success(f"📊 一次審査完了！ 高配当割安: {len(high_dividend_stocks)}社 / 高成長: {len(high_growth_stocks)}社 / 1000円以下株: {len(under_1000_stocks)}社")

            prompt = f"""
            あなたはプロの極めて優秀な投資コンサルタントです。
            プログラムによる一次スクリーニングを通過した以下の3つのリストについて、Google検索で最新ニュースや決算をリアルタイム分析した上で、日本語で詳細に解説・提案してください。
    【絶対厳守ルール：価格の表記について】
    提案・紹介する具体的な銘柄を解説する際、リスト末尾に記載されている「現在株価 〇〇円」の情報を必ず引っ張ってきて
    (例：「おすすめの銘柄は、トヨタ自動車（7203.T）[現在の株価：2,750円] です。理由は…」という風に記載してください。)
    通過しただけの他の全銘柄の一般名などは画面に出す必要はありません。最終的にあなたが出したおすすめの銘柄だけに焦点を当ててください。

    1. 【高配当・割安株】から、今最もおすすめする銘柄を 【1～2つ】 厳選とその詳細な理由（現在価格も含めること）。
    2. 【高成長株】から、今後株価の大幅な伸びが期待できる銘柄を 【1～2つ】 厳選とその詳細な理由（現在価格も含めること）。
    3. 【現在値1000円以下の注目株枠】から、少額から投資しやすく最新ニュースの材料も良い「おすすめの銘柄3選」を厳選し、それぞれの魅力と選定理由（1円単位の正確な現在価格を明記すること）。
    4. 初心者が今、市場全体に対して警戒すべきリスク。

    【システム用出力ルール】
        解説をすべて書き終えたあと、必ず最後に改行し、一番最後の行に、オーディションで選んだ銘柄のデータを以下のフォーマット「データ:[...]」の1行だけで出力してください。余計な文字（```など）や前後の説明は絶対に入れないでください。必ず1行で完結させてください。
    データ:[{{"コード":"〇〇","社名":"〇〇","株価":1234,"枠":"高配当割安"}}]

    【1: 高配当割安株リスト】
    {dividend_data if dividend_data else "該当なし"}

    【2: 高成長株リスト】
    {growth_data if growth_data else "該当なし"}

    【3: 現在値1000円以下の通過株リスト】
    {under_1000_data if under_1000_data else "該当なし"}
    """
          # 🚀【超重要】Geminiに頼らず、手元にあるデータを直接美しい表にする！
    try:
        import pandas as pd
        all_table_data = []
        
        # 1. 高配当割安株のリストからデータを綺麗に登録
        if 'high_dividend_stocks' in locals() and high_dividend_stocks:
            for item in high_dividend_stocks:
                # 辞書データから直接コード、社名、株価をスマートに取得
                code = item.get("ticker", "不明").replace(".T", "") # .T を消してすっきり
                name = item.get("name", "不明")
                price = item.get("price", 0)
                all_table_data.append({"銘柄コード": code, "正式社名": name, "リアルタイム現在値": price, "AI評価枠": "高配当割安"})
                
        # 2. 高成長株のリストからデータを綺麗に登録
        if 'high_growth_stocks' in locals() and high_growth_stocks:
            for item in high_growth_stocks:
                code = item.get("ticker", "不明").replace(".T", "")
                name = item.get("name", "不明")
                price = item.get("price", 0)
                all_table_data.append({"銘柄コード": code, "正式社名": name, "リアルタイム現在値": price, "AI評価枠": "高成長"})
                
        # 3. 1000円以下の注目株リストからデータを綺麗に登録
        if 'under_1000_stocks' in locals() and under_1000_stocks:
            for item in under_1000_stocks:
                code = item.get("ticker", "不明").replace(".T", "")
                name = item.get("name", "不明")
                price = item.get("price", 0)
                all_table_data.append({"銘柄コード": code, "正式社名": name, "リアルタイム現在値": price, "AI評価枠": "1000円以下"})

             # --- 4列の生データ表をここで一旦作成 ---
        if all_table_data:
            df_stock = pd.DataFrame(all_table_data)
            
            # --- 【重要】夕方にGeminiが復活したら、表の社名を日本語に綺麗に翻訳させる ---
            client = genai.Client(api_key=API_KEY)
            
            with st.spinner("🧠 Geminiが社名を正式な日本語に変換し、文章で分析中..."):
                try:
                    # 作成した表をGeminiにそのまま見せて、日本語化とオーディションを同時に頼む
                    table_text = df_stock.to_string(index=False)
                    final_prompt = prompt + f"\n\n以下が現在のスクリーニング通過銘柄のリストデータです。英語の社名は必ず正式な日本語社名に変換した上で解説・オーディションを行ってください。\n\n{table_text}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=final_prompt,
                        config=types.GenerateContentConfig(tools=[{"google_search": {}}])
                    )
                    
                    # 1. AIの詳しい文章解説を完全復活！
                    st.header("✨ AI投資エージェントのスクリーニング分析")
                    st.markdown(response.text)
                    
                except Exception as gemini_err:
                    # 夕方前や制限中の場合は、文章はスキップして優しい警告を出す
                    st.warning("⚠️ 現在、Geminiの無料利用枠の制限中です（文章の生成と日本語変換をスキップしました）。夕方16〜17時以降にリセットされます。")
            
            # 2. スマホでもサクサク動く美しい並び替え表を画面に出す
            st.subheader("🔍 スクリーニング通過銘柄リスト（クリックで並び替え可能）")
            st.dataframe(
                df_stock, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "銘柄コード": st.column_config.TextColumn("銘柄コード"),
                    "リアルタイム現在値": st.column_config.NumberColumn("現在値", format="¥%d")
                }
            )
    except Exception as table_err:
        pass

with tab2:
    st.write("### リアルタイムニュース・出来高発掘")
    st.write("特定のリストを持たず、AIが今この瞬間に東証で売買代金が急増している銘柄や材料株を完全自動でリサーチします。")
    
    if st.button("🚀 ネットの海から注目株の自動発掘を開始", type="primary", key="btn_trend"):
        client = genai.Client(api_key=API_KEY)
        
        with st.spinner("🔍 Geminiが東証のリアルタイム出来高や最新ニュースをネットパトロール中...（約1分）"):
            prompt_trend = """
            あなたは日本の株式相場に精通した天才投資コンサルタントです。
            Google検索を駆使して、現在の日本株市場において「直近で売買代金が急増している銘柄」や「株価の強力な材料となるニュース・決算速報が発表されたばかりの注目銘柄」をリアルタイムに自動でリサーチ・発掘してください。
            今まさに市場の裏で大口投資家が動いている生きた情報をネット上から直接掴み取り、以下の4つの構成で日本語で詳細に提案・解説してください。

            1. 【市場環境分析：今、東証で資金が集まっているセクター】
               現在、日本の株式市場でどの業種に売買代金が集まり、相場を牽引しているかの動向解説。
            2. 【全自動発掘：ニュース・売買代金急増の超注目銘柄3選】
               ネット検索で見つけた、今大きな材料ニュースが出て売買代金を伴って動いている「具体的な日本の日本語名の銘柄（会社名とコード）」を【3つ】厳選し、それぞれの株価材料と選定理由。価格データが検索で判明した場合はその現在株価も記載してください。
            3. 【お宝お手頃枠：1,000円以下で買える大注目株1選】
               上記で発掘したテーマに絡む企業の中で、さらに「現在価格が1,000円以下」で少額から検討できる魅力的な低位株を【1つ】具体的に挙げて、その理由と魅力。
            4. 【激動相場における冷徹なリスクと注意点】
               売買代金急増株ならではの急激な乱高下リスクや、初心者が飛びつく前に必ず確認すべき警戒ポイント。
            """

        with st.spinner("🧠 Geminiが最新のトレンド銘柄を執筆中..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=prompt_trend,
                    config=types.GenerateContentConfig(tools=[{"google_search": {}}])
                )
                st.header("🏆 AI投資エージェントのリアルタイムトレンド発掘")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました。({e})")
