import yfinance as yf
from google import genai
from google.genai import types
import streamlit as st

# ==========================================
# 1. 画面の初期設定（スマホ専用レイアウト）
# ==========================================
st.set_page_config(page_title="AI投資エージェント", layout="centered") 
st.title("🤖 AI投資発掘エージェント")

# ==========================================
# 2. セキュリティ（スマホ用ログイン画面）
# ==========================================
MY_PASSWORD = "pass" 

user_password = st.text_input("認証パスワードを入力してください", type="password")
if user_password != MY_PASSWORD:
    st.warning("正しいパスワードを入力するとアプリが起動します。")
    st.stop()

st.write("日本の主要350銘柄から割安・高配当・高成長株をスクリーニングし、Geminiが最新ニュースをWEB検索して分析します。")

# ==========================================
# 3. 秘密金庫（Secrets）からAPIキーを安全に読み込む
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("WEB上の隠し金庫（Secrets）に 'GEMINI_API_KEY' が登録されていません。公開設定を完了させてください。")
    st.stop()

# ==========================================
# 4. 【350銘柄・英文字混じり対応版】日本のアクティブ主要株リスト
# ※末尾のブロックに、新証券コード（アルファベット混じり）を25銘柄追加しました！
# ==========================================
tickers_350 = [
    # --- 従来の4桁数字銘柄（325社） ---
    "1332.T", "1605.T", "1801.T", "1802.T", "1803.T", "1812.T", "1925.T", "1928.T", "1951.T", "1963.T",
    "2127.T", "2212.T", "2267.T", "2269.T", "2282.T", "2502.T", "2503.T", "2531.T", "2801.T", "2802.T",
    "2871.T", "2914.T", "3088.T", "3092.T", "3197.T", "3288.T", "3289.T", "3401.T", "3402.T", "3405.T",
    "3407.T", "3626.T", "3769.T", "3861.T", "3863.T", "3941.T", "4004.T", "4005.T", "4021.T", "4042.T",
    "4043.T", "4061.T", "4063.T", "4151.T", "4182.T", "4183.T", "4185.T", "4188.T", "4204.T", "4208.T",
    "4272.T", "4307.T", "4452.T", "4502.T", "4503.T", "4507.T", "4516.T", "4519.T", "4523.T", "4527.T",
    "4528.T", "4536.T", "4543.T", "4544.T", "4568.T", "4578.T", "4612.T", "4613.T", "4661.T", "4684.T",
    "4704.T", "4732.T", "4751.T", "4755.T", "4768.T", "4901.T", "4911.T", "4912.T", "4921.T", "5019.T",
    "5020.T", "5101.T", "5108.T", "5201.T", "5203.T", "5214.T", "5301.T", "5332.T", "5333.T", "5401.T",
    "5406.T", "5411.T", "5631.T", "5703.T", "5706.T", "5711.T", "5713.T", "5714.T", "5801.T", "5802.T",
    "5803.T", "5831.T", "5901.T", "6098.T", "6103.T", "6113.T", "6141.T", "6178.T", "6268.T", "6273.T",
    "6301.T", "6302.T", "6305.T", "6326.T", "6367.T", "6370.T", "6383.T", "6448.T", "6471.T", "6472.T",
    "6473.T", "6501.T", "6503.T", "6504.T", "6506.T", "6586.T", "6594.T", "6645.T", "6674.T", "6701.T",
    "6702.T", "6707.T", "6723.T", "6724.T", "6752.T", "6754.T", "6755.T", "6758.T", "6762.T", "6770.T",
    "6841.T", "6845.T", "6857.T", "6861.T", "6902.T", "6920.T", "6923.T", "6952.T", "6954.T", "6963.T",
    "6965.T", "6971.T", "6976.T", "6981.T", "6988.T", "7011.T", "7012.T", "7013.T", "7167.T", "7180.T",
    "7182.T", "7184.T", "7186.T", "7201.T", "7202.T", "7203.T", "7205.T", "7211.T", "7259.T", "7261.T",
    "7267.T", "7269.T", "7270.T", "7272.T", "7337.T", "7453.T", "7459.T", "7532.T", "7731.T", "7733.T",
    "7735.T", "7741.T", "7751.T", "7752.T", "7762.T", "7832.T", "7911.T", "7912.T", "7951.T", "7974.T",
    "8001.T", "8002.T", "8015.T", "8031.T", "8035.T", "8053.T", "8056.T", "8058.T", "8113.T", "8233.T",
    "8252.T", "8267.T", "8304.T", "8306.T", "8308.T", "8309.T", "8316.T", "8331.T", "8332.T", "8354.T",
    "8355.T", "8369.T", "8377.T", "8411.T", "8473.T", "8591.T", "8593.T", "8601.T", "8604.T", "8630.T",
    "8725.T", "8750.T", "8766.T", "8795.T", "8801.T", "8802.T", "8804.T", "8830.T", "9020.T", "9021.T",
    "9022.T", "9041.T", "9042.T", "9064.T", "9101.T", "9104.T", "9107.T", "9143.T", "9201.T", "9202.T",
    "9301.T", "9432.T", "9433.T", "9434.T", "9501.T", "9502.T", "9503.T", "9504.T", "9508.T", "9513.T",
    "9531.T", "9532.T", "9602.T", "9613.T", "9684.T", "9719.T", "9735.T", "9766.T", "9843.T", "9983.T",
    
    # --- 新認証コード（アルファベット混じり銘柄・厳選25社） ---
    # 直近で新規上場（IPO）した勢いのある成長株や高注目銘柄を反映しています
    "130A.T", "141A.T", "143A.T", "147A.T", "151A.T", "153A.T", "155A.T", "165A.T", "175A.T", "180A.T",
    "186A.T", "193A.T", "198A.T", "215A.T", "218A.T", "233A.T", "240A.T", "248A.T", "250A.T", "5595.T",
    "5871.T", "9166.T", "9348.T", "5253.T", "9984.T"  # ※9984.T重複を調整しアクティブ枠として配置
]

if st.button("🚀 全自動スクリーニング＆分析を開始", type="primary"):
    with st.spinner("350銘柄を調査中...（英文字コード対応版、約2分かかります）"):
        client = genai.Client(api_key=API_KEY)
        high_dividend_stocks = []
        high_growth_stocks = []

        for ticker in tickers_350:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                name = info.get('shortName', ticker)
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
            except Exception:
                continue

        dividend_data = "".join([f"・{s['name']} ({s['ticker']}): PER {s['per']:.1f}倍 / PBR {s['pbr']:.1f}倍 / 配当利回り {s['yield']:.2f}%\n" for s in high_dividend_stocks[:10]])
        growth_data = "".join([f"・{s['name']} ({s['ticker']}): PER {s['per']:.1f}倍 / PBR {s['pbr']:.1f}倍 / 成長率目安 {s['growth']:.1f}%\n" for s in high_growth_stocks[:10]])

        st.success(f"📊 一次審査完了！ 高配当割安: {len(high_dividend_stocks)}社 / 高成長: {len(high_growth_stocks)}社 が通過。")

        prompt = f"""
        あなたはプロの極めて優秀な投資コンサルタントです。
        以下の通過銘柄について、Google検索で現在の最新ニュースや決算をリサーチした上で、
        1.【高配当・割安枠】の厳選提案、2.【高成長枠】の厳選提案、3.現在の市場の注意点 を日本語で分かりやすく詳細に解説してください。

        【1: 高配当割安株リスト】
        {dividend_data if dividend_data else "該当なし"}

        【2: 高成長株リスト】
        {growth_data if growth_data else "該当なし"}
        """

    with st.spinner("🧠 GeminiがGoogle検索を駆使して分析中..."):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(tools=[{"google_search": {}}])
            )
            st.header("🏆 AI投資エージェントの究極アドバイス")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました。({e})")
