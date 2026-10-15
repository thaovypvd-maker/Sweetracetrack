import streamlit as st

st.set_page_config(
    page_title="Sweet Racetrack",
    page_icon="🍮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ẩn header/footer mặc định của Streamlit để giao diện giống game app thực thụ
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffd1dc; }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Mã nguồn HTML/JS cho game Canvas
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Sweet Racetrack</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #ffb6c1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Courier New', Courier, monospace;
            touch-action: manipulation;
            overflow: hidden;
        }
        #game-container {
            text-align: center;
            position: relative;
            width: 100%;
            max-width: 600px;
        }
        canvas {
            border: 4px solid #fff;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4);
            width: 100%;
            height: auto;
            background: #a0e6ff;
        }
        .controls {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        }
        .btn-control {
            background-color: #ff69b4;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 15px 35px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 0 #c71585;
            outline: none;
            transition: 0.1s;
        }
        .btn-control:active {
            transform: translateY(4px);
            box-shadow: 0 1px 0 #c71585;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="600" height="500"></canvas>
    <div class="controls">
        <button class="btn-control" id="upBtn">⬆️ LÊN</button>
        <button class="btn-control" id="downBtn">⬇️ XUỐNG</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Link ảnh từ GitHub của bạn (đã chuyển sang dạng raw)
const puddingImgUrl = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/Pudding.png.PNG";
const obstacleImgUrl = "https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/e187630e00469df1a7e0c774bd8188d1eb4b3b3b/obstacle.png.PNG";

const puddingImg = new Image();
puddingImg.src = puddingImgUrl;

const obstacleImg = new Image();
obstacleImg.src = obstacleImgUrl;

// Cấu hình làn đường (3 làn)
const lanes = [210, 310, 410]; // Tọa độ Y trung tâm của 3 làn
let currentLaneIndex = 1; // Bắt đầu ở làn giữa

let gameState = "START"; // START, PLAYING, WIN, GAMEOVER
let score = 0;
let timeLeft = 30.0;
let gameTimer;
let obstacles = [];
let obstacleTimer = 0;

const pudding = {
    x: 80,
    y: lanes[currentLaneIndex],
    width: 60,
    height: 60
};

// Điều khiển bàn phím
window.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" || e.key === "KeyW") {
        moveUp();
    } else if (e.key === "ArrowDown" || e.key === "KeyS") {
        moveDown();
    } else if (e.key === "Enter" && (gameState === "START" || gameState === "GAMEOVER" || gameState === "WIN")) {
        startGame();
    }
});

// Điều khiển nút bấm trên màn hình (Mobile & PC click)
document.getElementById("upBtn").addEventListener("click", () => {
    if (gameState === "PLAYING") moveUp();
    else startGame();
});
document.getElementById("downBtn").addEventListener("click", () => {
    if (gameState === "PLAYING") moveDown();
    else startGame();
});

canvas.addEventListener("click", () => {
    if (gameState === "START" || gameState === "GAMEOVER" || gameState === "WIN") {
        startGame();
    }
});

function moveUp() {
    if (currentLaneIndex > 0) {
        currentLaneIndex--;
        pudding.y = lanes[currentLaneIndex];
    }
}

function moveDown() {
    if (currentLaneIndex < lanes.length - 1) {
        currentLaneIndex++;
        pudding.y = lanes[currentLaneIndex];
    }
}

function startGame() {
    gameState = "PLAYING";
    score = 0;
    timeLeft = 30.0;
    obstacles = [];
    currentLaneIndex = 1;
    pudding.y = lanes[currentLaneIndex];
    
    clearInterval(gameTimer);
    gameTimer = setInterval(() => {
        if (gameState === "PLAYING") {
            timeLeft -= 0.1;
            if (timeLeft <= 0) {
                timeLeft = 0;
                gameState = "WIN";
                clearInterval(gameTimer);
            }
        }
    }, 100);
}

// Vẽ nền phong cách Pixel Art giống ảnh mẫu
function drawBackground() {
    // 1. Bầu trời chia dải màu phong cách pixel
    ctx.fillStyle = "#b5e2fa";
    ctx.fillRect(0, 0, canvas.width, 140);
    ctx.fillStyle = "#cceeff";
    ctx.fillRect(0, 140, canvas.width, 100);

    // Mặt trời pixel
    ctx.fillStyle = "#ff8fab";
    ctx.beginPath();
    ctx.arc(450, 60, 30, 0, Math.PI * 2);
    ctx.fill();
    // Tia mặt trời
    ctx.strokeStyle = "#ff8fab";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(450, 15); ctx.lineTo(450, 5);
    ctx.moveTo(450, 105); ctx.lineTo(450, 115);
    ctx.moveTo(405, 60); ctx.lineTo(395, 60);
    ctx.moveTo(495, 60); ctx.lineTo(505, 60);
    ctx.stroke();

    // Mây hồng pixel
    drawPixelCloud(100, 50);
    drawPixelCloud(300, 40);

    // Dãy núi phía sau (Núi nâu & Núi kem phủ sốp ngọt ngào)
    // Núi nâu
    ctx.fillStyle = "#b07d62";
    ctx.beginPath();
    ctx.moveTo(120, 240); ctx.lineTo(220, 160); ctx.lineTo(320, 240); ctx.fill();
    
    ctx.fillStyle = "#8c583c";
    ctx.beginPath();
    ctx.moveTo(250, 240); ctx.lineTo(350, 150); ctx.lineTo(480, 240); ctx.fill();

    // Núi kem hồng (chủ đạo)
    ctx.fillStyle = "#ffb3c6";
    ctx.beginPath();
    ctx.moveTo(-20, 240); ctx.lineTo(60, 150); ctx.lineTo(140, 240); ctx.fill();
    // Kem phủ đỉnh núi
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(40, 180, 40, 15);

    ctx.fillStyle = "#ffb3c6";
    ctx.beginPath();
    ctx.moveTo(350, 240); ctx.lineTo(450, 140); ctx.lineTo(550, 240); ctx.fill();
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(430, 175, 45, 15);

    // 2. Khu vực đường chạy màu đất cam nhạt
    ctx.fillStyle = "#e59866";
    ctx.fillRect(0, 170, canvas.width, 330);

    // Vạch kẻ các làn đường (màu hồng chấm trắng)
    ctx.strokeStyle = "#ff69b4";
    ctx.lineWidth = 6;
    ctx.setLineDash([15, 10]);
    
    ctx.beginPath();
    ctx.moveTo(0, 260); ctx.lineTo(canvas.width, 260);
    ctx.moveTo(0, 360); ctx.lineTo(canvas.width, 360);
    ctx.stroke();
    ctx.setLineDash([]); // Reset line dash
}

function drawPixelCloud(x, y) {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(x, y, 60, 20);
    ctx.fillRect(x + 10, y - 10, 40, 20);
}

// Vòng lặp chính của Game
function update() {
    if (gameState === "PLAYING") {
        // Sinh chướng ngại vật ngẫu nhiên
        obstacleTimer++;
        if (obstacleTimer > 90) { // Tần suất xuất hiện
            obstacleTimer = 0;
            let randomLane = Math.floor(Math.random() * lanes.length);
            obstacles.push({
                x: canvas.width,
                y: lanes[randomLane],
                width: 45,
                height: 45,
                speed: 5
            });
        }

        // Cập nhật vị trí chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            obstacles[i].x -= obstacles[i].speed;

            // Kiểm tra va chạm với Pudding
            let pBox = { x: pudding.x + 10, y: pudding.y + 10, width: pudding.width - 20, height: pudding.height - 20 };
            let oBox = { x: obstacles[i].x + 5, y: obstacles[i].y + 5, width: obstacles[i].width - 10, height: obstacles[i].height - 10 };

            if (pBox.x < oBox.x + oBox.width &&
                pBox.x + pBox.width > oBox.x &&
                pBox.y < oBox.y + oBox.height &&
                pBox.y + pBox.height > oBox.y) {
                gameState = "GAMEOVER";
                clearInterval(gameTimer);
            }

            // Xóa chướng ngại vật ra khỏi mảng khi ra ngoài màn hình
            if (obstacles[i].x < -50) {
                obstacles.splice(i, 1);
                score += 10; // Tăng điểm khi né thành công
            }
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Vẽ nền
    drawBackground();

    // Vẽ chướng ngại vật (Cherry)
    obstacles.forEach(obs => {
        ctx.drawImage(obstacleImg, obs.x, obs.y - 22, obs.width, obs.height);
    });

    // Vẽ nhân vật Pudding
    ctx.drawImage(puddingImg, pudding.x, pudding.y - 30, pudding.width, pudding.height);

    // Vẽ giao diện Điểm và Thời gian trên cùng (Pixel Style Header)
    ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
    ctx.fillRect(0, 0, canvas.width, 45);

    ctx.fillStyle = "#ff69b4";
    ctx.font = "bold 20px 'Courier New'";
    ctx.fillText("SCORE: " + score, 20, 30);
    ctx.fillText("TIME: " + timeLeft.toFixed(1) + "s", 420, 30);

    // Màn hình Bắt đầu
    if (gameState === "START") {
        ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ffb6c1";
        ctx.font = "bold 32px 'Courier New'";
        ctx.textAlign = "center";
        ctx.fillText("SWEET RACETRACK", canvas.width / 2, 180);

        ctx.fillStyle = "#ffffff";
        ctx.font = "18px 'Courier New'";
        ctx.fillText("Dùng nút LÊN / XUỐNG để né Cherry!", canvas.width / 2, 230);
        ctx.fillText("Sống sót trong 30 giây để về đích!", canvas.width / 2, 260);

        ctx.fillStyle = "#ff69b4";
        ctx.fillRect(canvas.width / 2 - 110, 320, 220, 50);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Courier New'";
        ctx.fillText("BẮT ĐẦU CHƠI", canvas.width / 2, 352);
        ctx.textAlign = "left"; // reset
    }

    // Màn hình Thua cuộc (Game Over)
    if (gameState === "GAMEOVER") {
        ctx.fillStyle = "rgba(100, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ff69b4";
        ctx.font = "bold 36px 'Courier New'";
        ctx.textAlign = "center";
        ctx.fillText("THUA CUỘC!", canvas.width / 2, 180);

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px 'Courier New'";
        ctx.fillText("Bạn đã dính chướng ngại vật :(", canvas.width / 2, 230);
        ctx.fillText("Điểm đạt được: " + score, canvas.width / 2, 270);

        // Nút Reset
        ctx.fillStyle = "#ff1493";
        ctx.fillRect(canvas.width / 2 - 90, 320, 180, 50);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Courier New'";
        ctx.fillText("CHƠI LẠI", canvas.width / 2, 352);
        ctx.textAlign = "left";
    }

    // Màn hình Chiến thắng (Win)
    if (gameState === "WIN") {
        ctx.fillStyle = "rgba(0, 100, 50, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00ffcc";
        ctx.font = "bold 36px 'Courier New'";
        ctx.textAlign = "center";
        ctx.fillText("CHIẾN THẮNG!", canvas.width / 2, 180);

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px 'Courier New'";
        ctx.fillText("Chúc mừng bạn đã về đích an toàn!", canvas.width / 2, 230);
        ctx.fillText("Tổng điểm: " + score, canvas.width / 2, 270);

        // Nút Chơi lại
        ctx.fillStyle = "#00bfff";
        ctx.fillRect(canvas.width / 2 - 90, 320, 180, 50);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Courier New'";
        ctx.fillText("CHƠI LẠI", canvas.width / 2, 352);
        ctx.textAlign = "left";
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

// Đợi ảnh tải xong rồi chạy game loop
let loadedImages = 0;
function checkImagesLoaded() {
    loadedImages++;
    if (loadedImages === 2) {
        loop();
    }
}

puddingImg.onload = checkImagesLoaded;
obstacleImg.onload = checkImagesLoaded;

// Dự phòng nếu ảnh đã cache sẵn
if (puddingImg.complete) checkImagesLoaded();
if (obstacleImg.complete) checkImagesLoaded();

</script>
</body>
</html>
"""

# Hiển thị game trong ứng dụng Streamlit
st.components.v1.html(game_code, height=620, scrolling=False)
