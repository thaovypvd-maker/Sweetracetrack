import streamlit as st
import random
import time

# 1. Cấu hình trang web
st.set_page_config(page_title="Pudding Vượt Chướng Ngại Vật", page_icon="🍮", layout="centered")

# 2. Nhúng CSS để làm giao diện đường đua màu Hồng & Nâu (Bánh bông lan)
st.markdown("""
<style>
    /* Màu nền tổng thể */
    .stApp {
        background-color: #FFF0F5; /* Màu hồng nhạt */
    }
    /* Khung đường đua */
    .race-track {
        background: linear-gradient(90deg, #D2691E 25%, #FFB6C1 25%, #FFB6C1 75%, #D2691E 75%);
        /* Tạo 3 làn đường bằng background gradient */
        background-size: 100% 100%;
        border: 5px dashed #8B4513;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    /* Từng làn đường */
    .lane {
        height: 80px;
        border-bottom: 3px solid #8B4513;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        font-size: 30px;
        position: relative;
    }
    .lane:last-child {
        border-bottom: none;
    }
    /* Nhân vật Pudding */
    .pudding {
        font-size: 50px;
        transition: all 0.5s ease;
    }
    /* Chướng ngại vật */
    .obstacle {
        font-size: 40px;
    }
    /* Nút bấm */
    .stButton>button {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        height: 60px;
        border: 3px solid #C71585;
    }
</style>
""", unsafe_allow_html=True)

# 3. Khởi tạo trạng thái game (Lưu vào bộ nhớ tạm)
if 'distance' not in st.session_state:
    st.session_state.distance = 0 # Vị trí hiện tại của Pudding (0 đến 100)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'obstacles' not in st.session_state:
    # Tạo chướng ngại vật ngẫu nhiên trên 3 làn (Cách nhau 15-25 đơn vị)
    st.session_state.obstacles = [
        {"lane": 0, "pos": 30}, {"lane": 1, "pos": 50}, {"lane": 2, "pos": 70},
        {"lane": 0, "pos": 85}, {"lane": 1, "pos": 95}
    ]
if 'current_lane' not in st.session_state:
    st.session_state.current_lane = 1 # Bắt đầu ở làn giữa

# Hàm vẽ đường đua
def draw_track():
    # Tạo 3 làn, mỗi làn có Pudding và chướng ngại vật
    track_html = '<div class="race-track">'
    for i in range(3):
        track_html += f'<div class="lane" style="justify-content: flex-start;">'
        
        # Vẽ chướng ngại vật trên làn này (nếu có)
        for obs in st.session_state.obstacles:
            if obs["lane"] == i:
                # Tính toán vị trí phần trăm
                left_pos = obs["pos"] * 0.8 # Chỉnh chút cho vừa khung
                if obs["pos"] > st.session_state.distance:
                    track_html += f'<span class="obstacle" style="position: absolute; left: {left_pos}%;">🌾</span>'
        
        # Vẽ Pudding nếu đang ở làn này
        if i == st.session_state.current_lane:
            # Tính vị trí Pudding
            pud_pos = st.session_state.distance * 0.8
            track_html += f'<span class="pudding" style="position: absolute; left: {pud_pos}%; transition: left 0.5s;">🍮</span>'
            
        track_html += '</div>'
    track_html += '</div>'
    st.markdown(track_html, unsafe_allow_html=True)

# 4. Giao diện chính
st.title("🍮 Game Pudding Vượt Chướng Ngại Vật")
st.write("Chào mừng bé đến với đường đua bánh bông lan! Hãy giúp Pudding về đích an toàn nhé.")

# Hiển thị thanh tiến độ
st.progress(st.session_state.distance / 100)
st.write(f"🏁 Quãng đường: **{st.session_state.distance}%**")

# Vẽ đường đua
draw_track()

# 5. Xử lý logic game
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Sang trái", disabled=st.session_state.game_over):
        if st.session_state.current_lane > 0:
            st.session_state.current_lane -= 1
            st.rerun()

with col2:
    if st.button("🚀 CHẠY", disabled=st.session_state.game_over):
        # Tăng khoảng cách
        st.session_state.distance += 15
        if st.session_state.distance >= 100:
            st.session_state.distance = 100
            st.success("🎉 CHÚC MỪNG! PUDDING ĐÃ VỀ ĐÍCH! 🎉")
            st.balloons()
            st.session_state.game_over = True
            st.rerun()
        
        # Kiểm tra va chạm
        for obs in st.session_state.obstacles:
            # Nếu cùng làn và khoảng cách chạm nhau (sai số 10 đơn vị)
            if obs["lane"] == st.session_state.current_lane and abs(obs["pos"] - st.session_state.distance) < 10:
                st.session_state.game_over = True
                st.error("💥 ÔI KHÔNG, VA TRÚNG RỒI! 💥")
                st.write("Đừng buồn, thử lại nha sư muội ơi!")
                st.rerun()
        st.rerun()

with col3:
    if st.button("➡️ Sang phải", disabled=st.session_state.game_over):
        if st.session_state.current_lane < 2:
            st.session_state.current_lane += 1
            st.rerun()

# Nút chơi lại
if st.session_state.game_over:
    if st.button("💖 CHƠI LẠI NÀO 💖"):
        st.session_state.distance = 0
        st.session_state.game_over = False
        st.session_state.current_lane = 1
        # Random lại chướng ngại vật
        st.session_state.obstacles = [
            {"lane": random.randint(0,2), "pos": random.randint(20,40)},
            {"lane": random.randint(0,2), "pos": random.randint(50,70)},
            {"lane": random.randint(0,2), "pos": random.randint(80,95)}
        ]
        st.rerun()
