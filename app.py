import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정 및 여백 제거
st.set_page_config(page_title="Gravity Arrow - Planetary Journey", layout="wide")
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
    <title>Gravity Arrow</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #050608;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #game-wrapper {
            position: relative;
            width: 1200px;
            height: 675px;
            background: #000;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.8), 0 0 2px rgba(255, 255, 255, 0.2);
            overflow: hidden;
            border-radius: 8px;
        }

        #game-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: transparent;
            cursor: crosshair;
            z-index: 1;
        }

        .screen-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(5, 6, 8, 0.92);
            z-index: 10;
        }

        .hidden {
            display: none !important;
        }

        h1 {
            font-size: 3.8rem;
            margin: 10px 0;
            text-shadow: 0 0 20px #00d2ff;
            font-weight: 800;
            letter-spacing: 3px;
        }

        .result-title {
            font-size: 3.2rem;
            color: #ffcc00;
            text-shadow: 0 0 15px #ffcc00;
            margin-bottom: 15px;
        }

        .score-report {
            font-size: 1.6rem;
            margin-bottom: 35px;
            text-align: center;
            line-height: 1.6;
        }

        .ui-panel {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 70%;
            max-width: 600px;
            background: rgba(255, 255, 255, 0.07);
            padding: 12px 25px;
            border-radius: 20px;
            box-sizing: border-box;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 5;
        }

        .stats {
            font-size: 1.2rem;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 8px;
            width: 100%;
            text-align: center;
        }

        .progress-container {
            width: 100%;
            height: 12px;
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .progress-bar {
            height: 100%;
            width: 100%;
            background: linear-gradient(90deg, #0066ff, #00d2ff);
            box-shadow: 0 0 10px #00d2ff;
            transition: width 0.1s linear, background 0.3s;
        }

        .progress-bar.buffed {
            background: linear-gradient(90deg, #ff0055, #ffcc00) !important;
            box-shadow: 0 0 15px #ff0055 !important;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 14px 38px;
            font-size: 1.3rem;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 132, 255, 0.6);
        }

        .main-planet-selector {
            display: flex;
            gap: 15px;
            align-items: center;
            margin-bottom: 35px;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px 30px;
            border-radius: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .planet-circle {
            width: 55px;
            height: 55px;
            border-radius: 50%;
            cursor: pointer;
            border: 3px solid transparent;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000;
        }

        .planet-circle:hover {
            transform: scale(1.15);
        }

        .planet-circle.active {
            border-color: #fff;
            box-shadow: 0 0 18px currentColor;
            transform: scale(1.05);
        }

        #planet-earth { background: radial-gradient(circle at 30% 30%, #2ecc71, #2980b9); color: #2ecc71; }
        #planet-moon { background: radial-gradient(circle at 30% 30%, #bdc3c7, #2c3e50); color: #bdc3c7; }
        #planet-mars { background: radial-gradient(circle at 30% 30%, #e67e22, #c0392b); color: #e67e22; }
        #planet-venus { background: radial-gradient(circle at 30% 30%, #f1c40f, #d35400); color: #f1c40f; }
        #planet-europa { background: radial-gradient(circle at 30% 30%, #ecf0f1, #3498db); color: #ecf0f1; }

        #combo-wrapper {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
            text-align: center;
            pointer-events: none;
        }
       
        .combo-text {
            font-size: 2.5rem;
            font-weight: 900;
            font-style: italic;
            color: #ff3e3e;
            text-shadow: 0 0 10px rgba(255, 62, 62, 0.8), 0 0 20px rgba(255, 200, 0, 0.5);
            margin: 0;
        }

        #buff-alert {
            position: absolute;
            top: 110px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.8rem;
            font-weight: bold;
            color: #ffcc00;
            text-shadow: 0 0 15px #ff3300;
            z-index: 5;
            pointer-events: none;
            letter-spacing: 2px;
            background: rgba(0,0,0,0.5);
            padding: 6px 20px;
            border-radius: 12px;
            width: max-content;
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
       
        <div id="start-screen" class="screen-overlay">
            <h1>Gravity Arrow</h1>
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 25px;">[조작] 마우스: 각도 조절 / 스페이스바: 발사</p>
           
            <div class="main-planet-selector" id="planet-selector-bar">
                <div id="planet-earth" class="planet-circle active" onclick="selectPlanet('earth')">지구</div>
                <div id="planet-moon" class="planet-circle" onclick="selectPlanet('moon')">달</div>
                <div id="planet-mars" class="planet-circle" onclick="selectPlanet('mars')">화성</div>
                <div id="planet-venus" class="planet-circle" onclick="selectPlanet('venus')">금성</div>
                <div id="planet-europa" class="planet-circle" onclick="selectPlanet('europa')">유로파</div>
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

        <div id="buff-alert" class="hidden">🔥 기가 과녁 증폭 및 감속 활성화! 🔥</div>

        <div id="combo-wrapper" class="hidden">
            <p class="combo-text" id="combo-disp">5 COMBO</p>
        </div>

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

        const bowPos = { x: 200, y: 675 / 2 };

        function initCanvasSize() {
            canvas.width = 1200;
            canvas.height = 675;
            bowPos.x = 200;
            bowPos.y = canvas.height / 2;
            target.x = canvas.width - 150;
        }

        const planets = {
            earth: { name: '지구', gravity: 9.8, bgColor: '#87CEEB', groundColor: '#8B4513' },
            moon: { name: '달', gravity: 1.6, bgColor: '#000000', groundColor: '#808080' },
            mars: { name: '화성', gravity: 3.7, bgColor: '#DAA520', groundColor: '#A0522D' },
            venus: { name: '금성', gravity: 8.9, bgColor: '#F0E68C', groundColor: '#FFD700' },
            europa: { name: '유로파', gravity: 1.3, bgColor: '#B0E0E6', groundColor: '#E0FFFF' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        const totalDuration = 30;
        let timeLeft = 30;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        let buffTimer = 0;
        let isBuffed = false;

        let meteor = { x: 0, y: 0, vx: 0, vy: 0, radius: 45, active: false };

        let target = {
            x: 1200 - 150,
            y: 675 / 2,
            radiusD: 115, radiusC: 84, radiusB: 51, radiusA: 20,  
            speed: 2.5,
            dir: 1,
            visible: true,
            respawnTimer: 0
        };

        let combo = 0;
        let maxCombo = 0;
        let shakeIntensity = 0;
        let particles = [];
        let scoreTexts = [];
        let backgroundElements = []; // Clouds, dust, snow, etc.

        let gravityScale = 0.03;
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        let mousePos = { x: 400, y: 675 / 2 };
        let currentAngle = 0;
        const shootPower = 23;

        let activeArrows = [];
        let currentArrow = { isApple: false, isGiant: false };
        let arrowTrajectoryVisible = true;
        let blinkTimer = 0;

        document.getElementById('main-high-disp').innerText = highScore;
        initCanvasSize();

        function selectPlanet(key) {
            if (gameActive) return;
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`planet-${k}`).classList.remove('active');
            });
            document.getElementById(`planet-${key}`).classList.add('active');
           
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            initBackground();
        }

        function initBackground() {
            backgroundElements = [];
            if (currentPlanetKey === 'earth') {
                for (let i = 0; i < 6; i++) {
                    backgroundElements.push({
                        x: Math.random() * canvas.width,
                        y: 50 + Math.random() * 150,
                        w: 100 + Math.random() * 100,
                        h: 40 + Math.random() * 40,
                        speed: 0.2 + Math.random() * 0.5
                    });
                }
            } else if (currentPlanetKey === 'mars') {
                for (let i = 0; i < 100; i++) {
                    backgroundElements.push({
                        x: Math.random() * canvas.width,
                        y: Math.random() * canvas.height,
                        r: 1 + Math.random() * 2,
                        speedX: (Math.random() - 0.5) * 1,
                        speedY: (Math.random() - 0.5) * 0.5
                    });
                }
            } else if (currentPlanetKey === 'venus') {
                for (let i = 0; i < 80; i++) {
                    backgroundElements.push({
                        x: Math.random() * canvas.width,
                        y: Math.random() * canvas.height,
                        w: 20 + Math.random() * 40,
                        h: 2 + Math.random() * 3,
                        speed: 2 + Math.random() * 4
                    });
                }
            } else if (currentPlanetKey === 'europa') {
                for (let i = 0; i < 150; i++) {
                    backgroundElements.push({
                        x: Math.random() * canvas.width,
                        y: Math.random() * canvas.height,
                        r: 1 + Math.random() * 3,
                        speed: 1 + Math.random() * 2
                    });
                }
            }
        }
        initBackground();

        function startGame() {
            score = 0;
            timeLeft = totalDuration;
            combo = 0;
            maxCombo = 0;
            gameActive = true;
            activeArrows = [];
            particles = [];
            scoreTexts = [];
           
            isBuffed = false;
            buffTimer = 0;
            document.getElementById('buff-alert').classList.add('hidden');
            document.getElementById('time-progress').classList.remove('buffed');

            target.visible = true;
            target.respawnTimer = 0;
            target.speed = 2.5;

            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('ingame-ui').classList.remove('hidden');

            document.getElementById('score-disp').innerText = score;
            updateProgressBar();

            timerInterval = setInterval(() => {
                timeLeft--;
                updateProgressBar();
                if(timeLeft <= 0) endGame();
            }, 1000);

            gameInterval = requestAnimationFrame(gameLoop);
        }

        function updateProgressBar() {
            const bar = document.getElementById('time-progress');
            const percent = (timeLeft / totalDuration) * 100;
            bar.style.width = percent + "%";
        }

        function endGame() {
            gameActive = false;
            clearInterval(timerInterval);
            cancelAnimationFrame(gameInterval);

            document.getElementById('ingame-ui').classList.add('hidden');
            document.getElementById('final-score-disp').innerText = score;
            document.getElementById('final-combo-disp').innerText = maxCombo;

            const titleElement = document.getElementById('result-title-text');
            const msgElement = document.getElementById('highscore-message');

            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('main-high-disp').innerText = highScore;
                titleElement.innerText = "NEW RECORD!";
                titleElement.style.color = "#4cdf50";
                msgElement.innerText = "최고 기록을 경신했습니다!";
            } else {
                titleElement.innerText = "GAME OVER";
                titleElement.style.color = "#ffcc00";
                msgElement.innerText = "";
            }
            document.getElementById('result-screen').classList.remove('hidden');
        }

        function goToMain() {
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('hidden');
        }

        function rollNextArrow() {
            let rand = Math.random();
            if (rand < 0.05) currentArrow = { isApple: false, isGiant: true };
            else if (rand < 0.15) currentArrow = { isApple: true, isGiant: false };
            else currentArrow = { isApple: false, isGiant: false };
        }

        window.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mousePos = {
                x: (e.clientX - rect.left) * (canvas.width / rect.width),
                y: (e.clientY - rect.top) * (canvas.height / rect.height)
            };
            currentAngle = Math.atan2(mousePos.y - bowPos.y, mousePos.x - bowPos.x);
        });

        window.addEventListener('keydown', (e) => {
            if (!gameActive) return;
            if (e.code === 'Space') {
                e.preventDefault();
                let vx = Math.cos(currentAngle) * shootPower;
                let vy = Math.sin(currentAngle) * shootPower;
                if (vx > 0) {
                    activeArrows.push({
                        x: bowPos.x, y: bowPos.y, vx: vx, vy: vy,
                        isApple: currentArrow.isApple, isGiant: currentArrow.isGiant,
                        width: currentArrow.isGiant ? 240 : 95, handled: false
                    });
                    rollNextArrow();
                }
            }
        });

        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 600;
            target.speed = 1.2;
            document.getElementById('buff-alert').classList.remove('hidden');
            document.getElementById('time-progress').classList.add('buffed');
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            target.speed = 2.5;
            document.getElementById('buff-alert').classList.add('hidden');
            document.getElementById('time-progress').classList.remove('buffed');
        }

        function createExplosion(x, y, color) {
            for (let i = 0; i < 15; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 10,
                    vy: (Math.random() - 0.5) * 10,
                    radius: 2 + Math.random() * 4,
                    color: color, alpha: 1, decay: 0.02
                });
            }
        }

        function drawPlanetTarget(ctx, target, key) {
            const skewX = 0.25;
            ctx.save();
            
            // Draw support pole
            ctx.strokeStyle = "#4a5568"; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD); ctx.stroke();

            // Base shadow
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); ctx.fill();

            // Main layers
            const drawLayer = (radius, color) => {
                ctx.fillStyle = color;
                ctx.beginPath(); ctx.ellipse(target.x, target.y, radius * skewX, radius, 0, 0, Math.PI * 2); ctx.fill();
            };

            if (key === 'earth') {
                drawLayer(target.radiusD, "#2980b9"); // Ocean
                // Drawing some land masses
                ctx.fillStyle = "#2ecc71";
                for(let i=0; i<5; i++) {
                    ctx.beginPath();
                    ctx.ellipse(target.x + (Math.sin(i)*10)*skewX, target.y + Math.cos(i)*40, 20*skewX, 30, 0, 0, Math.PI*2);
                    ctx.fill();
                }
            } else if (key === 'moon') {
                drawLayer(target.radiusD, "#bdc3c7");
                ctx.fillStyle = "#7f8c8d";
                for(let i=0; i<8; i++) {
                    ctx.beginPath();
                    ctx.arc(target.x + (Math.cos(i*1.2)*15)*skewX, target.y + Math.sin(i*1.2)*40, 8, 0, Math.PI*2);
                    ctx.fill();
                }
            } else if (key === 'mars') {
                drawLayer(target.radiusD, "#e67e22");
                ctx.fillStyle = "#A0522D";
                for(let i=0; i<10; i++) {
                    ctx.beginPath();
                    ctx.arc(target.x + (Math.random()*40-20)*skewX, target.y + (Math.random()*160-80), 10, 0, Math.PI*2);
                    ctx.fill();
                }
            } else if (key === 'venus') {
                drawLayer(target.radiusD, "#f1c40f");
                ctx.fillStyle = "#B8860B";
                for(let i=0; i<10; i++) {
                    ctx.beginPath();
                    ctx.ellipse(target.x + (Math.random()*30-15)*skewX, target.y + (Math.random()*180-90), 15*skewX, 10, 0, 0, Math.PI*2);
                    ctx.fill();
                }
            } else if (key === 'europa') {
                drawLayer(target.radiusD, "#ecf0f1");
                ctx.strokeStyle = "#3498db"; ctx.lineWidth = 2;
                for(let i=0; i<5; i++) {
                    ctx.beginPath();
                    ctx.moveTo(target.x - 20*skewX, target.y - 80 + i*40);
                    ctx.lineTo(target.x + 20*skewX, target.y - 60 + i*40);
                    ctx.stroke();
                }
            }
            
            // Rings for scoring zones (subtle)
            ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 1;
            [target.radiusC, target.radiusB, target.radiusA].forEach(r => {
                ctx.beginPath(); ctx.ellipse(target.x, target.y, r * skewX, r, 0, 0, Math.PI * 2); ctx.stroke();
            });

            ctx.restore();
        }

        function drawArrowIcon(x, y, angle, isApple, isGiant, width) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);
            
            const headSize = isGiant ? 35 : 15;
            const shaftLen = width;
            
            // Shaft
            ctx.strokeStyle = isGiant ? "#ffcc00" : (isApple ? "#ff4444" : "#e2e8f0");
            ctx.lineWidth = isGiant ? 8 : 3;
            ctx.beginPath(); ctx.moveTo(-shaftLen/2, 0); ctx.lineTo(shaftLen/2, 0); ctx.stroke();
            
            // Head
            ctx.fillStyle = ctx.strokeStyle;
            ctx.beginPath();
            ctx.moveTo(shaftLen/2, 0);
            ctx.lineTo(shaftLen/2 - headSize, -headSize/2);
            ctx.lineTo(shaftLen/2 - headSize, headSize/2);
            ctx.fill();
            
            // Apple
            if (isApple) {
                ctx.fillStyle = "#ff0000";
                ctx.beginPath(); ctx.arc(-shaftLen/2 + 20, -10, 12, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(-shaftLen/2 + 18, -25, 4, 8);
            }
            ctx.restore();
        }

        function gameLoop() {
            if (!gameActive) return;

            // Background
            ctx.fillStyle = planets[currentPlanetKey].bgColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Background Animations
            if (currentPlanetKey === 'earth') {
                backgroundElements.forEach(cloud => {
                    cloud.x += cloud.speed;
                    if (cloud.x > canvas.width) cloud.x = -cloud.w;
                    ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                    ctx.beginPath(); ctx.roundRect(cloud.x, cloud.y, cloud.w, cloud.h, 20); ctx.fill();
                });
            } else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = "rgba(160, 82, 45, 0.3)";
                backgroundElements.forEach(p => {
                    p.x += p.speedX; p.y += p.speedY;
                    if (p.x < 0) p.x = canvas.width; if (p.x > canvas.width) p.x = 0;
                    if (p.y < 0) p.y = canvas.height; if (p.y > canvas.height) p.y = 0;
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                });
            } else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = "rgba(218, 165, 32, 0.4)";
                backgroundElements.forEach(d => {
                    d.x -= d.speed;
                    if (d.x < -d.w) d.x = canvas.width;
                    ctx.fillRect(d.x, d.y, d.w, d.h);
                });
            } else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = "#fff";
                backgroundElements.forEach(s => {
                    s.y += s.speed;
                    if (s.y > canvas.height) s.y = -10;
                    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
                });
            }

            // Ground
            ctx.fillStyle = planets[currentPlanetKey].groundColor;
            if (currentPlanetKey === 'moon') {
                // Bumpy ground
                ctx.beginPath();
                ctx.moveTo(0, canvas.height);
                for(let x=0; x<=canvas.width; x+=40) {
                    ctx.lineTo(x, canvas.height - 60 + Math.sin(x/50)*20);
                }
                ctx.lineTo(canvas.width, canvas.height);
                ctx.fill();
            } else if (currentPlanetKey === 'europa') {
                // Cracked ice
                ctx.fillRect(0, canvas.height - 60, canvas.width, 60);
                ctx.strokeStyle = "rgba(52, 152, 219, 0.5)"; ctx.lineWidth = 2;
                for(let i=0; i<20; i++) {
                    ctx.beginPath(); ctx.moveTo(i*70, canvas.height-60); ctx.lineTo(i*70 + 30, canvas.height); ctx.stroke();
                }
            } else {
                ctx.fillRect(0, canvas.height - 60, canvas.width, 60);
            }

            // Update Target
            if (target.visible) {
                target.y += target.speed * target.dir;
                if (target.y - target.radiusD < 50 || target.y + target.radiusD > canvas.height - 70) target.dir *= -1;
                drawPlanetTarget(ctx, target, currentPlanetKey);
            } else {
                target.respawnTimer--;
                if (target.respawnTimer <= 0) {
                    target.y = 150 + Math.random() * (canvas.height - 300);
                    target.visible = true;
                }
            }

            // Update Arrows
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let a = activeArrows[i];
                a.x += a.vx; a.y += a.vy; a.vy += currentGravity;
                
                let angle = Math.atan2(a.vy, a.vx);
                drawArrowIcon(a.x, a.y, angle, a.isApple, a.isGiant, a.width);

                let tipX = a.x + Math.cos(angle) * (a.width/2);
                let tipY = a.y + Math.sin(angle) * (a.width/2);

                if (tipX > canvas.width || tipY > canvas.height || tipY < 0) {
                    if (!a.handled) { combo = 0; document.getElementById('combo-wrapper').classList.add('hidden'); }
                    activeArrows.splice(i, 1);
                    continue;
                }

                if (target.visible && tipX > target.x - 20 && tipX < target.x + 20) {
                    let dy = Math.abs(tipY - target.y);
                    if (dy < target.radiusD) {
                        a.handled = true; target.visible = false; target.respawnTimer = 40;
                        combo++; maxCombo = Math.max(maxCombo, combo);
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');
                        
                        let pts = dy < target.radiusA ? 10 : (dy < target.radiusB ? 5 : 2);
                        if (a.isApple) pts *= 2; if (a.isGiant) pts *= 3;
                        score += pts + Math.floor(combo/3);
                        document.getElementById('score-disp').innerText = score;
                        createExplosion(tipX, tipY, "#fff");
                        shakeIntensity = 5;
                    }
                }
            }

            // Bow & Trajectory
            ctx.save();
            ctx.translate(bowPos.x, bowPos.y);
            ctx.rotate(currentAngle);
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff"; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); ctx.stroke();
            ctx.restore();
            drawArrowIcon(bowPos.x, bowPos.y, currentAngle, currentArrow.isApple, currentArrow.isGiant, currentArrow.isGiant ? 240 : 95);

            if (arrowTrajectoryVisible) {
                ctx.setLineDash([5, 5]); ctx.strokeStyle = "rgba(255,255,255,0.3)";
                ctx.beginPath();
                let tx = bowPos.x, ty = bowPos.y, tvx = Math.cos(currentAngle)*shootPower, tvy = Math.sin(currentAngle)*shootPower;
                ctx.moveTo(tx, ty);
                for(let i=0; i<50; i++) {
                    tx += tvx; ty += tvy; tvy += currentGravity;
                    ctx.lineTo(tx, ty);
                    if (tx > canvas.width || ty > canvas.height) break;
                }
                ctx.stroke(); ctx.setLineDash([]);
            }

            // Particles
            for(let i=particles.length-1; i>=0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) particles.splice(i, 1);
                else {
                    ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill();
                }
            }
            ctx.globalAlpha = 1;

            gameInterval = requestAnimationFrame(gameLoop);
        }

        selectPlanet('earth');
    </script>
</body>
</html>
"""

components.html(game_html, height=700)
