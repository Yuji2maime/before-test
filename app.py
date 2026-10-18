import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="思考・表現力セッション（事前用）", layout="wide")

# ==========================================
# 🔑 管理者設定
# ==========================================
ADMIN_PASSWORD = "19700124"  # 横山様用パスワード（他ユーザー展開時はここを変更）

# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state.page = "candidate"  # "candidate" or "admin"
if "submitted_data" not in st.session_state:
    st.session_state.submitted_data = []
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# --- 1. 応募者用画面（事前回答用）---
if st.session_state.page == "candidate":
    st.title("思考・表現力セッション（事前回答）")
    st.write(
        "面接をより有意義でお互いの理解を深めるお時間にするため、事前に以下のテーマについてご回答をお願いしております。"
        "能力の優劣を評価するものではありませんので、ご安心してお答えください。"
    )

    st.markdown("---")

    # 氏名入力
    candidate_name = st.text_input("お名前（氏名）を入力してください", placeholder="例：山田 太郎")

    # 事前テーマの表示
    st.subheader("【事前課題テーマ】")
    st.info(
        "「これまでのご経験の中で、不確実性の高い課題や困難な状況に直面した際、"
        "あなたはどのような思考プロセスで状況を整理し、周囲と協調しながら推進されましたか？"
        "具体的なスタンスや判断基準を教えてください。」"
    )

    # 記述エリア
    text_input = st.text_area(
        "ご自身のスタンスや考え方を自由にご記述ください（文字数制限なし）",
        height=350,
        placeholder="ここに思考プロセスや具体的なエピソードを入力してください..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("回答を提出する", type="primary"):
            if candidate_name.strip() and text_input.strip():
                st.session_state.submitted_data.append({
                    "name": candidate_name,
                    "text": text_input,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "types": [],
                    "sub_functions": [],
                    "notes": ""
                })
                st.success("ご回答ありがとうございました。送信が完了いたしました。画面を閉じていただいて構いません。")
                st.balloons()
            elif not candidate_name.strip():
                st.warning("お名前（氏名）を入力してください。")
            else:
                st.warning("記述欄に回答を入力してください。")

    with col2:
        if st.button("採用担当者用画面へ"):
            st.session_state.page = "admin"
            st.rerun()

# --- 2. 採用側（管理・評価ダッシュボード）画面 ---
elif st.session_state.page == "admin":
    st.title("【事前回答】採用担当者用 管理・評価ダッシュボード")

    if st.button("← 応募者用画面に戻る"):
        st.session_state.page = "candidate"
        st.rerun()

    st.markdown("---")

    # パスワード認証チェック
    if not st.session_state.admin_authenticated:
        st.subheader("🔒 管理者認証")
        pwd_input = st.text_input("管理者パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("認証に成功しました。")
                st.rerun()
            else:
                st.error("パスワードが正しくありません。")
    else:
        # 認証成功後の管理画面コンテンツ
        if not st.session_state.submitted_data:
            st.info("現在、提出された事前回答データはありません。")
        else:
            for i, data in enumerate(st.session_state.submitted_data):
                candidate_label = data.get('name', f"応募者 #{i+1}")
                with st.expander(f"提出データ: {candidate_label} 様（提出日時: {data['timestamp']}）", expanded=True):
                    st.subheader(f"【応募者氏名】 {candidate_label}")
                    st.subheader("【事前回答内容】")
                    st.write(data["text"])

                    st.markdown("---")
                    st.subheader("【認知特性・思考傾向分析】")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        selected_types = st.multiselect(
                            "主機能・認知タイプ（該当するものすべて）",
                            ["Te型（効率・構造化）", "Ti型（論理・体系化）", "Fe型（調和・関係性）", "Fi型（価値観・内省）", "Se型（現実・実行）", "Ni型（直観・本質）"],
                            default=data["types"],
                            key=f"types_{i}"
                        )
                    with col_b:
                        selected_subs = st.multiselect(
                            "補助機能（複数認定）",
                            ["補助Te", "補助Ti", "補助Fe", "補助Fi", "補助Se", "補助Ne", "補助Si", "補助Ni"],
                            default=data["sub_functions"],
                            key=f"subs_{i}"
                        )

                    notes = st.text_area("採用・面接評価メモ（思考の癖、リスク、面接時確認事項など）", value=data["notes"], key=f"notes_{i}")

                    if st.button("評価・メモを保存する", key=f"save_{i}"):
                        st.session_state.submitted_data[i]["types"] = selected_types
                        st.session_state.submitted_data[i]["sub_functions"] = selected_subs
                        st.session_state.submitted_data[i]["notes"] = notes
                        st.success(f"{candidate_label} 様の評価メモを保存しました。")

        # ==========================================
        # 📜 管理画面フッター（免責・管理責任注記）
        # ==========================================
        st.markdown("---")
        st.caption(
            "※本システムの分析結果は選考補助用の参考情報です。"
            "採用判断（合否・配属）および出力・印刷データの管理責任はすべて採用企業（採用担当者様）に帰属します。"
        )
