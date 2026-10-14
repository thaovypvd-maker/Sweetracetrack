import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Đường Đua Ngọt Ngào - Sweet Racetrack", layout="centered")

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
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🍰 ĐƯỜNG ĐUA NGỌT NGÀO - SWEET RACETRACK 🍮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #780000;'>Game né chướng ngại vật bánh kem nông trại hồng cực mượt!</p>", unsafe_allow_html=True)

# Trò chơi dạng HTML trực quan chạy ngay trong khung web, bấm nút là nhân vật chạy né mượt mà
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    background-color: #fff0f3;
    text-align: center;
    font-family: 'Courier New', monospace;
    margin: 0;
    padding: 10px;
  }
  .game-container {
    background: #ffccd5;
    border: 4px dashed #ff758c;
    border-radius: 15px;
    padding: 15px;
    width: 280px;
    margin: 0 auto;
    box-shadow: 0 8px 16px rgba(255, 117, 140, 0.3);
  }
  .lane {
    background: white;
    margin: 8px 0;
    padding: 10px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    color: #582f0e;
  }
  .active-lane {
    background: #ffb3c6;
    border: 2px solid #d90429;
  }
  button {
    background-color: #ff758c;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border-radius: 15px;
    border: none;
    padding: 12px 18px;
    margin: 5px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  button:active {
    background-color: #ff4d6d;
    transform: scale(0.95);
  }
  #message {
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
    color: #d90429;
  }
</style>
</head>
<body>

<div class="game-container">
  <div id="scoreText" style="font-weight: bold; color: #582f0e; margin-bottom: 10px;">Điểm né: 0 / 10</div>
  
  <div id="lane0" class="lane">Làn 1: 🌾 Nông Trại</div>
  <div id="lane1" class="lane active-lane">Làn 2: 🍮 Pudding Kính Hồng</div>
  <div id="lane2" class="lane">Làn 3: 🌾 Nông Trại</div>

  <div id="message">Hãy bấm nút để né!</div>
</div>

<div style="margin-top: 15px;">
  <button onclick="changeLane(0)">⬅️ Trái</button>
  <button onclick="changeLane(1)">⏺️ Giữa</button>
  <button onclick="changeLane(2)">Phải ➡️</button>
</div>

<script>
let currentLane = 1;
let obsLane = 0;
let score = 0;
let isPlaying = true;

function updateView() {
  for (let i = 0; i < 3; i++) {
    let el = document.getElementById("lane" + i);
    let text = "Làn " + (i + 1) + ": 🌾 Nông Trại";
    if (i === obsLane) {
      text = "Làn " + (i + 1) + ": ⚠️ Vật Cản";
    }
    if (i === currentLane) {
      text = "Làn " + (i + 1) + ": 🍮 Pudding Kính Hồng";
    }
    el.innerHTML = text;
    
    if (i === currentLane) {
      el.className = "lane active-lane";
    } else {
      el.className = "lane";
    }
  }
  document.getElementById("scoreText").innerText = "Điểm né: " + score + " / 10";
}

function changeLane(targetLane) {
  if (!isPlaying) {
    resetGame();
    return;
  }
  
  currentLane = targetLane;
  
  // Kiểm tra va chạm ngay khi bấm
  if (currentLane === obsLane) {
    isPlaying = false;
    document.getElementById("message.innerHTML = "💥 VA TRÚNG RỒI! Bấm nút để chơi lại";
    document.getElementById("message").innerHTML = "💥 VA TRÚNG RỒI! Bấm nút chơi lại";
  } else {
    score++;
    if (score >= 10) {
      isPlaying = false;
      document.getElementById("message").innerHTML = "🎉 CHIẾN THẮNG NGỌT NGÀO! 🎉";
    } else {
      obsLane = Math.floor(Math.random() * 3);
      document.getElementById("message").innerHTML = "Đang né rất mượt!";
    }
  }
  updateView();
}

function resetGame() {
  currentLane = 1;
  obsLane = Math.floor(Math.random() * 3);
  score = 0;
  isPlaying = true;
  document.getElementById("message").innerHTML = "Hãy bấm nút để né!";
  updateView();
}

resetGame();
</script>

</body>
</html>
"""

components.html(game_html, height=480)

st.markdown("<p style='text-align: center; color: #780000; font-weight: bold;'>Bấm các nút Trái - Giữa - Phải ở bên dưới để điều khiển nhân vật Pudding nhé!</p>", unsafe_allow_html=True)
