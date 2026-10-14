import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pudding Race", layout="centered")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; display: flex; justify-content: center; background: #FFF0F5; font-family: 'Courier New', monospace; }
    #game { position: relative; width: 100%; max-width: 500px; height: 600px; overflow: hidden; border: 8px solid #FF69B4; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .bg { position: absolute; width: 100%; height: 100%; object-fit: cover; z-index: 1; }
    #pudding { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); width: 80px; height: 80px; background: url('https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/8f2d9b66ef4db621044d300264ddbac563444553/pudding.png.jpg') no-repeat center/contain; z-index: 10; transition: bottom 0.15s; }
    .obs { position: absolute; width: 50px; height: 50px; background: url('https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/8f2d9b66ef4db621044d300264ddbac563444553/obstacle.png.JPG') no-repeat center/contain; z-index: 5; }
    #ui { position: absolute; top: 10px; width: 100%; display: flex; justify-content: space-between; padding: 0 20px; box-sizing: border-box; color: #FF69B4; font-size: 24px; font-weight: bold; text-shadow: 2px 2px 0 #FFF, -2px -2px 0 #FFF; z-index: 20; }
    .ctrl { position: absolute; bottom: 10px; width: 100%; display: flex; justify-content: center; gap: 20px; z-index: 30; }
    button { padding: 10px 20px; font-size: 20px; background: #FF69B4; color: white; border: 3px solid #C71585; border-radius: 10px; font-weight: bold; cursor: pointer; }
    #start { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 30px; padding: 20px 40px; z-index: 100; }
    .over { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: #FF0000; font-size: 40px; font-weight: bold; text-align: center; text-shadow: 2px 2px 0 #FFF; z-index: 50; display: none; }
</style>
</head>
<body>
<div id="game">
    <img src="https://raw.githubusercontent.com/thaovypvd-maker/Sweetracetrack/8f2d9b66ef4db621044d300264ddbac563444553/background.png.PNG" class="bg">
    <div id="pudding"></div>
    <div id="ui"><div>SCORE: <span id="score">0000</span></div><div>TIME: <span id="time">00:30</span></div></div>
    <div class="over" id="msg">💥 ÔI KHÔNG, VA TRÚNG RỒI! 💥</div>
    <div class="ctrl"><button id="left">⬅️ TRÁI</button><button id="right">➡️ PHẢI</button></div>
    <button id="start">🚀 BẮT ĐẦU CHẠY</button>
</div>
<script>
    const g = document.getElementById('game'), p = document.getElementById('pudding'), s = document.getElementById('score'), t = document.getElementById('time'), st = document.getElementById('start'), m = document.getElementById('msg');
    let play = false, sc = 0, time = 30, lane = 1, obs = [], loop;
    const pos = [10, 70, 130];
    
    function move(d) {
        if (!play) return;
        if (d === 'l' && lane > 0) lane--;
        if (d === 'r' && lane < 2) lane++;
        p.style.bottom = pos[lane] + 'px';
    }
    
    function spawn() {
        if (!play) return;
        const o = document.createElement('div'); o.className = 'obs';
        const r = Math.floor(Math.random() * 3);
        o.style.bottom = pos[r] + 'px'; o.style.right = '-60px'; o.dataset.lane = r;
        g.appendChild(o); obs.push(o);
    }
    
    function update() {
        if (!play) return;
        obs.forEach((o, i) => {
            let cr = parseFloat(o.style.right) + 5;
            o.style.right = cr + 'px';
            if (cr > 180 && cr < 260 && parseInt(o.dataset.lane) === lane) {
                play = false; clearInterval(loop); m.style.display = 'block'; st.innerText = 'CHƠI LẠI 💖'; st.style.display = 'block';
            }
            if (cr > 550) { o.remove(); obs.splice(i, 1); sc += 10; s.innerText = String(sc).padStart(4, '0'); }
        });
        if (Math.random() < 0.03) spawn();
        requestAnimationFrame(update);
    }
    
    function start() {
        play = true; sc = 0; time = 30; lane = 1; obs.forEach(o => o.remove()); obs = [];
        s.innerText = '0000'; t.innerText = '00:30'; m.style.display = 'none'; st.style.display = 'none'; p.style.bottom = '70px';
        const timer = setInterval(() => {
            if (!play) { clearInterval(timer); return; }
            time--; t.innerText = '00:' + String(time).padStart(2, '0');
            if (time <= 0) { play = false; clearInterval(timer); m.innerText = '🎉 CHÚC MỪNG! VỀ ĐÍCH! 🎉'; m.style.color = '#00FF00'; m.style.display = 'block'; st.innerText = 'CHƠI LẠI 💖'; st.style.display = 'block'; }
        }, 1000);
        loop = requestAnimationFrame(update);
    }
    
    st.addEventListener('click', start);
    document.getElementById('left').addEventListener('click', () => move('l'));
    document.getElementById('right').addEventListener('click', () => move('r'));
    document.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') move('l'); if (e.key === 'ArrowRight') move('r'); });
</script>
</body>
</html>
"""

components.html(game_html, height=620)
