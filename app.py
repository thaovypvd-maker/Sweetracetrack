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
            background-color: #ffe6f0; /* Nền hồng nhạt */
            font-family: 'VT323', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            touch-action: none; /* Ngăn chặn cuộn trang trên điện thoại khi chơi */
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
            image-rendering: pixelated; /* Giữ nét pixel */
        }

        /* Lớp phủ giao diện (Start, Win, Lose) */
        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 230, 240, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            z-index: 10;
        }

        h1 {
            color: #ff3399;
            font-size: 42px; /* Tăng size do font VT323 nhỏ hơn */
            text-shadow: 2px 2px 0 #fff;
            margin-bottom: 20px;
            line-height: 1.2;
        }

        p {
            color: #cc0066;
            font-size: 24px; /* Tăng size */
            margin-bottom: 30px;
            line-height: 1.4;
        }

        .btn {
            background-color: #ff66b3;
            color: white;
            border: 3px solid #cc0066;
            padding: 15px 30px;
            font-family: 'VT323', monospace;
            font-size: 28px; /* Tăng size */
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

        /* Nút điều khiển di chuyển */
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
            width: 70px;
            height: 70px;
            background-color: rgba(255, 153, 204, 0.8);
            border: 3px solid #ff3399;
            border-radius: 50%;
            color: white;
            font-size: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
            box-shadow: 0 4px 0 #cc0066;
        }

        .control-btn:active {
            transform: translateY(4px);
            box-shadow: 0 0 0 #cc0066;
            background-color: #ff66b3;
        }

        #timer {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 36px; /* Tăng size */
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
    
    // Tải hình ảnh từ GitHub (đã chuyển sang link Raw)
    const bgImg = new Image();
    bgImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/background.png.PNG";

    const playerImg = new Image();
    playerImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/Pudding.png.PNG";

    const obsImg = new Image();
    obsImg.src = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/obstacle.png.PNG";

    // Biến trạng thái game
    let gameState = 'START'; // START, PLAYING, WON, LOST
    let timeLeft = 30;
    let lastTime = 0;
    let spawnTimer = 0;
    
    // Kích thước nhân vật và chướng ngại vật (ĐÃ TĂNG KÍCH THƯỚC)
    let playerSize = 80; 
    let obsWidth = 70;
    let obsHeight = 70;

    // Cấu hình làn đường (3 làn)
    // Tọa độ Y của TÂM 3 làn đường dựa trên nền 600px
    const laneCenters = [375, 460, 550]; 
    let currentLane = 1; // Bắt đầu ở làn giữa
    
    // Tính toán tọa độ top-left (góc trên bên trái) để vẽ
    let playerY = laneCenters[currentLane] - playerSize / 2;
    let targetY = laneCenters[currentLane] - playerSize / 2;
    let playerX = 50; // Lùi vào một chút để không sát lề

    // Mảng chướng ngại vật
    let obstacles = [];
    let gameSpeed = 350; // Tốc độ di chuyển của chướng ngại vật (px/s)

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
            targetY = laneCenters[currentLane] - playerSize / 2;
        }
    }

    function moveDown() {
        if (currentLane < 2) {
            currentLane++;
            targetY = laneCenters[currentLane] - playerSize / 2;
        }
    }

    // Nút bắt đầu / chơi lại
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
        // Gán lại sự kiện cho nút mới
        document.getElementById('startBtn').addEventListener('click', startGame);
    }

    function spawnObstacle() {
        const laneIndex = Math.floor(Math.random() * 3);
        // Tính toán tọa độ top-left dựa trên tâm làn đường
        const yPos = laneCenters[laneIndex] - obsHeight / 2;
        obstacles.push({
            x: 400, // Bắt đầu từ bên phải màn hình
            y: yPos,
            width: obsWidth,
            height: obsHeight,
            lane: laneIndex
        });
    }

    function update(deltaTime) {
        if (gameState !== 'PLAYING') return;

        // Đếm ngược thời gian
        timeLeft -= deltaTime;
        if (timeLeft <= 0) {
            timeLeft = 0;
            gameOver(true);
            return;
        }
        timerDisplay.innerText = Math.ceil(timeLeft) + "s";

        // Di chuyển mượt mà nhân vật theo làn
        playerY += (targetY - playerY) * 15 * deltaTime;

        // Tạo chướng ngại vật
        spawnTimer -= deltaTime;
        if (spawnTimer <= 0) {
            spawnObstacle();
            // Tốc độ tạo chướng ngại vật nhanh dần theo thời gian
            spawnTimer = Math.max(0.4, 1.2 - (30 - timeLeft) * 0.02); 
        }

        // Cập nhật chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.x -= gameSpeed * deltaTime;

            // Xóa chướng ngại vật khi ra khỏi màn hình
            if (obs.x + obs.width < 0) {
                obstacles.splice(i, 1);
                continue;
            }

            // Kiểm tra va chạm (Collision Detection)
            // Đã điều chỉnh padding (khoảng đệm) cho hitbox vừa vặn hơn với hình to
            const padding = 15;
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
        
        // Tăng tốc độ game theo thời gian
        gameSpeed += 5 * deltaTime;
    }

    function draw() {
        // Xóa canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Vẽ nền
        if (bgImg.complete) {
            ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);
        } else {
            ctx.fillStyle = '#f4c2c2';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Vẽ chướng ngại vật
        if (obsImg.complete) {
            obstacles.forEach(obs => {
                ctx.drawImage(obsImg, obs.x, obs.y, obs.width, obs.height);
            });
        }

        // Vẽ nhân vật
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

        // Giới hạn deltaTime để tránh lag khi chuyển tab
        const safeDeltaTime = Math.min(deltaTime, 0.1);

        update(safeDeltaTime);
        draw();

        if (gameState === 'PLAYING' || gameState === 'WON' || gameState === 'LOST') {
            requestAnimationFrame(gameLoop);
        }
    }

    // Vẽ màn hình chờ ban đầu
    window.onload = () => {
        draw();
    };

</script>
</body>
</html>
"""

# Nhúng game vào Streamlit
components.html(game_html, height=650)
