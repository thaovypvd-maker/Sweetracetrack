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
            background-color: #d2a679;
        }

        #gameCanvas { 
            position: absolute; top: 0; left: 0; 
            width: 100%; height: 100%; image-rendering: pixelated; 
            z-index: 1;
        }

        #entity-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 2; pointer-events: none;
        }

        #player {
            position: absolute;
            width: 150px; height: 150px;
            left: 25px;
            transition: top 0.1s ease-out;
            image-rendering: pixelated;
        }

        .obstacle {
            position: absolute;
            width: 80px; height: 80px;
            image-rendering: pixelated;
        }

        #ui-layer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 10; pointer-events: none;
        }

        #timer {
            position: absolute; top: 20px; right: 20px; font-size.style: 40px;
            color: #ff3399; text-shadow: 2px 2px 0 #fff; display: none;
        }

        #controls {
            position: absolute; bottom: 20px; right: 20px;
            display: flex; flex-direction: column; gap: 15px;
            pointer-events: auto;
        }
        .control-btn {
            width: 80px; height: 80px; background-color: rgba(255, 153, 204, 0.9);
            border: 4px solid #ff3399; border-radius: 50%; color: white; font-size: 36px;
            display: flex; justify-content: center; align-items: center; cursor: pointer;
           .display user-select: none; -webkit-user-select: none; box =-shadow: 0 5px 0 #cc0066 ';
        }
        .control-btn:active { transform: translateblockY(5px); box-shadow: 0 ';0 0 #cc0066; background-color: #ff66b3; }

        #overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 230, 240, 0.95);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; pointer-events: auto;
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

        #error-msg {
            position: absolute; top: 10px; left: 10px; color: red; font-size: 20px; display: none; z-index: 20;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="400" height="600"></canvas>
    
    <div id="entity-layer">
        <img id="player" src="" alt="Pudding">
    </div>

    <div id="ui-layer">
        <div id="error-msg">LỖI: Không tải được ảnh!</div>
        <div id="timer">30s</div>
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
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const overlay = document.getElementById('overlay');
    const timerDisplay = document.getElementById('timer');
    const playerElement = document.getElementById('player');
    const entityLayer = document.getElementById('entity-layer');
    const errorMsg = document.getElementById('error-msg');

    // Link ảnh
    const playerUrl = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/Pudding.png.PNG";
    const obsUrl = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/obstacle.png.PNG";

    playerElement.src = playerUrl;
    playerElement.onerror = () => { errorMsg.style.display = 'block'; errorMsg.innerText = "LỖI: Không tải được ảnh Pudding!"; };
    playerElement.onload = () => { playerElement };

    let gameState = 'START'; 
    let timeLeft = 30;
    let spawnTimer = 0;
    
    let playerSize = 150; 
    let obsSize = 80;

    // TÂM CỦA 3 LÀN ĐƯỜNG
    const laneCenters = [283, 410, 536]; 
    let currentLane = 1; 
    
    let playerY = laneCenters[currentLane] - playerSize / 2;
    playerElement.style.top = playerY + "px";

    let obstacles = [];
    let gameSpeed = 350; 

    // ==========================================
    // VẼ BACKGROUND BÁNH KEM PIXEL ART (MỚI)
    // ==========================================
    function drawBackground() {
        // 1. BẦU TRỜI & MÂY & NÚI (Giữ nguyên)
        ctx.fillStyle = '#80d4ff'; ctx.fillRect(0, 0, 400, 60);
        ctx.fillStyle = '#99ddff'; ctx.fillRect(0, 60, 400, 60);
        ctx.fillStyle = '#b3e6ff'; ctx.fillRect(0, 120, 400, 100);

        ctx.fillStyle = '#ffcce0'; ctx.fillRect(270, 50, 80, 80);
        ctx.fillStyle = '#ffb3d9'; ctx.fillRect(280, 60, 60, 60);
        ctx.fillStyle = '#ffd9ec'; ctx.fillRect(285, 65, 20, 20);
        ctx.fillStyle = '#ffcce0';
        ctx.fillRect(260, 80, 10, 20); ctx.fillRect(350, 80, 10, 20);
        ctx.fillRect(300, 40, 20, 10); ctx.fillRect(300, 130, 20, 10);

        ctx.fillStyle = '#ffd1ec';
        ctx.fillRect(30, 100, 140, 20); ctx.fillRect(50, 80, 100, 20); ctx.fillRect(70, 60, 60, 20);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(40, 90, 120, 15); ctx.fillRect(60, 70, 80, 15); ctx.fillRect(80, 55, 40, 15);
        ctx.fillStyle = '#ffd1ec';
        ctx.fillRect(280, 110, 90, 20); ctx.fillRect(300, 90, 50, 20);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(290, 100, 70, 15); ctx.fillRect(310, 85, 30, 15);

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

        // 2. VẼ ĐƯỜNG ĐUA BÁNH KEM (3 TẦNG)
        // Tầng 1: Kem Vani (Màu vàng nhạt)
        ctx.fillStyle = '#fff5e6'; 
        ctx.fillRect(0, 220, 400, 126);
        // Highlight Tầng 1
        ctx.fillStyle = '#ffffff'; 
        ctx.fillRect(0, 220, 400, 10);

        // Tầng 2: Kem Dâu (Màu hồng nhạt)
        ctx.fillStyle = '#ffe6f0'; 
        ctx.fillRect(0, 346, 400, 127);
        // Highlight Tầng 2
        ctx.fillStyle = '#fff0f5'; 
        ctx.fillRect(0, 346, 400, 10);

        // Tầng 3: Kem Socola (Màu nâu sữa)
        ctx.fillStyle = '#e6c280'; 
        ctx.fillRect(0, 473, 400, 127);
        // Highlight Tầng 3
        ctx.fillStyle = '#f2d9a6'; 
        ctx.fillRect(0, 473, 400, 10);

        // 3. VẼ SỐT CHẢY (FROSTING DRIPS) Ở CÁC VẠCH PHÂN CÁCH
        // Sốt Dâu (Vạch giữa làn 1 & 2)
        ctx.fillStyle = '#ff66b3'; // Màu sốt đậm
        ctx.fillRect(0, 340, 400, 15); // Dải sốt chính
        for (let i = 0; i < 400; i += 30) {
            ctx.fillRect(i + 5, 355, 10, 15); // Giọt sốt nhỏ xuống
            ctx.fillRect(i + 15, 355, 5, 8);   // Giọt sốt ngắn hơn
        }
        // Highlight cho sốt dâu
        ctx.fillStyle = '#ff99cc'; 
        ctx.fillRect(0, 340, 400, 4);

        // Sốt Socola (Vạch giữa làn 2 & 3)
        ctx.fillStyle = '#8c5a3c'; // Màu socola đậm
        ctx.fillRect(0, 467, 400, 15); // Dải sốt chính
        for (let i = 0; i < 400; i += 25) {
            ctx.fillRect(i + 10, 482, 12, 18); // Giọt socola dài
            ctx.fillRect(i + 2, 482, 6, 10);   // Giọt socola ngắn
        }
        // Highlight cho socola
        ctx.fillStyle = '#b3804d'; 
        ctx.fillRect(0, 467, 400, 4);

        // Viền trên cùng của đường đua (Sốt dâu)
        ctx.fillStyle = '#ff66b3'; ctx.fillRect(0, 220, 400, 6);
        ctx.fillStyle = '#ff99cc'; ctx.fillRect(0, 220, 400, 2);

        // 4. THÊM HẠT CỐM (SPRINKLES) VÀ BÁNH VỤN (CRUMBS)
        const sprinkles = [
            {x: 30, y: 250, c: '#ff3399'}, {x: 150, y: 280, c: '#33ccff'}, {x: 280, y: 240, c: '#ffff33'},
            {x: 80, y: 320, c: '#ff3399'}, {x: 220, y: 300, c: '#33ccff'}, {x: 350, y: 330, c: '#ffff33'},
            {x: 50, y: 380, c: '#ffff33'}, {x: 180, y: 400, c: '#ff3399'}, {x: 300, y: 420, c: '#33ccff'},
            {x: 120, y: 430, c: '#33ccff'}, {x: 250, y: 390, c: '#ffff33'}, {x: 370, y: 440, c: '#ff3399'},
            {x: 40, y: 500, c: '#33ccff'}, {x: 160, y: 520, c: '#ffff33'}, {x: 290, y: 510, c: '#ff3399'},
            {x: 90, y: 550, c: '#ff3399'}, {x: 210, y: 570, c: '#33ccff'}, {x: 330, y: 560, c: '#ffff33'},
            {x: 60, y: 580, c: '#ffff33'}, {x: 140, y: 480, c: '#ff3399'}, {x: 320, y: 540, c: '#33ccff'}
        ];
        
        sprinkles.forEach(s => {
            ctx.fillStyle = s.c;
            ctx.fillRect(s.x, s.y, 6, 3); // Hạt cốm hình chữ nhật
            // Thêm một chút bóng đổ cho hạt cốm
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(s.x, s.y+3, 6, 1);
        });

        // Thêm các đốm bánh vụn (màu nâu nhạt) rải rác
        ctx.fillStyle = '#d9b38c';
        ctx.fillRect(100, 260, 10, 5); ctx.fillRect(240, 310, 15, 5); ctx.fillRect(340, 280, 8, 5);
        ctx.fillRect(60, 410, 12, 5); ctx.fillRect(190, 450, 10, 5); ctx.fillRect(310, 490, 15, 5);
        ctx.fillRect(130, 540, 8, 5); ctx.fillRect(270, 580, 12, 5);
    }

    // ==========================================
    // LOGIC GAME
    // ==========================================
    function moveUp() {
        if (gameState !== 'PLAYING') return;
        if (currentLane > 0) {
            currentLane--;
            playerY = laneCenters[currentLane] - playerSize / 2;
            playerElement.style.top = playerY + "px";
        }
    }

    function moveDown() {
        if (gameState !== 'PLAYING') return;
        if (currentLane < 2) {
            currentLane++;
            playerY = laneCenters[currentLane] - playerSize / 2;
            playerElement.style.top = playerY + "px";
        }
    }

    window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') moveUp();
        if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') moveDown();
    });

    document.getElementById('btnUp').addEventListener('touchstart', (e) => { e.preventDefault(); moveUp(); });
    document.getElementById('btnUp').addEventListener('mousedown', moveUp);
    document.getElementById('btnDown').addEventListener('touchstart', (e) => { e.preventDefault(); moveDown(); });
    document.getElementById('btnDown').addEventListener('mousedown', moveDown);

    document.getElementById('startBtn').addEventListener('click', startGame);

    function startGame() {
        gameState = 'PLAYING';
        timeLeft = 30;
        currentLane = 1;
        playerY = laneCenters[currentLane] - playerSize / 2;
        playerElement.style.top = playerY + "px";
        
        obstacles.forEach(obs => obs.element.remove());
        obstacles = [];
        
        spawnTimer = 0;
        gameSpeed = 350;
        overlay.style.display = 'none';
        timerDisplay.style.display = 'block';
        playerElement.style.display = 'block';
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
        const yPos = laneCenters[laneIndex] - obsSize / 2;
        
        const obsImg = document.createElement('img');
        obsImg.src = obsUrl;
        obsImg.className = 'obstacle';
        obsImg.style.top = yPos + "px";
        obsImg.style.left = "400px";
        entityLayer.appendChild(obsImg);

        obstacles.push({
            element: obsImg,
            x: 400, 
            y: yPos,
            width: obsSize,
            height: obsSize
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

        spawnTimer -= deltaTime;
        if (spawnTimer <= 0) {
            spawnObstacle();
            spawnTimer = Math.max(0.4, 1.2 - (30 - timeLeft) * 0.02); 
        }

        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.x -= gameSpeed * deltaTime;
            obs.element.style.left = obs.x + "px";

            if (obs.x + obs.width < 0) {
                obs.element.remove();
                obstacles.splice(i, 1);
                continue;
            }

            const pRect = playerElement.getBoundingClientRect();
            const oRect = obs.element.getBoundingClientRect();
            
            const pad = 25; 
            if (
                pRect.left + pad < oRect.right - pad &&
                pRect.right - pad > oRect.left + pad &&
                pRect.top + pad < oRect.bottom - pad &&
                pRect.bottom - pad > oRect.top + pad
            ) {
                gameOver(false);
                return;
            }
        }
        gameSpeed += 5 * deltaTime;
    }

    let lastTime = Date.now();
    setInterval(() => {
        const now = Date.now();
        const deltaTime = (now - lastTime) / 1000;
        lastTime = now;
        
        if (gameState === 'PLAYING') {
            update(Math.min(deltaTime, 0.1)); 
        }
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBackground();
    }, 1000 / 60);

</script>
</body>
</html>
"""

# Nhúng game vào Streamlit
components.html(game_html, height=650)
