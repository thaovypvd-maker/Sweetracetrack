import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Sweet Racetrack", page_icon="🍮", layout="centered")

# CSS để ẩn các thành phần thừa của Streamlit, giúp giao diện game nổi bật hơn
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
        /* Sử dụng font VT323 hỗ trợ tiếng Việt có dấu, kiểu pixel retro */
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        body {
            margin: 0;
            padding: 0;
            background-color: #ffe6f0;
            font-family: 'VT323', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            touch-action: none;
        }

        #game-container {
            position: relative;
            width: 100%;
            max-width: 400px;
            height: 600px;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.5);
            border-radius: 15px;
            overflow: hidden;
            border: 4px solid #ff99cc;
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
            image-rendering: pixelated;
        }

        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 230, 240, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            z-index: 10;
        }

        h1 {
            color: #ff3399;
            font-size: 46px;
            text-shadow: 2px 2px 0 #fff;
            margin-bottom: 20px;
            line-height: 1.1;
        }

        p {
            color: #cc0066;
            font-size: 26px;
            margin-bottom: 30px;
            line-height: 1.3;
        }

        .btn {
            background-color: #ff66b3;
            color: white;
            border: 3px solid #cc0066;
            padding: 15px 30px;
            font-family: 'VT323', monospace;
            font-size: 30px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 5px 0 #cc0066;
            transition: all 0.1s;
            text-transform: uppercase;
        }

        .btn:active {
            transform: translateY(5px);
            box-shadow: 0 0 0 #cc0066;
        }

        #controls {
            position: absolute;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            z-index: 5;
        }

        .control-btn {
            width: 80px;
            height: 80px;
            background-color: rgba(255, 153, 204, 0.9);
            border: 4px solid #ff3399;
            border-radius: 50%;
            color: white;
            font-size: 36px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
            box-shadow: 0 5px 0 #cc0066;
        }

        .control-btn:active {
            transform: translateY(5px);
            box-shadow: 0 0 0 #cc0066;
            background-color: #ff66b3;
        }

        #timer {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 40px;
            color: #ff3399;
            text-shadow: 2px 2px 0 #fff;
            z-index: 5;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="400" height="600"></canvas>
    
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

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const overlay = document.getElementById('overlay');
    const timerDisplay = document.getElementById('timer');
    
    // Tải hình ảnh nhân vật và chướng ngại vật
    const playerImg = new Image();
    playerImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/Pudding.png.PNG";

    const obsImg = new Image();
    obsImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/obstacle.png.PNG";

    // Biến trạng thái game
    let gameState = 'START'; 
    let timeLeft = 30;
    let lastTime = 0;
    let spawnTimer = 0;
    
    // KÍCH THƯỚC ĐÃ ĐƯỢC TĂNG LÊN (Pudding to hơn hẳn Cherry)
    let playerSize = 150; 
    let obsWidth = 80;
    let obsHeight = 80;

    // Cấu hình làn đường (3 làn)
    // Tọa độ Y của TÂM 3 làn đường (đã tính toán lại cho phù hợp với background mới)
    const laneCenters = [310, 420, 530]; 
    let currentLane = 1; 
    
    let playerY = laneCenters[currentLane] - playerSize / 2 + 10; // +10 để nhân vật nằm đúng tâm làn
    let targetY = laneCenters[currentLane] - playerSize / 2 + 10;
    let playerX = 30; 

    let obstacles = [];
    let gameSpeed = 350; 

    // Hàm vẽ Background tự động theo phong cách Pixel Art
    function drawBackground() {
        // 1. Vẽ bầu trời (Màu xanh da trời pixel)
        ctx.fillStyle = '#8cd9ff'; 
        ctx.fillRect(0, 0, canvas.width, 260);

        // 2. Vẽ mặt trời (Khối vuông pixel)
        ctx.fillStyle = '#ffb3d9'; 
        ctx.fillRect(280, 60, 60, 60); // Mặt trời chính
        // Tia nắng
        ctx.fillRect(260, 80, 10, 20); ctx.fillRect(350, 80, 10, 20);
        ctx.fillRect(300, 40, 20, 10); ctx.fillRect(300, 130, 20, 10);

        // 3. Vẽ mây (Các khối vuông chồng lên nhau)
        ctx.fillStyle = '#ffd1ec'; 
        // Mây trái
        ctx.fillRect(50, 80, 100, 30);
        ctx.fillRect(70, 60, 60, 30);
        ctx.fillRect(30, 100, 140, 20);
        // Mây phải
        ctx.fillRect(280, 100, 90, 30);
        ctx.fillRect(300, 80, 50, 30);

        // 4. Vẽ núi kem (Pixel Art)
        // Núi hồng (Dâu)
        ctx.fillStyle = '#ffcce0';
        ctx.beginPath(); ctx.moveTo(-50, 260); ctx.lineTo(80, 140); ctx.lineTo(210, 260); ctx.fill();
        // Núi nâu (Socola)
        ctx.fillStyle = '#8c5a3c';
        ctx.beginPath(); ctx.moveTo(150, 260); ctx.lineTo(260, 160); ctx.lineTo(370, 260); ctx.fill();
        // Núi hồng phải
        ctx.fillStyle = '#ffcce0';
        ctx.beginPath(); ctx.moveTo(300, 260); ctx.lineTo(400, 150); ctx.lineTo(500, 260); ctx.fill();

        // 5. Vẽ mặt đường (đất) theo dạng lưới pixel
        ctx.fillStyle = '#d2a679'; 
        ctx.fillRect(0, 260, canvas.width, 340);

        // 6. Vẽ 3 làn đường (Vạch kẻ hồng dạng khối pixel)
        ctx.fillStyle = '#ff99cc';
        // Vạch phân cách làn 1 và 2 (dạng nét đứt khối)
        for (let i = 0; i < 400; i += 40) {
            ctx.fillRect(i, 365, 20, 10);
        }
        // Vạch phân cách làn 2 và 3
        for (let i = 0; i < 400; i += 40) {
            ctx.fillRect(i, 475, 20, 10);
        }
        
        // Vẽ thêm các đốm nhỏ trên đường cho sinh động (pixel art texture)
        ctx.fillStyle = '#b3804d';
        ctx.fillRect(50, 290, 15, 5); ctx.fillRect(200, 330, 10, 5);
        ctx.fillRect(350, 300, 20, 5); ctx.fillRect(100, 400, 15, 5);
        ctx.fillRect(280, 450, 10, 5); ctx.fillRect(150, 520, 20, 5);
        ctx.fillRect(300, 560, 15, 5); ctx.fillRect(50, 580, 15, 5);
    }

    // Xử lý sự kiện bàn phím (cho máy tính)
    window.addEventListener('keydown', (e) => {
        if (gameState !== 'PLAYING') return;
        if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') moveUp();
        if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') moveDown();
    });

    // Xử lý nút bấm (cho điện thoại)
    document.getElementById('btnUp').addEventListener('touchstart', (e) => { e.preventDefault(); moveUp(); });
    document.getElementById('btnUp').addEventListener('mousedown', moveUp);
    
    document.getElementById('btnDown').addEventListener('touchstart', (e) => { e.preventDefault(); moveDown(); });
    document.getElementById('btnDown').addEventListener('mousedown', moveDown);

    function moveUp() {
        if (currentLane > 0) {
            currentLane--;
            targetY = laneCenters[currentLane] - playerSize / 2 + 10;
        }
    }

    function moveDown() {
        if (currentLane < 2) {
            currentLane++;
            targetY = laneCenters[currentLane] - playerSize / 2 + 10;
        }
    }

    // Nút bắt đầu / chơi lại
    document.getElementById('startBtn').addEventListener('click', startGame);

    function startGame() {
        gameState = 'PLAYING';
        timeLeft = 30;
        currentLane = 1;
        playerY = laneCenters[currentLane] - playerSize / 2 + 10;
        targetY = laneCenters[currentLane] - playerSize / 2 + 10;
        obstacles = [];
        spawnTimer = 0;
        gameSpeed = 350;
        overlay.style.display = 'none';
        timerDisplay.style.display = 'block';
        lastTime = performance.now();
        requestAnimationFrame(gameLoop);
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
        const yPos = laneCenters[laneIndex] - obsHeight / 2 + 10;
        obstacles.push({
            x: 400, 
            y: yPos,
            width: obsWidth,
            height: obsHeight,
            lane: laneIndex
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

            // Kiểm tra va chạm (Padding được tinh chỉnh cho Pudding to hơn)
            const padding = 30; 
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

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBackground();

        if (obsImg.complete) {
            obstacles.forEach(obs => {
                ctx.drawImage(obsImg, obs.x, obs.y, obs.width, obs.height);
            });
        }

        if (playerImg.complete) {
            ctx.drawImage(playerImg, playerX, playerY, playerSize, playerSize);
        } else {
            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(playerX, playerY, playerSize, playerSize);
        }
    }

    function gameLoop(timestamp) {
        const deltaTime = (timestamp - lastTime) / 1000;
        lastTime = timestamp;
        const safeDeltaTime = Math.min(deltaTime, 0.1);

        update(safeDeltaTime);
        draw();

        if (gameState === 'PLAYING' || gameState === 'WON' || gameState === 'LOST') {
            requestAnimationFrame(gameLoop);
        }
    }

    window.onload = () => {
        draw();
    };

</script>
</body>
</html>
"""

# Nhúng game vào Streamlit
components.html(game_html, height=650)
