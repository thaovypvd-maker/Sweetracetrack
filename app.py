import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Sweet Racetrack", page_icon="🍮", layout="centered")

# CSS để ẩn các thành phần thừa của Streamlit
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        iframe {
            border: none;
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# Mã HTML, CSS và JavaScript của Game
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Sweet Racetrack</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        body {
            margin: 0; padding: 0; background-color: #ffe6f0;
            font-family: 'VT323', monospace;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden; touch-action: none;
        }

        #game-container {
            position: relative; width: 100%; max-width: 400px; height: 600px;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.5);
            border-radius: 15px; overflow: hidden; border: 4px solid #ff99cc;
        }

        canvas { display: block; width: 100%; height: 100%; image-rendering: pixelated; }

        #overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 230, 240, 0.95);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; z-index: 10;
        }

        h1 { color: #ff3399; font-size: 46px; text-shadow: 2px 2px 0 #fff; margin-bottom: 20px; line-height: 1.1; }
        p { color: #cc0066; font-size: 26px; margin-bottom: 30px; line-height: 1.3; }
        
        .btn {
            background-color: #ff66b3; color: white; border: 3px solid #cc0066;
            padding: 15px 30px; font-family: 'VT323', monospace; font-size: 30px;
            border-radius: 8px; cursor: pointer; box-shadow: 0 5px 0 #cc0066;
            transition: all 0.1s; text-transform: uppercase;
        }
        .btn:active { transform: translateY(5px); box-shadow: 0 0 0 #cc0066; }

        #controls {
            position: absolute; bottom: 20px; right: 20px;
            display: flex; flex-direction: column; gap: 15px; z-index: 5;
        }
        .control-btn {
            width: 80px; height: 80px; background-color: rgba(255, 153, 204, 0.9);
            border: 4px solid #ff3399; border-radius: 50%; color: white; font-size: 36px;
            display: flex; justify-content: center; align-items: center; cursor: pointer;
            user-select: none; -webkit-user-select: none; box-shadow: 0 5px 0 #cc0066;
        }
        .control-btn:active { transform: translateY(5px); box-shadow: 0 0 0 #cc0066; background-color: #ff66b3; }

        #timer {
            position: absolute; top: 20px; right: 20px; font-size: 40px;
            color: #ff3399; text-shadow: 2px 2px 0 #fff; z-index: 5;
        }

        #loading-msg {
            position: absolute; bottom: 20px; left: 20px;
            font-size: 24px; color: #cc0066; z-index: 5; display: none;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="400" height="600"></canvas>
    <div id="timer">30s</div>
    <div id="loading-msg">Đang tải hình ảnh...</div>
    <div id="controls">
        <div class="control-btn" id="btnUp">▲</div>
        <div class="control-btn" id="btnDown">▼</div>
    </div>
    <div id="overlay">
        <h1>SWEET<br>RACETRACK</h1>
        <p>Dùng nút ▲ ▼ để né Cherry.<br>Sống sót 30s để chiến thắng!</p>
        <button class="btn" id="startBtn">Bắt đầu</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const overlay = document.getElementById('overlay');
    const timerDisplay = document.getElementById('timer');
    const loadingMsg = document.getElementById('loading-msg');
    
    // TẢI HÌNH ẢNH (ĐÃ XÓA crossOrigin ĐỂ KHÔNG BỊ CHẶN TRÊN ĐIỆN THOẠI)
    const playerImg = new Image();
    playerImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/Pudding.png.PNG";

    const obsImg = new Image();
    obsImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/obstacle.png.PNG";

    let isPlayerLoaded = false;
    let isObsLoaded = false;

    playerImg.onload = () => { isPlayerLoaded = true; checkLoading(); };
    obsImg.onload = () => { isObsLoaded = true; checkLoading(); };

    // Hiển thị thông báo nếu ảnh tải chậm
    setTimeout(() => {
        if (!isPlayerLoaded || !isObsLoaded) {
            loadingMsg.style.display = 'block';
        }
    }, 1000);

    function checkLoading() {
        if (isPlayerLoaded && isObsLoaded) {
            loadingMsg.style.display = 'none';
        }
    }

    // Biến trạng thái
    let gameState = 'START'; 
    let timeLeft = 30;
    let spawnTimer = 0;
    
    // Kích thước
    let playerSize = 150; 
    let obsWidth = 80;
    let obsHeight = 80;

    // TỌA ĐỘ TÂM LÀN ĐƯỜNG
    const laneCenters = [283, 410, 536]; 
    let currentLane = 1; 
    
    let playerY = laneCenters[currentLane] - playerSize / 2;
    let targetY = laneCenters[currentLane] - playerSize / 2;
    let playerX = 25; 

    let obstacles = [];
    let gameSpeed = 350; 

    // ==========================================
    // VẼ BACKGROUND PIXEL ART
    // ==========================================
    function drawBackground() {
        // Bầu trời
        ctx.fillStyle = '#80d4ff'; ctx.fillRect(0, 0, 400, 60);
        ctx.fillStyle = '#99ddff'; ctx.fillRect(0, 60, 400, 60);
        ctx.fillStyle = '#b3e6ff'; ctx.fillRect(0, 120, 400, 100);

        // Mặt trời
        ctx.fillStyle = '#ffcce0'; ctx.fillRect(270, 50, 80, 80);
        ctx.fillStyle = '#ffb3d9'; ctx.fillRect(280, 60, 60, 60);
        ctx.fillStyle = '#ffd9ec'; ctx.fillRect(285, 65, 20, 20);
        ctx.fillStyle = '#ffcce0';
        ctx.fillRect(260, 80, 10, 20); ctx.fillRect(350, 80, 10, 20);
        ctx.fillRect(300, 40, 20, 10); ctx.fillRect(300, 130, 20, 10);

        // Mây
        ctx.fillStyle = '#ffd1ec';
        ctx.fillRect(30, 100, 140, 20); ctx.fillRect(50, 80, 100, 20); ctx.fillRect(70, 60, 60, 20);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(40, 90, 120, 15); ctx.fillRect(60, 70, 80, 15); ctx.fillRect(80, 55, 40, 15);
        ctx.fillStyle = '#ffd1ec';
        ctx.fillRect(280, 110, 90, 20); ctx.fillRect(300, 90, 50, 20);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(290, 100, 70, 15); ctx.fillRect(310, 85, 30, 15);

        // Núi
        ctx.fillStyle = '#f4c2c2';
        ctx.beginPath(); ctx.moveTo(-50, 220); ctx.lineTo(80, 100); ctx.lineTo(210, 220); ctx.fill();
        ctx.fillStyle = '#ffd9d9';
        ctx.beginPath(); ctx.moveTo(80, 100); ctx.lineTo(130, 220); ctx.lineTo(210, 220); ctx.fill();
        ctx.fillStyle = '#6b4226';
        ctx.beginPath(); ctx.moveTo(150, 220); ctx.lineTo(260, 130); ctx.lineTo(370, 220); ctx.fill();
        ctx.fillStyle = '#8c5a3c';
        ctx.beginPath(); ctx.moveTo(260, 130); ctx.lineTo(310, 220); ctx.lineTo(370, 220); ctx.fill();
        ctx.fillStyle = '#f4c2c2';
        ctx.beginPath(); ctx.moveTo(300, 220); ctx.lineTo(400, 110); ctx.lineTo(500, 220); ctx.fill();

        // Mặt đường
        ctx.fillStyle = '#d2a679'; 
        ctx.fillRect(0, 220, 400, 380);

        // Texture đường
        ctx.fillStyle = '#c1956a';
        ctx.fillRect(20, 250, 15, 5); ctx.fillRect(180, 300, 20, 5); ctx.fillRect(320, 270, 10, 5);
        ctx.fillRect(80, 400, 25, 5); ctx.fillRect(250, 480, 15, 5); ctx.fillRect(150, 550, 20, 5);
        ctx.fillStyle = '#e0b88c';
        ctx.fillRect(50, 280, 10, 5); ctx.fillRect(220, 330, 15, 5); ctx.fillRect(350, 380, 20, 5);
        ctx.fillRect(120, 450, 10, 5); ctx.fillRect(300, 520, 15, 5); ctx.fillRect(70, 580, 25, 5);

        // Vạch kẻ đường
        for (let i = 0; i < 400; i += 40) {
            ctx.fillStyle = '#cc0066'; ctx.fillRect(i, 348, 20, 8);
            ctx.fillStyle = '#ff99cc'; ctx.fillRect(i, 346, 20, 8);
            ctx.fillStyle = '#ffd1ec'; ctx.fillRect(i, 346, 20, 2);
        }
        for (let i = 0; i < 400; i += 40) {
            ctx.fillStyle = '#cc0066'; ctx.fillRect(i, 475, 20, 8);
            ctx.fillStyle = '#ff99cc'; ctx.fillRect(i, 473, 20, 8);
            ctx.fillStyle = '#ffd1ec'; ctx.fillRect(i, 473, 20, 2);
        }
        ctx.fillStyle = '#cc0066'; ctx.fillRect(0, 221, 400, 6);
        ctx.fillStyle = '#ff99cc'; ctx.fillRect(0, 220, 400, 6);
        ctx.fillStyle = '#ffd1ec'; ctx.fillRect(0, 220, 400, 2);
    }

    // Xử lý sự kiện
    window.addEventListener('keydown', (e) => {
        if (gameState !== 'PLAYING') return;
        if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') moveUp();
        if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') moveDown();
    });

    document.getElementById('btnUp').addEventListener('touchstart', (e) => { e.preventDefault(); moveUp(); });
    document.getElementById('btnUp').addEventListener('mousedown', moveUp);
    document.getElementById('btnDown').addEventListener('touchstart', (e) => { e.preventDefault(); moveDown(); });
    document.getElementById('btnDown').addEventListener('mousedown', moveDown);

    function moveUp() {
        if (currentLane > 0) {
            currentLane--;
            targetY = laneCenters[currentLane] - playerSize / 2;
        }
    }

    function moveDown() {
        if (currentLane < 2) {
            currentLane++;
            targetY = laneCenters[currentLane] - playerSize / 2;
        }
    }

    document.getElementById('startBtn').addEventListener('click', startGame);

    function startGame() {
        gameState = 'PLAYING';
        timeLeft = 30;
        currentLane = 1;
        playerY = laneCenters[currentLane] - playerSize / 2;
        targetY = laneCenters[currentLane] - playerSize / 2;
        obstacles = [];
        spawnTimer = 0;
        gameSpeed = 350;
        overlay.style.display = 'none';
        timerDisplay.style.display = 'block';
    }

    function gameOver(isWin) {
        gameState = isWin ? 'WON' : 'LOST';
        timerDisplay.style.display = 'none';
        overlay.style.display = 'flex';
        
        if (isWin) {
            overlay.innerHTML = `
                <h1 style="color: #ffcc00;">CHIẾN THẮNG!</h1>
                <p style="color: #ff3399;">Bạn đã về đích an toàn!<br>Pudding rất vui!</p>
                <button class="btn" id="startBtn">Chơi lại</button>
            `;
        } else {
            overlay.innerHTML = `
                <h1 style="color: #ff3333;">THUA CUỘC!</h1>
                <p style="color: #ff3399;">Pudding đã dính chướng ngại vật!<br>Thử lại nhé!</p>
                <button class="btn" id="startBtn">Thử lại</button>
            `;
        }
        document.getElementById('startBtn').addEventListener('click', startGame);
    }

    function spawnObstacle() {
        const laneIndex = Math.floor(Math.random() * 3);
        const yPos = laneCenters[laneIndex] - obsHeight / 2;
        obstacles.push({
            x: 400, y: yPos, width: obsWidth, height: obsHeight, lane: laneIndex
        });
    }

    function update(deltaTime) {
        if (gameState !== 'PLAYING') return;

        timeLeft -= deltaTime;
        if (timeLeft <= 0) {
            timeLeft = 0;
            gameOver(true);
            return;
        }
        timerDisplay.innerText = Math.ceil(timeLeft) + "s";

        playerY += (targetY - playerY) * 15 * deltaTime;

        spawnTimer -= deltaTime;
        if (spawnTimer <= 0) {
            spawnObstacle();
            spawnTimer = Math.max(0.4, 1.2 - (30 - timeLeft) * 0.02); 
        }

        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.x -= gameSpeed * deltaTime;

            if (obs.x + obs.width < 0) {
                obstacles.splice(i, 1);
                continue;
            }

            const padding = 25; 
            if (
                playerX + padding < obs.x + obs.width - padding &&
                playerX + playerSize - padding > obs.x + padding &&
                playerY + padding < obs.y + obs.height - padding &&
                playerY + playerSize - padding > obs.y + padding
            ) {
                gameOver(false);
                return;
            }
        }
        gameSpeed += 5 * deltaTime;
    }

    // Hàm vẽ chính (Luôn chạy 60 lần/giây)
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBackground();

        // Vẽ Cherry (Nếu ảnh đã tải xong)
        if (isObsLoaded) {
            obstacles.forEach(obs => {
                ctx.drawImage(obsImg, obs.x, obs.y, obs.width, obs.height);
            });
        } else {
            // Fallback nếu ảnh chưa tải kịp
            ctx.fillStyle = '#ff4d4d';
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
            });
        }

        // Vẽ Pudding (Nếu ảnh đã tải xong)
        if (isPlayerLoaded) {
            ctx.drawImage(playerImg, playerX, playerY, playerSize, playerSize);
        } else {
            // Fallback nếu ảnh chưa tải kịp
            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(playerX, playerY, playerSize, playerSize);
        }
    }

    // VÒNG LẶP GAME (Sử dụng setInterval để đảm bảo không bao giờ bị đứng)
    let lastTime = Date.now();
    setInterval(() => {
        const now = Date.now();
        const deltaTime = (now - lastTime) / 1000;
        lastTime = now;
        
        // Cập nhật logic game nếu đang chơi
        if (gameState === 'PLAYING') {
            update(Math.min(deltaTime, 0.1)); // Giới hạn deltaTime tránh lag
        }
        
        // Luôn luôn vẽ lại màn hình
        draw();
    }, 1000 / 60); // 60 FPS

</script>
</body>
</html>
"""

# Nhúng game vào Streamlit
components.html(game_html, height=650)
