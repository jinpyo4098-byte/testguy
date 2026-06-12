import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gravity Arrow - Pure Standard Edition", layout="wide")
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
    <title>Gravity Arrow - Standard Arrow Only</title>
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
        h1 { font-size: 3.8rem; margin: 10px 0; text-shadow: 0 0 20px #00d2ff; font-weight: 800; letter-spacing: 3px; }
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
            <h1>Gravity Arrow</h1>
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 25px;">활을 마우스로 클릭 후 뒤로 당겨서(드래그) 조준하고 놓으세요!</p>
            
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
        const bowPos = { x: 200, y: (675 - 120) / 2 }; 

        function initCanvasSize() {
            canvas.width = 1200; canvas.height = 675;
            bowPos.x = 200; bowPos.y = (canvas.height - 120) / 2;
            target.x = canvas.width - 150; 
        }

        const planets = {
            earth: { name: '지구', gravity: 9.8, color: '#2b82c9' },
            moon: { name: '달', gravity: 1.6, color: '#ccc' },
            mars: { name: '화성', gravity: 3.7, color: '#e03e1d' },
            venus: { name: '금성', gravity: 8.9, color: '#e3a857' },
            europa: { name: '유로파', gravity: 1.3, color: '#a5cad6' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        const totalDuration = 30; let timeLeft = 30;
        let gameActive = false;
        let timerInterval, targetDirInterval;

        // 디테일 운석 객체
        let meteor = { x: 0, y: 0, vx: 0, vy: 0, radius: 45, active: false, destroyed: false, rotation: 0, rotSpeed: 0.02 };

        let target = {
            x: 1200 - 150, y: (675 - 120) / 2, radiusD: 115, radiusC: 84, radiusB: 51, radiusA: 20,  
            speed: 2.5, dir: 1, visible: true, respawnTimer: 0
        };

        let combo = 0; let maxCombo = 0; let shakeIntensity = 0;
        let particles = []; let scoreTexts = [];
        let gravityScale = 0.03; let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 드래그 조준 상태 변수
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragCurrent = { x: 0, y: 0 };
        let currentAngle = 0;
        let dynamicPower = 0;
        const maxDragDist = 160;

        let activeArrows = [];
        let arrowTrajectoryVisible = false;

        let envParticles = []; let stars = [];        
        document.getElementById('main-high-disp').innerText = highScore;
        initCanvasSize();

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
                    pCtx.fillStyle = '#228b22'; pCtx.beginPath(); pCtx.arc(cx - 10, cy - 5, 15, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'moon') {
                    pCtx.fillStyle = '#bbbbbb'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#666666'; pCtx.beginPath(); pCtx.arc(cx - 12, cy - 10, 5, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'mars') {
                    pCtx.fillStyle = '#e03e1d'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#8b4513'; pCtx.beginPath(); pCtx.arc(cx - 8, cy - 8, 7, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'venus') {
                    pCtx.fillStyle = '#ffd166'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#b8860b'; pCtx.beginPath(); pCtx.ellipse(cx, cy - 10, 20, 5, 0, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'europa') {
                    pCtx.fillStyle = '#a5cad6'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.strokeStyle = '#4682b4'; pCtx.lineWidth = 2; pCtx.beginPath(); pCtx.moveTo(cx - 20, cy - 20); pCtx.lineTo(cx + 20, cy + 20); pCtx.stroke();
                }
                pCtx.restore();
            });
        }

        function initEnvParticles() {
            envParticles = [];
            let count = currentPlanetKey === 'earth' ? 8 : (currentPlanetKey === 'mars' ? 40 : (currentPlanetKey === 'venus' ? 65 : 90));
            for (let i = 0; i < count; i++) envParticles.push(createEnvParticle(true));
        }

        function createEnvParticle(randomY = true) {
            let p = { x: Math.random() * canvas.width, y: Math.random() * (canvas.height - 120) };
            if (currentPlanetKey === 'earth') { p.w = 110 + Math.random() * 130; p.h = 40 + Math.random() * 35; p.vx = 0.2 + Math.random() * 0.4; p.vy = 0; }
            else if (currentPlanetKey === 'mars') { p.r = 1.2 + Math.random() * 2.5; p.vx = Math.random() * 0.6 - 0.3; p.vy = Math.random() * 0.4 - 0.2; }
            else if (currentPlanetKey === 'venus') { p.w = 8 + Math.random() * 25; p.h = 1.5 + Math.random() * 2; p.vx = -2.5 - Math.random() * 3.5; p.vy = (Math.random() - 0.5) * 0.3; }
            else if (currentPlanetKey === 'europa') { p.r = 1.0 + Math.random() * 2.8; p.vx = Math.random() * 0.8 - 0.4; p.vy = 0.8 + Math.random() * 1.5; }
            return p;
        }

        function initStars() {
            stars = [];
            for(let i=0; i<120; i++) stars.push({ x: Math.random() * canvas.width, y: Math.random() * (canvas.height - 120), r: Math.random() * 1.4 });
        }

        function selectPlanet(key) {
            if (gameActive) return; 
            currentPlanetKey = key;
            planetKeys.forEach(k => document.getElementById(`wrapper-${k}`).classList.remove('active'));
            document.getElementById(`wrapper-${key}`).classList.add('active');
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            initStars(); initEnvParticles();
        }

        function startGame() {
            score = 0; timeLeft = totalDuration; combo = 0; maxCombo = 0; gameActive = true;
            activeArrows = []; particles = []; scoreTexts = [];
            isDragging = false; arrowTrajectoryVisible = false;
            
            target.visible = true; target.respawnTimer = 0;
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
                if(timeLeft === 15 && !meteor.destroyed) spawnMeteor();
                if(timeLeft <= 0) endGame();
            }, 1000);
        }

        function updateProgressBar() {
            const bar = document.getElementById('time-progress');
            bar.style.width = `${(timeLeft / totalDuration) * 100}%`;
        }

        function spawnMeteor() {
            meteor.x = canvas.width + 50; meteor.y = 70; 
            let dx = bowPos.x - meteor.x; let dy = bowPos.y - meteor.y; let distance = Math.hypot(dx, dy);
            meteor.vx = (dx / distance) * 1.3; meteor.vy = (dy / distance) * 1.3;
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
            activeArrows = []; particles = []; scoreTexts = [];
            initStars(); initEnvParticles(); drawPlanetButtonsVisual();
        }

        function createExplosion(x, y, color, customCount) {
            let count = customCount || 15; 
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2; let speed = 1 + Math.random() * 5;
                particles.push({
                    x: x, y: y, vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
                    radius: 2 + Math.random() * 4, color: color, alpha: 1, decay: 0.015 + Math.random() * 0.02
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

        window.addEventListener('mousedown', (e) => {
            if (!gameActive) return;
            let pos = getCanvasMousePos(e);
            if (pos.x >= 0 && pos.x <= canvas.width && pos.y >= 0 && pos.y <= canvas.height) {
                isDragging = true;
                dragStart = { x: pos.x, y: pos.y };
                dragCurrent = { x: pos.x, y: pos.y };
                arrowTrajectoryVisible = true;
            }
        });

        window.addEventListener('mousemove', (e) => {
            let pos = getCanvasMousePos(e);
            if (isDragging) {
                dragCurrent = { x: pos.x, y: pos.y };
                let dx = dragStart.x - dragCurrent.x;
                let dy = dragStart.y - dragCurrent.y;
                currentAngle = Math.atan2(dy, dx); 
                let dist = Math.hypot(dx, dy);
                dynamicPower = Math.min(dist / maxDragDist, 1.0) * 24; 
            } else {
                currentAngle = Math.atan2(pos.y - bowPos.y, pos.x - bowPos.x);
            }
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
                        width: 95, height: 5, collided: false, handled: false 
                    });
                }
            }
            dynamicPower = 0;
        });

        function updateLoop() {
            if (gameActive) {
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 40 || target.y + target.radiusD > canvas.height - 135) target.dir *= -1; 
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) { target.y = 80 + Math.random() * (canvas.height - 240); target.visible = true; }
                }
                if(meteor.active) {
                    meteor.x += meteor.vx; meteor.y += meteor.vy;
                    meteor.rotation += meteor.rotSpeed; 
                    if(meteor.x < bowPos.x - 20) {
                        meteor.active = false; createExplosion(meteor.x, meteor.y, "#ef4444", 30); shakeIntensity = 10;
                    }
                }
            }

            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; if (shakeIntensity < 0.2) shakeIntensity = 0;
            }
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 행성별 우주 배경 채색
            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB'; 
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505'; 
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#cda365'; 
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#dcb858'; 
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#b0e0e6'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.48)";
                stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill(); });
            }

            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if (p.x > canvas.width + 120) p.x = -120;
                ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
                ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, Math.PI*2); ctx.fill();
            });

            // 지형 바닥 지면 리얼 렌더링
            let groundHeight = 120; let gY = canvas.height - groundHeight;
            ctx.fillStyle = '#334155'; ctx.fillRect(0, gY, canvas.width, groundHeight);

            // 입체 디테일 메테오 운석 비주얼
            if(meteor.active) {
                ctx.save();
                let tailGrad = ctx.createLinearGradient(meteor.x, meteor.y, meteor.x + 80, meteor.y - 30);
                tailGrad.addColorStop(0, "rgba(239, 68, 68, 0.8)");
                tailGrad.addColorStop(1, "rgba(239, 68, 68, 0)");
                ctx.fillStyle = tailGrad;
                ctx.beginPath();
                ctx.moveTo(meteor.x, meteor.y - meteor.radius);
                ctx.lineTo(meteor.x + 90, meteor.y - 35);
                ctx.lineTo(meteor.x + 35, meteor.y + meteor.radius);
                ctx.closePath(); ctx.fill();

                ctx.translate(meteor.x, meteor.y);
                ctx.rotate(meteor.rotation);
                let rockGrad = ctx.createRadialGradient(-10, -10, 5, 0, 0, meteor.radius);
                rockGrad.addColorStop(0, '#78716c'); rockGrad.addColorStop(1, '#1c1917');
                ctx.fillStyle = rockGrad; ctx.beginPath(); ctx.arc(0, 0, meteor.radius, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = "rgba(28, 25, 23, 0.6)";
                ctx.beginPath(); ctx.arc(-15, -5, 10, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(10, 15, 12, 0, Math.PI*2); ctx.fill();
                ctx.restore();
            }

            // 움직이는 리얼 과녁 시스템
            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "rgba(40, 50, 70, 0.5)"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD); ctx.stroke();
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
                
                ctx.fillStyle = "#ff3e3e"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ffcc00"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // 활 및 고무줄 비주얼 드로우
            ctx.save(); ctx.translate(bowPos.x, bowPos.y); ctx.rotate(currentAngle);
            ctx.strokeStyle = "#00d2ff"; ctx.lineWidth = 6; 
            ctx.beginPath(); ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); ctx.stroke();
            
            if(isDragging) {
                ctx.strokeStyle = "rgba(255,255,255,0.7)"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-dynamicPower*3, 0); ctx.lineTo(-15, 65); ctx.stroke();
            } else {
                ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-15, 65); ctx.stroke();
            }
            ctx.restore();

            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, 95);
            }

            // 포물선 예측선 시스템
            if (arrowTrajectoryVisible && gameActive && dynamicPower > 3) {
                let tVx = Math.cos(currentAngle) * dynamicPower;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.55)";
                    ctx.lineWidth = 2.5; ctx.setLineDash([5, 5]); ctx.beginPath();
                    let tX = bowPos.x; let tY = bowPos.y; let tVy = Math.sin(currentAngle) * dynamicPower;
                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                }
            }

            // 투사체 시뮬레이션 연산 (일반 화살 전용)
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                arrow.x += arrow.vx; arrow.y += arrow.vy; arrow.vy += currentGravity;
                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                if (arrow.x > canvas.width + 150 || arrow.y > canvas.height + 150 || arrow.y < -150) {
                    if(!arrow.handled) { combo = 0; document.getElementById('combo-wrapper').classList.add('hidden'); }
                    activeArrows.splice(i, 1); continue;
                }

                if(meteor.active) {
                    if(Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y) <= meteor.radius + 15) {
                        meteor.active = false; meteor.destroyed = true; activeArrows.splice(i, 1);
                        createExplosion(meteor.x, meteor.y, "#ef4444", 30); 
                        score += 15; document.getElementById('score-disp').innerText = score;
                        createScoreText(meteor.x, meteor.y, "+15 Meteor Clear!", "#ef4444");
                        continue;
                    }
                }

                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + 15 && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);
                    if (dy <= target.radiusD) {
                        arrow.handled = true; target.visible = false; target.respawnTimer = 45; 
                        combo++; if(combo > maxCombo) maxCombo = combo;
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = dy <= target.radiusA ? 10 : (dy <= target.radiusB ? 5 : 2);
                        score += (earnedPoints + Math.floor(combo / 3));
                        document.getElementById('score-disp').innerText = score;

                        createExplosion(arrowTipX, arrowTipY, "#00d2ff", 20);
                        createScoreText(arrowTipX, arrowTipY, `+${earnedPoints}`, "#00d2ff");
                        activeArrows.splice(i, 1); continue;
                    }
                }
            }

            // 이펙트 렌더링
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i]; p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i]; stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color; ctx.font = "bold 22px 'Segoe UI'";
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            requestAnimationFrame(updateLoop);
        }

        // 오직 표준 화살 비주얼만 드로우하도록 간소화
        function drawArrowIcon(x, y, angle, customWidth) {
            ctx.save(); ctx.translate(x, y); ctx.rotate(angle);
            let width = customWidth || 95; 
            ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 4.5;
            ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); ctx.stroke();
            ctx.restore();
        }

        drawPlanetButtonsVisual(); initStars(); initEnvParticles();
        requestAnimationFrame(updateLoop);
    </script>
</body>
</html>
"""

components.html(game_html, height=760, scrolling=False)
