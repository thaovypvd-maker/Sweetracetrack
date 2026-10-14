import streamlit as st
import time

st.set_page_config(page_title="Đường Đua Ngọt Ngào - Sweet Racetrack", page_kwargs={"layout": "centered"})

# CSS tùy chỉnh giao diện ngọt ngào, màu hồng và nâu bánh kem
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #d4a373 100%);
        color: #582f0e;
    }
    h1 {
        text-align: center;
        color: #d90429;
        font-family: 'Courier New', monospace;
        text-shadow: 2px 2px #ffb3c6;
    }
    .game-box {
        background-color: #fff0f3;
        border: 4px dashed #ff758c;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(255, 117, 140, 0.3);
    }
    .stButton>button {
        background-color: #ff758c;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        border: none;
        padding: 10px 24px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #ff4d6d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🍰 ĐƯỜNG ĐUA NGỌT NGÀO - SWEET RACETRACK 🍮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #780000;'>Né chướng ngại vật nông trại hồng trong 30 giây để chiến thắng nhé!</p>", unsafe_allow_html=True)

# Khởi tạo trạng thái game
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'won' not in st.session_state:
    st.session_state.won = False
if 'pudding_lane' not in st.session_state:
    st.session_state.pudding_lane = 1 # 0: Trái, 1: Giữa, 2: Phải

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if not st.session_state.game_started:
        if st.button("🚀 BẮT ĐẦU CHƠI NGAY"):
            st.session_state.game_started = True
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.won = False
            st.session_state.pudding_lane = 1
            st.rerun()
    else:
        # Mô phỏng quá trình chạy đua
        if not st.session_state.game_over and not st.session_state.won:
            time.sleep(1)
            st.session_state.score += 1
            
            # Kiểm tra chiến thắng sau 30 giây
            if st.session_state.score >= 30:
                st.session_state.won = True
            else:
                # Ngẫu nhiên xuất hiện chướng ngại vật ở một làn đường
                import random
                obs_lane = random.choice([0, 1, 2])
                if obs_lane == st.session_state.pudding_lane:
                    st.session_state.game_over = True
            st.rerun()

        # Hiển thị giao diện điều khiển làn đường cho cả máy tính & điện thoại mượt mà
        c_left, c_mid, c_right = st.columns(3)
        with c_left:
            if st.button("⬅️ Sang Trái"):
                st.session_state.pudding_lane = 0
        with c_mid:
            if st.button("⏺️ Giữa"):
                st.session_state.pudding_lane = 1
        with c_right:
            if st.button("➡️ Sang Phải"):
                st.session_state.pudding_lane = 2

        # Hiển thị đường đua nông trại bánh kem
        lanes = ["🌾 [Nông trại] ", "🌾 [Nông trại] ", "🌾 [Nông trại] "]
        lanes[st.session_state.pudding_lane] = "🍮 [Pudding Kính Hồng]"

        st.markdown(f"""
        <div class="game-box">
            <h3>⏱️ Thời gian sống sót: {st.session_state.score} / 30 giây</h3>
            <hr style="border: 2px dashed #ff758c;">
            <p style="font-size: 22px; font-weight: bold;">Làn 1: {lanes[0]}</p>
            <p style="font-size: 22px; font-weight: bold;">Làn 2: {lanes[1]}</p>
            <p style="font-size: 22px; font-weight: bold;">Làn 3: {lanes[2]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Thông báo Thắng / Thua
        if st.session_state.won:
            st.markdown("""
                <div style="background-color: #ffb3c6; padding: 15px; border-radius: 15px; text-align: center; margin-top: 15px;">
                    <h2 style="color: #9b2226;">🎉 XUẤT SẮC! CHIẾN THẮNG RỒI! 🎉</h2>
                    <p style="color: #582f0e; font-weight: bold;">Muội đã bảo vệ bánh Pudding thành công suốt 30 giây ngọt ngào!</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("💖 CHƠI LẠI NGAY 💖"):
                st.session_state.game_started = False
                st.rerun()

        elif st.session_state.game_over:
            st.markdown("""
                <div style="background-color: #ffccd5; padding: 15px; border-radius: 15px; text-align: center; margin-top: 15px;">
                    <h2 style="color: #ae2012;">💥 ÔI KHÔNG, VA TRÚNG RỒI! 💥</h2>
                    <p style="color: #582f0e; font-weight: bold;">Đừng buồn, thử lại nha sư muội ơi!</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("💖 CHƠI LẠI NÀO 💖"):
                st.session_state.game_started = False
                st.rerun()
