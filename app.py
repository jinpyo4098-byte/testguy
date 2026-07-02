import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gravity Arrow - Dynamic Planet Edition", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding: 0; }
    iframe { display: block; width: 100vw; height: 95vh; border: none; }
    body { margin: 0; background-color: #050608; }
    </style>
    """,
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow - Dynamic Planet</title>
    <style>
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
            background-color: #050608; color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none; display: flex; align-items: center; justify-content: center;
        }
        #game-wrapper {
            position: relative; width: 1200px; height: 675px;
            background-color: #000; box-shadow: 0 0 35px rgba(0,0,0,0.9);
            overflow: hidden; border-radius: 12px;
        }
        #game-canvas {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: transparent; cursor: grab; z-index: 1;
        }
        #game-canvas:active { cursor: grabbing; }
        .screen-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: rgba(5, 6, 8, 0.92); z-index: 10;
        }
        .hidden { display: none !important; }
        .result-title { font-size: 3.2rem; color: #ffcc00; text-shadow: 0 0 15px #ffcc00; margin-bottom: 15px; }
        .score-report { font-size: 1.6rem; margin-bottom: 35px; text-align: center; line-height: 1.6; }
        .ui-panel {
            position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
            display: flex; flex-direction: column; align-items: center; width: 70%; max-width: 600px;
            background: rgba(0, 0, 0, 0.55); padding: 12px 25px; border-radius: 20px;
            box-sizing: border-box; backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.15); z-index: 5;
        }
        .stats { font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px; width: 100%; text-align: center; }
        .progress-container { width: 100%; height: 12px; background-color: rgba(255, 255, 255, 0.2); border-radius: 6px; overflow: hidden; }
        .progress-bar { height: 100%; width: 100%; background: linear-gradient(90deg, #0066ff, #00d2ff); box-shadow: 0 0 10px #00d2ff; transition: width 0.1s linear; }
        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%); border: none; color: white;
            padding: 14px 38px; font-size: 1.3rem; font-weight: bold; border-radius: 30px; cursor: pointer; transition: all 0.2s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 132, 255, 0.6); }
        .main-planet-selector { display: flex; gap: 20px; align-items: center; margin-bottom: 35px; background: rgba(255, 255, 255, 0.05); padding: 20px 35px; border-radius: 40px; }
        .planet-btn-wrapper { display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer; }
        .planet-canvas { width: 65px; height: 65px; border-radius: 50%; border: 3px solid transparent; transition: all 0.25s ease; box-sizing: border-box; }
        .planet-btn-wrapper.active .planet-canvas { border-color: #ffffff; box-shadow: 0 0 20px rgba(255, 255, 255, 0.6); }
        .planet-label { font-size: 0.85rem; font-weight: bold; color: #a0aec0; }
        .planet-btn-wrapper.active .planet-label { color: #fff; }
        #combo-wrapper { position: absolute; bottom: 140px; left: 50%; transform: translateX(-50%); z-index: 5; pointer-events: none; }
        .combo-text { font-size: 2.5rem; font-weight: 900; font-style: italic; color: #ff3e3e; text-shadow: 0 0 10px rgba(255, 62, 62, 0.8); margin: 0; }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div id="start-screen" class="screen-overlay">
            <h1 style="font-size: 3.8rem; margin: 10px 0; text-shadow: 0 0 20px #00d2ff; font-weight: 800; letter-spacing: 3px;">Gravity Arrow</h1>
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 25px;">활을 클릭하고 뒤로 당겼다 놓으세요! (장궁 시뮬레이터 조준)</p>
            
            <div class="main-planet-selector" id="planet-selector-bar">
                <div id="wrapper-earth" class="planet-btn-wrapper active" onclick="selectPlanet('earth')">
                    <canvas id="btn-canvas-earth" class="planet-canvas" width="60" height="60"></canvas>
                    <div class="planet-label">지구</div>
                </div>
                <div id="wrapper-moon" class="planet-btn-wrapper" onclick="selectPlanet('moon')">
                    <canvas id="btn-canvas-moon" class="planet-canvas" width="60" height="60"></canvas>
                    <div class="planet-label">달</div>
                </div>
                <div id="wrapper-mars" class="planet-btn-wrapper" onclick="selectPlanet('mars')">
                    <canvas id="btn-canvas-mars" class="planet-canvas" width="60" height="60"></canvas>
                    <div class="planet-label">화성</div>
                </div>
                <div id="wrapper-venus" class="planet-btn-wrapper" onclick="selectPlanet('venus')">
                    <canvas id="btn-canvas-venus" class="planet-canvas" width="60" height="60"></canvas>
                    <div class="planet-label">금성</div>
                </div>
                <div id="wrapper-europa" class="planet-btn-wrapper" onclick="selectPlanet('europa')">
                    <canvas id="btn-canvas-europa" class="planet-canvas" width="60" height="60"></canvas>
                    <div class="planet-label">유로파</div>
                </div>
            </div>

            <button class="btn" onclick="startGame()">게임 시작</button>
            <p style="font-size: 1rem; color: #718096; margin-top: 20px;">최고 기록: <span id="main-high-disp" style="color:#00d2ff;">0</span>점</p>
        </div>

        <div id="ingame-ui" class="ui-panel hidden">
            <div class="stats">
                행성: <span id="planet-name-disp" style="color:#ffcc00;">지구</span> |
                점수: <span id="score-disp" style="color:#00d2ff;">0</span>
            </div>
            <div class="progress-container">
                <div id="time-progress" class="progress-bar"></div>
            </div>
        </div>

        <div id="combo-wrapper" class="hidden"><p class="combo-text" id="combo-disp">5 COMBO</p></div>

        <div id="result-screen" class="screen-overlay hidden">
            <div class="result-title" id="result-title-text">GAME OVER</div>
            <div class="score-report">
                최종 점수: <span id="final-score-disp" style="color: #00d2ff; font-weight: bold;">0</span> 점<br>
                최대 콤보: <span id="final-combo-disp" style="color: #ff3e3e; font-weight: bold;">0</span> 콤보<br>
                <span id="highscore-message" style="font-size: 1.2rem; color: #4cdf50;"></span>
            </div>
            <button class="btn" onclick="goToMain()">메인으로 가기</button>
        </div>

        <canvas id="game-canvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        const bowPos = { x: 180, y: 675 / 2 };

        const planets = {
            earth: { name: '지구', gravity: 9.8, color: '#2b82c9' },
            moon: { name: '달', gravity: 1.6, color: '#777777' },
            mars: { name: '화성', gravity: 3.7, color: '#e03e1d' },
            venus: { name: '금성', gravity: 8.9, color: '#e3a857' },
            europa: { name: '유로파', gravity: 1.3, color: '#b0e0e6' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        const totalDuration = 30; let timeLeft = 30;
        let gameActive = false;
        let timerInterval, targetDirInterval;

        let meteor = { x: 0, y: 0, vx: 0, vy: 0, radius: 45, active: false, destroyed: false, rotation: 0, rotSpeed: 0.04 };
        let target = {
            x: 1200 - 150, y: 675 / 2, radiusD: 115, radiusC: 84, radiusB: 51, radiusA: 20,  
            speed: 4.5, dir: 1, visible: true, respawnTimer: 0
        };

        let combo = 0; let maxCombo = 0; let shakeIntensity = 0;
        let particles = []; let scoreTexts = [];
        let gravityScale = 0.04; let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragCurrent = { x: 0, y: 0 };
        let currentAngle = 0;
        let dynamicPower = 0;
        const maxDragDist = 180;

        let activeArrows = [];
        let arrowTrajectoryVisible = false;
        let envParticles = []; let stars = [];        

        function initCanvasSize() {
            canvas.width = 1200; canvas.height = 675;
            bowPos.x = 180; bowPos.y = canvas.height / 2;
            target.x = canvas.width - 150;
        }

        function drawPlanetButtonsVisual() {
            planetKeys.forEach(key => {
                const pCanvas = document.getElementById(`btn-canvas-${key}`);
                if (!pCanvas) return;
                const pCtx = pCanvas.getContext('2d');
                const cx = pCanvas.width / 2; const cy = pCanvas.height / 2; const r = pCanvas.width / 2 - 2;
                pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
                pCtx.save(); pCtx.beginPath(); pCtx.arc(cx, cy, r, 0, Math.PI * 2); pCtx.clip();

                if (key === 'earth') {
                    pCtx.fillStyle = '#2b82c9'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#228b22';
                    pCtx.beginPath(); pCtx.arc(cx - 12, cy - 8, 14, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 10, cy + 10, 16, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'moon') {
                    pCtx.fillStyle = '#aaaaaa'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#444444';
                    pCtx.beginPath(); pCtx.arc(cx - 12, cy - 10, 6, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 8, cy - 6, 4, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'mars') {
                    pCtx.fillStyle = '#e03e1d'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#8b4513';
                    pCtx.beginPath(); pCtx.arc(cx - 8, cy - 8, 8, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'venus') {
                    pCtx.fillStyle = '#ffd166'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#b8860b';
                    pCtx.beginPath(); pCtx.arc(cx - 10, cy + 5, 7, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'europa') {
                    pCtx.fillStyle = '#b0e0e6'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.strokeStyle = '#5f9ea0'; pCtx.lineWidth = 2;
                    pCtx.beginPath(); pCtx.moveTo(cx - 20, cy - 15); pCtx.lineTo(cx + 15, cy + 20); pCtx.stroke();
                }
                pCtx.restore();
            });
        }

        function initEnvParticles() {
            envParticles = [];
            let count = 0;
            if (currentPlanetKey === 'earth') count = 8;
            else if (currentPlanetKey === 'mars') count = 40;
            else if (currentPlanetKey === 'venus') count = 65;
            else if (currentPlanetKey === 'europa') count = 100;

            for (let i = 0; i < count; i++) envParticles.push(createEnvParticle(true));
        }

        function createEnvParticle(randomY = true) {
            let p = { x: Math.random() * canvas.width, y: randomY ? Math.random() * canvas.height : 0 };
            if (currentPlanetKey === 'earth') {
                p.w = 110 + Math.random() * 130; p.h = 45 + Math.random() * 35; p.vx = 0.2 + Math.random() * 0.4; p.vy = 0;
            } else if (currentPlanetKey === 'mars') {
                p.r = 1.5 + Math.random() * 2.5; p.vx = Math.random() * 0.4 - 0.2; p.vy = Math.random() * 0.3 - 0.15;
            } else if (currentPlanetKey === 'venus') {
                p.w = 8 + Math.random() * 25; p.h = 2 + Math.random() * 2.5; p.vx = -3.0 - Math.random() * 4.0; p.vy = (Math.random() - 0.5) * 0.3;
            } else if (currentPlanetKey === 'europa') {
                p.r = 1.2 + Math.random() * 3.0; p.vx = Math.random() * 0.8 - 0.4; p.vy = 1.0 + Math.random() * 2.0;
            }
            return p;
        }

        function initStars() {
            stars = [];
            for(let i=0; i<120; i++) stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, r: Math.random() * 1.5 });
        }

        function selectPlanet(key) {
            if (gameActive) return;
            currentPlanetKey = key;
            planetKeys.forEach(k => document.getElementById(`wrapper-${k}`).classList.remove('active'));
            document.getElementById(`wrapper-${key}`).classList.add('active');
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            currentAngle = 0;
            initStars(); initEnvParticles();
        }

        function startGame() {
            score = 0; timeLeft = totalDuration; combo = 0; maxCombo = 0; gameActive = true;
            activeArrows = []; particles = []; scoreTexts = []; currentAngle = 0;
            isDragging = false; arrowTrajectoryVisible = false;
            
            target.visible = true; target.respawnTimer = 0;
            target.y = canvas.height / 2;
            meteor.active = false; meteor.destroyed = false;

            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('ingame-ui').classList.remove('hidden');
            document.getElementById('score-disp').innerText = score;
            updateProgressBar(); initStars(); initEnvParticles();

            if(targetDirInterval) clearInterval(targetDirInterval);
            targetDirInterval = setInterval(() => { if(!gameActive) clearInterval(targetDirInterval); target.dir *= -1; }, 4500);

            if(timerInterval) clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                timeLeft--; updateProgressBar();
                if(timeLeft === 20 && !meteor.destroyed) spawnMeteor();
                if(timeLeft <= 0) endGame();
            }, 1000);
        }

        function updateProgressBar() {
            const bar = document.getElementById('time-progress');
            if (bar) bar.style.width = `${(timeLeft / totalDuration) * 100}%`;
        }

        function spawnMeteor() {
            meteor.x = canvas.width + 60; meteor.y = 80;
            let dx = bowPos.x - meteor.x; let dy = bowPos.y - meteor.y; let distance = Math.hypot(dx, dy);
            meteor.vx = (dx / distance) * 2.5; meteor.vy = (dy / distance) * 2.5;
            meteor.active = true;
        }

        function endGame() {
            gameActive = false; clearInterval(timerInterval); if(targetDirInterval) clearInterval(targetDirInterval);
            document.getElementById('ingame-ui').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');

            document.getElementById('final-score-disp').innerText = score;
            document.getElementById('final-combo-disp').innerText = maxCombo;
            const msgElement = document.getElementById('highscore-message');
            const titleElement = document.getElementById('result-title-text');

            if(score > highScore) {
                highScore = score; localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('main-high-disp').innerText = highScore;
                titleElement.innerText = "NEW RECORD!"; titleElement.style.color = "#4cdf50";
                msgElement.innerText = "축하합니다! 최고 기록을 경신했습니다!";
            } else {
                titleElement.innerText = "GAME OVER"; titleElement.style.color = "#ffcc00"; msgElement.innerText = "";
            }
            document.getElementById('result-screen').classList.remove('hidden');
        }

        function goToMain() {
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('hidden');
            activeArrows = []; particles = []; scoreTexts = []; currentAngle = 0;
            initStars(); initEnvParticles(); drawPlanetButtonsVisual();
        }

        function createExplosion(x, y, type) {
            let count = type === "meteor" ? 40 : 15;
            let colors = ["#ffffff"];
            
            if (type === "gold" || type === "yellow") colors = ["#ffcc00", "#ff5500", "#ffffff"];
            else if (type === "red") colors = ["#ff2222", "#ff6666", "#aa0000"]; 
            else if (type === "stone") colors = ["#999999", "#cccccc", "#555555"]; 
            else if (type === "spark") colors = ["#ffea00", "#ff9100", "#ffffff"]; 
            else if (type === "meteor") colors = ["#5c4033", "#ff3e3e", "#3a2a20", "#ffaa00"]; 

            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2; 
                let speed = type === "spark" ? 2 + Math.random() * 6 : 1 + Math.random() * 4;
                particles.push({
                    x: x, y: y, 
                    vx: Math.cos(angle) * speed, 
                    vy: Math.sin(angle) * speed,
                    radius: type === "meteor" ? 2 + Math.random() * 6 : 1.5 + Math.random() * 3, 
                    color: colors[Math.floor(Math.random() * colors.length)], 
                    alpha: 1, 
                    decay: 0.02 + Math.random() * 0.02
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -0.8 });
        }

        function getCanvasMousePos(e) {
            const rect = canvas.getBoundingClientRect();
            return { x: (e.clientX - rect.left) * (canvas.width / rect.width), y: (e.clientY - rect.top) * (canvas.height / rect.height) };
        }

        canvas.addEventListener('mousedown', (e) => {
            if (!gameActive) return;
            let pos = getCanvasMousePos(e);
            if (Math.hypot(pos.x - bowPos.x, pos.y - bowPos.y) < 160) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragCurrent = { x: pos.x, y: pos.y };
                arrowTrajectoryVisible = true;
            }
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            let pos = getCanvasMousePos(e);
            dragCurrent = { x: pos.x, y: pos.y };
            
            let dx = dragStart.x - dragCurrent.x;
            let dy = dragStart.y - dragCurrent.y;
            currentAngle = Math.atan2(dy, dx);
            
            let dist = Math.hypot(dx, dy);
            dynamicPower = Math.min(dist / maxDragDist, 1.0) * 26; 
        });

        window.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;
            arrowTrajectoryVisible = false;

            if (dynamicPower > 3) {
                let vx = Math.cos(currentAngle) * dynamicPower;
                let vy = Math.sin(currentAngle) * dynamicPower;

                if (vx > 0) {
                    activeArrows.push({
                        x: bowPos.x, y: bowPos.y, vx: vx, vy: vy,
                        width: 85, height: 3, collided: false, handled: false,
                        spinAngle: 0, trail: []
                    });
                }
            }
            dynamicPower = 0;
        });

        function updateLoop() {
            if (gameActive) {
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y < 0) {
                        target.y = 0; target.dir = 1;
                    } else if (target.y > canvas.height) {
                        target.y = canvas.height; target.dir = -1;
                    }
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) { target.y = Math.random() * canvas.height; target.visible = true; }
                }
                if(meteor.active) {
                    meteor.x += meteor.vx; meteor.y += meteor.vy;
                    meteor.rotation += meteor.rotSpeed;
                    if(meteor.x < bowPos.x - 50) {
                        meteor.active = false; createExplosion(meteor.x, meteor.y, "meteor"); shakeIntensity = 15;
                    }
                }
            }

            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; if (shakeIntensity < 0.2) shakeIntensity = 0;
            }
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB';
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505';
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#f0d399';
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#cca43b';
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#b0e0e6';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.5)";
                stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill(); });
            }

            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if (currentPlanetKey === 'venus') {
                    if (p.x < -40) { p.x = canvas.width + 40; p.y = Math.random() * canvas.height; }
                } else if (currentPlanetKey === 'europa') {
                    if (p.y > canvas.height) { p.y = 0; p.x = Math.random() * canvas.width; }
                } else {
                    if (p.x > canvas.width + 150) p.x = -150;
                }

                if (currentPlanetKey === 'earth') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
                    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.w/2, p.h/2, 0, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = 'rgba(139, 69, 19, 0.35)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = 'rgba(184, 134, 11, 0.45)';
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            // [요구사항 반영] 달을 포함한 행성별 지표면(땅) 실루엣 컴백 추가
            if (currentPlanetKey === 'earth') ctx.fillStyle = "#1e3d22";
            else if (currentPlanetKey === 'moon') ctx.fillStyle = "#1c1d1f";
            else if (currentPlanetKey === 'mars') ctx.fillStyle = "#3b160b";
            else if (currentPlanetKey === 'venus') ctx.fillStyle = "#42330b";
            else if (currentPlanetKey === 'europa') ctx.fillStyle = "#1e2e3d";
            
            ctx.beginPath();
            ctx.moveTo(0, canvas.height - 50);
            ctx.quadraticCurveTo(canvas.width / 2, canvas.height - 95, canvas.width, canvas.height - 45);
            ctx.lineTo(canvas.width, canvas.height);
            ctx.lineTo(0, canvas.height);
            ctx.fill();

            if(meteor.active) {
                ctx.save();
                let tailGrad = ctx.createLinearGradient(meteor.x, meteor.y, meteor.x + 110, meteor.y - 40);
                tailGrad.addColorStop(0, "rgba(255, 60, 0, 0.85)");
                tailGrad.addColorStop(0.3, "rgba(239, 68, 68, 0.4)");
                tailGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
                ctx.fillStyle = tailGrad; ctx.beginPath();
                ctx.moveTo(meteor.x, meteor.y - meteor.radius + 5); 
                ctx.lineTo(meteor.x + 120, meteor.y - 45); 
                ctx.lineTo(meteor.x + 40, meteor.y + meteor.radius - 5);
                ctx.closePath(); ctx.fill();

                ctx.translate(meteor.x, meteor.y); 
                ctx.rotate(meteor.rotation);
                
                let meteorGrad = ctx.createRadialGradient(-10, -10, 5, 5, 5, meteor.radius);
                meteorGrad.addColorStop(0, '#8b7355'); 
                meteorGrad.addColorStop(0.6, '#4a3525'); 
                meteorGrad.addColorStop(1, '#1f140e'); 
                
                ctx.fillStyle = meteorGrad; ctx.beginPath(); 
                ctx.arc(0, 0, meteor.radius, 0, Math.PI*2); ctx.fill();

                let craters = [
                    {cx: -15, cy: -10, cr: 10}, {cx: 15, cy: 12, cr: 8}, 
                    {cx: -5, cy: 20, cr: 6}, {cx: 20, cy: -15, cr: 7}
                ];
                craters.forEach(c => {
                    ctx.beginPath(); ctx.arc(c.cx, c.cy, c.cr, 0, Math.PI*2);
                    ctx.fillStyle = "rgba(20, 10, 5, 0.65)"; ctx.fill();
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)"; ctx.lineWidth = 1.5; ctx.stroke();
                });
                ctx.restore();
            }

            const skewX = 0.25;
            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "rgba(40, 50, 70, 0.4)"; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.moveTo(target.x + 5, 0); ctx.lineTo(target.x + 5, canvas.height); ctx.stroke();
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ff3e3e"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ffcc00"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // [버그 수정 완료] 활과 화살 조준 상태 드로잉 통합 행렬 적용 공간
            ctx.save(); 
            ctx.translate(bowPos.x, bowPos.y); 
            ctx.rotate(currentAngle);
            
            ctx.strokeStyle = "#8b5a2b"; ctx.lineWidth = 7;
            ctx.beginPath(); ctx.arc(-25, 0, 75, -Math.PI/2.3, Math.PI/2.3); ctx.stroke();
            
            let stringX = -20;
            if(isDragging) {
                stringX = -20 - (dynamicPower * 4.0); // 활 당겨지는 물리 깊이
                ctx.strokeStyle = "rgba(255,255,255,0.9)"; ctx.lineWidth = 2.0;
                ctx.beginPath(); ctx.moveTo(-20, -70); ctx.lineTo(stringX, 0); ctx.lineTo(-20, 70); ctx.stroke();
            } else {
                ctx.strokeStyle = "rgba(255,255,255,0.4)"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.moveTo(-20, -70); ctx.lineTo(-20, 70); ctx.stroke();
            }

            // [대형 버그 패치] 대기/조준 화살을 활의 완전 로컬 좌표계 내부에 결속하여 절대 어긋나지 않도록 수정
            if(gameActive) {
                let arrowX = stringX + 41; // shaftLength(82) / 2 = 41 (꼬리가 시위에 정확히 맞닿는 정렬값)
                ctx.save();
                ctx.translate(arrowX, 0);
                drawArrowShapeLocal(0); // 회전 없는 고정 상태 조준 드로우
                ctx.restore();
            }
            ctx.restore();

            if (arrowTrajectoryVisible && gameActive && dynamicPower > 3) {
                let tVx = Math.cos(currentAngle) * dynamicPower;
                if (tVx > 0) {
                    ctx.save();
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.45)";
                    ctx.lineWidth = 2.0; ctx.setLineDash([4, 4]); ctx.beginPath();
                    let tX = bowPos.x; let tY = bowPos.y; let tVy = Math.sin(currentAngle) * dynamicPower;
                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                }
            }

            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                arrow.trail.push({ x: arrow.x, y: arrow.y });
                if (arrow.trail.length > 5) arrow.trail.shift();

                arrow.x += arrow.vx; arrow.y += arrow.vy; arrow.vy += currentGravity;
                arrow.spinAngle += 0.35; 
                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);

                if (arrow.trail.length > 1) {
                    ctx.save(); ctx.beginPath();
                    ctx.moveTo(arrow.trail[0].x, arrow.trail[0].y);
                    for (let j = 1; j < arrow.trail.length; j++) ctx.lineTo(arrow.trail[j].x, arrow.trail[j].y);
                    ctx.strokeStyle = "rgba(240, 245, 255, 0.28)"; ctx.lineWidth = 2.5; ctx.stroke(); ctx.restore();
                }

                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.spinAngle);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                if (arrow.x > canvas.width + 150 || arrow.y > canvas.height + 150 || arrow.y < -150) {
                    if(!arrow.handled) { combo = 0; document.getElementById('combo-wrapper').classList.add('hidden'); }
                    activeArrows.splice(i, 1); continue;
                }

                if(meteor.active) {
                    if(Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y) <= meteor.radius + 10) {
                        meteor.active = false; meteor.destroyed = true; arrow.handled = true;
                        createExplosion(meteor.x, meteor.y, "meteor");
                        score += 30; combo++; if(combo > maxCombo) maxCombo = combo;
                        document.getElementById('score-disp').innerText = score;
                        createScoreText(meteor.x, meteor.y - 20, `METEOR CRUSH +30`, "#ffaa00");
                        activeArrows.splice(i, 1); continue;
                    }
                }

                if (target.visible && !arrow.handled) {
                    if (arrowTipX >= target.x - 22 && arrowTipX <= target.x + 22) {
                        let currentRadY = Math.abs(arrowTipY - target.y);
                        if (currentRadY <= target.radiusD) {
                            arrow.handled = true;
                            let addedScore = 0; let scoreColor = "#ffffff"; let hitType = "red"; 

                            if (currentRadY <= target.radiusA) {
                                addedScore = 10; scoreColor = "#ffcc00"; hitType = "spark"; 
                                combo++; if(combo > maxCombo) maxCombo = combo;
                                createScoreText(target.x - 40, target.y - 30, `BULLSEYE +10 (${combo} Combo)`, scoreColor);
                            } else if (currentRadY <= target.radiusB) {
                                addedScore = 5; scoreColor = "#00d2ff"; hitType = "stone"; 
                                combo++; if(combo > maxCombo) maxCombo = combo;
                                createScoreText(target.x - 20, arrowTipY, `HIT +5`, scoreColor);
                            } else {
                                addedScore = 2; scoreColor = "#ffffff"; hitType = "red"; combo = 0;
                                createScoreText(target.x - 10, arrowTipY, `JUST FIT +2`, scoreColor);
                            }

                            score += addedScore; document.getElementById('score-disp').innerText = score;
                            createExplosion(arrowTipX, arrowTipY, hitType);

                            if (combo >= 3) {
                                let cDisp = document.getElementById('combo-disp');
                                let cWrap = document.getElementById('combo-wrapper');
                                cDisp.innerText = `${combo} COMBO`; cWrap.classList.remove('hidden');
                            } else {
                                document.getElementById('combo-wrapper').classList.add('hidden');
                            }

                            target.visible = false; target.respawnTimer = 22; activeArrows.splice(i, 1);
                        }
                    }
                }
            }

            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i]; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fill(); ctx.restore();
            }

            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i]; stx.y += stx.vy; stx.alpha -= 0.015;
                if (stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 1.4rem sans-serif"; ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore();
            requestAnimationFrame(updateLoop);
        }

        // 공용 호출을 위해 내부 셰이더 함수 추출 래핑 완료
        function drawArrowIcon(x, y, angle, spinAngle) {
            ctx.save(); ctx.translate(x, y); ctx.rotate(angle);
            drawArrowShapeLocal(spinAngle);
            ctx.restore();
        }

        function drawArrowShapeLocal(spinAngle) {
            let shaftLength = 82; 
            let shaftGrad = ctx.createLinearGradient(-shaftLength/2, -1.5, -shaftLength/2, 1.5);
            shaftGrad.addColorStop(0, '#2e1c0c'); 
            shaftGrad.addColorStop(0.5, '#4e3629'); 
            shaftGrad.addColorStop(1, '#1b0f07');
            ctx.fillStyle = shaftGrad; ctx.fillRect(-shaftLength/2, -1.5, shaftLength, 3); 

            let tipLength = 12; let tipStartX = shaftLength / 2;
            ctx.save();
            let flashAlpha = Math.abs(Math.sin(spinAngle));
            let tipGrad = ctx.createLinearGradient(tipStartX, -3, tipStartX + tipLength, 3);
            tipGrad.addColorStop(0, '#b0bec5'); 
            tipGrad.addColorStop(0.5 * flashAlpha, '#ffffff'); 
            tipGrad.addColorStop(1, '#607d8b'); 

            ctx.fillStyle = tipGrad; ctx.beginPath(); ctx.moveTo(tipStartX, -4); ctx.lineTo(tipStartX + tipLength, 0); ctx.lineTo(tipStartX, 4); ctx.closePath(); ctx.fill();
            ctx.restore();

            let featherStartX = -shaftLength / 2 + 5;
            let featherGradTop = ctx.createLinearGradient(featherStartX, -1.5, featherStartX - 14, -8);
            featherGradTop.addColorStop(0, '#ffffff'); featherGradTop.addColorStop(1, '#5c4033');
            ctx.fillStyle = featherGradTop; ctx.beginPath(); ctx.moveTo(featherStartX, -1.5); ctx.lineTo(featherStartX - 15, -9); ctx.lineTo(featherStartX - 10, -1.5); ctx.closePath(); ctx.fill();

            let featherGradBot = ctx.createLinearGradient(featherStartX, 1.5, featherStartX - 14, 8);
            featherGradBot.addColorStop(0, '#ffffff'); featherGradBot.addColorStop(1, '#5c4033');
            ctx.fillStyle = featherGradBot; ctx.beginPath(); ctx.moveTo(featherStartX, 1.5); ctx.lineTo(featherStartX - 15, 9); ctx.lineTo(featherStartX - 10, 1.5); ctx.closePath(); ctx.fill();

            ctx.fillStyle = "#ff5722"; ctx.fillRect(-shaftLength/2 - 2, -2, 2, 4);
            ctx.fillStyle = "#000000"; ctx.fillRect(-shaftLength/2 - 1, -1, 1, 2);
        }

        window.onload = function() {
            initCanvasSize();
            document.getElementById('main-high-disp').innerText = highScore;
            drawPlanetButtonsVisual();
            initStars();
            initEnvParticles();
            requestAnimationFrame(updateLoop);
        };
    </script>
</body>
</html>
"""

components.html(game_html, height=720, scrolling=False)
