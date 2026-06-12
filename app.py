import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정 및 여백 제거
st.set_page_config(page_title="Gravity Arrow - Dynamic Universe", layout="wide")
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
    <title>Gravity Arrow - Ultimate</title>
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
            background-color: #000;
            box-shadow: 0 0 35px rgba(0, 0, 0, 0.9), 0 0 5px rgba(255, 255, 255, 0.1);
            overflow: hidden;
            border-radius: 12px;
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
            background: rgba(0, 0, 0, 0.55);
            padding: 12px 25px;
            border-radius: 20px;
            box-sizing: border-box;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.15);
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
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
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

        /* 행성 선택 컨테이너 */
        .main-planet-selector {
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 35px;
            background: rgba(255, 255, 255, 0.05);
            padding: 20px 35px;
            border-radius: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .planet-btn-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }

        .planet-canvas {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: 3px solid transparent;
            transition: all 0.25s ease;
            box-sizing: border-box;
        }

        .planet-btn-wrapper:hover .planet-canvas {
            transform: scale(1.15);
        }

        .planet-btn-wrapper.active .planet-canvas {
            border-color: #ffffff;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.6);
        }

        .planet-label {
            font-size: 0.85rem;
            font-weight: bold;
            color: #a0aec0;
            transition: color 0.25s;
        }

        .planet-btn-wrapper.active .planet-label {
            color: #fff;
            text-shadow: 0 0 8px rgba(255,255,255,0.5);
        }

        #combo-wrapper {
            position: absolute;
            bottom: 140px;
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
            background: rgba(0,0,0,0.6);
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
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 25px;">마우스로 실시간 조준하고 클릭해서 발사하세요!</p>
            
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

        const bowPos = { x: 200, y: (675 - 120) / 2 }; 

        function initCanvasSize() {
            canvas.width = 1200;
            canvas.height = 675;
            bowPos.x = 200; 
            bowPos.y = (canvas.height - 120) / 2;
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
        const totalDuration = 30; 
        let timeLeft = 30;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        let buffTimer = 0; 
        let isBuffed = false;

        let meteor = {
            x: 0, y: 0, vx: 0, vy: 0, radius: 45, active: false, destroyed: false
        };

        let target = {
            x: 1200 - 150,
            y: (675 - 120) / 2,
            baseRadiusD: 115, 
            radiusD: 115, radiusC: 84, radiusB: 51, radiusA: 20,  
            baseSpeed: 2.5,
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

        let gravityScale = 0.03; 
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        let mousePos = { x: 400, y: 675 / 2 };
        let currentAngle = 0;
        const shootPower = 23; 

        let activeArrows = [];
        let currentArrow = { isApple: false, isGiant: false };
        let arrowTrajectoryVisible = true;
        let blinkTimer = 0;

        let envParticles = []; 
        let stars = [];        

        document.getElementById('main-high-disp').innerText = highScore;
        initCanvasSize();

        // 메인 선택화면 행성 고유 디자인 그리기 엔진
        function drawPlanetButtonsVisual() {
            planetKeys.forEach(key => {
                const pCanvas = document.getElementById(`btn-canvas-${key}`);
                if (!pCanvas) return;
                const pCtx = pCanvas.getContext('2d');
                const cx = pCanvas.width / 2;
                const cy = pCanvas.height / 2;
                const r = pCanvas.width / 2 - 2;

                pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
                pCtx.save();
                
                // 원형 클리핑 영역 지정
                pCtx.beginPath();
                pCtx.arc(cx, cy, r, 0, Math.PI * 2);
                pCtx.clip();

                if (key === 'earth') {
                    pCtx.fillStyle = '#2b82c9'; // 파란 바다
                    pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#228b22'; // 초록 대륙
                    pCtx.beginPath();
                    pCtx.arc(cx - 10, cy - 5, 15, 0, Math.PI * 2);
                    pCtx.arc(cx + 12, cy + 10, 12, 0, Math.PI * 2);
                    pCtx.arc(cx - 5, cy + 15, 10, 0, Math.PI * 2);
                    pCtx.fill();
                } 
                else if (key === 'moon') {
                    pCtx.fillStyle = '#bbbbbb'; // 회색 본체
                    pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#666666'; // 크레이터 자국
                    pCtx.beginPath();
                    pCtx.arc(cx - 12, cy - 10, 5, 0, Math.PI * 2);
                    pCtx.arc(cx + 10, cy + 8, 6, 0, Math.PI * 2);
                    pCtx.arc(cx - 2, cy + 12, 3, 0, Math.PI * 2);
                    pCtx.arc(cx + 5, cy - 14, 4, 0, Math.PI * 2);
                    pCtx.fill();
                } 
                else if (key === 'mars') {
                    pCtx.fillStyle = '#e03e1d'; // 주황 본체
                    pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#8b4513'; // 갈색 반점
                    pCtx.beginPath();
                    pCtx.arc(cx - 8, cy - 8, 7, 0, Math.PI * 2);
                    pCtx.arc(cx + 10, cy + 10, 6, 0, Math.PI * 2);
                    pCtx.arc(cx + 2, cy - 12, 4, 0, Math.PI * 2);
                    pCtx.fill();
                } 
                else if (key === 'venus') {
                    pCtx.fillStyle = '#ffd166'; // 노란 본체
                    pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#b8860b'; // 진노란 무늬
                    pCtx.beginPath();
                    pCtx.ellipse(cx, cy - 10, 20, 5, 0, 0, Math.PI * 2);
                    pCtx.ellipse(cx + 5, cy + 8, 16, 4, Math.PI / 12, 0, Math.PI * 2);
                    pCtx.fill();
                } 
                else if (key === 'europa') {
                    pCtx.fillStyle = '#a5cad6'; // 청백색 본체
                    pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.strokeStyle = '#4682b4'; pCtx.lineWidth = 2; // 얼음 금
                    pCtx.beginPath();
                    pCtx.moveTo(cx - 20, cy - 20); pCtx.lineTo(cx + 20, cy + 20);
                    pCtx.moveTo(cx + 20, cy - 15); pCtx.lineTo(cx - 15, cy + 20);
                    pCtx.stroke();
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
            else if (currentPlanetKey === 'europa') count = 90; 

            for (let i = 0; i < count; i++) {
                envParticles.push(createEnvParticle(true));
            }
        }

        function createEnvParticle(randomY = true) {
            let p = {
                x: Math.random() * canvas.width,
                y: randomY ? (Math.random() * (canvas.height - 120)) : (Math.random() * (canvas.height - 120))
            };
            
            if (currentPlanetKey === 'earth') {
                p.w = 110 + Math.random() * 130; 
                p.h = 40 + Math.random() * 35;
                p.vx = 0.2 + Math.random() * 0.4; 
                p.vy = 0;
            } else if (currentPlanetKey === 'mars') {
                p.r = 1.2 + Math.random() * 2.5;
                p.vx = Math.random() * 0.6 - 0.3; 
                p.vy = Math.random() * 0.4 - 0.2;
            } else if (currentPlanetKey === 'venus') {
                p.w = 8 + Math.random() * 25; 
                p.h = 1.5 + Math.random() * 2;
                p.vx = -2.5 - Math.random() * 3.5; 
                p.vy = (Math.random() - 0.5) * 0.3;
            } else if (currentPlanetKey === 'europa') {
                p.r = 1.0 + Math.random() * 2.8;
                p.vx = Math.random() * 0.8 - 0.4; 
                p.vy = 0.8 + Math.random() * 1.5; 
            }
            return p;
        }

        function initStars() {
            stars = [];
            for(let i=0; i<120; i++) {
                stars.push({ x: Math.random() * canvas.width, y: Math.random() * (canvas.height - 120), r: Math.random() * 1.4 });
            }
        }

        function selectPlanet(key) {
            if (gameActive) return; 
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`wrapper-${k}`).classList.remove('active');
            });
            document.getElementById(`wrapper-${key}`).classList.add('active');
            
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            
            initStars();
            initEnvParticles();
        }

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
            resetTargetSpecification(false);

            meteor.active = false;
            meteor.destroyed = false;

            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('ingame-ui').classList.remove('hidden');

            document.getElementById('score-disp').innerText = score;
            updateProgressBar();

            initStars();
            initEnvParticles();

            let targetDirInterval = setInterval(() => {
                if(!gameActive) clearInterval(targetDirInterval);
                target.dir *= -1;
            }, 4500);

            timerInterval = setInterval(() => {
                timeLeft--;
                updateProgressBar();

                if(timeLeft === 15 && !meteor.destroyed) {
                    spawnMeteor();
                }

                if(timeLeft <= 0) {
                    endGame();
                }
            }, 1000);

            gameInterval = requestAnimationFrame(update);
        }

        function updateProgressBar() {
            const bar = document.getElementById('time-progress');
            const percentage = (timeLeft / totalDuration) * 100;
            bar.style.width = `${percentage}%`;
        }

        function spawnMeteor() {
            meteor.x = canvas.width + 50;
            meteor.y = 70; 
            
            let dx = bowPos.x - meteor.x;
            let dy = bowPos.y - meteor.y;
            let distance = Math.hypot(dx, dy);
            
            let slowSpeed = 1.3; 
            meteor.vx = (dx / distance) * slowSpeed;
            meteor.vy = (dy / distance) * slowSpeed;
            meteor.active = true;
        }

        function resetTargetSpecification(buffActive) {
            if(buffActive) {
                target.radiusD = target.baseRadiusD * 1.6; 
                target.radiusC = 84 * 1.6;
                target.radiusB = 51 * 1.6;
                target.radiusA = 20 * 1.6;
                target.speed = target.baseSpeed * 0.4; 
            } else {
                target.radiusD = target.baseRadiusD;
                target.radiusC = 84;
                target.radiusB = 51;
                target.radiusA = 20;
                target.speed = target.baseSpeed;
            }
        }

        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 480; 
            resetTargetSpecification(true);
            document.getElementById('buff-alert').classList.remove('hidden');
            document.getElementById('time-progress').classList.add('buffed');
            shakeIntensity = 12;
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            resetTargetSpecification(false);
            document.getElementById('buff-alert').classList.add('hidden');
            document.getElementById('time-progress').classList.remove('buffed');
        }

        function endGame() {
            gameActive = false;
            cancelAnimationFrame(gameInterval);
            clearInterval(timerInterval);
            
            document.getElementById('ingame-ui').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('buff-alert').classList.add('hidden');

            document.getElementById('final-score-disp').innerText = score;
            document.getElementById('final-combo-disp').innerText = maxCombo;
            const msgElement = document.getElementById('highscore-message');
            const titleElement = document.getElementById('result-title-text');

            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('main-high-disp').innerText = highScore;
                titleElement.innerText = "NEW RECORD!";
                titleElement.style.color = "#4cdf50";
                msgElement.innerText = "축하합니다! 최고 기록을 경신했습니다!";
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
            activeArrows = [];
            particles = [];
            scoreTexts = [];
            initStars();
            initEnvParticles();
            drawPlanetButtonsVisual();
        }

        function rollNextArrow() {
            let rand = Math.random();
            if (rand < 0.03) { 
                currentArrow = { isApple: false, isGiant: true };
            } else if (rand < 0.09) { 
                currentArrow = { isApple: true, isGiant: false };
            } else {
                currentArrow = { isApple: false, isGiant: false };
            }
            blinkTimer = 0;
            arrowTrajectoryVisible = true;
        }
        rollNextArrow();

        function createExplosion(x, y, color, customCount) {
            let count = customCount || 15; 
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = 1 + Math.random() * 5;
                particles.push({
                    x: x, y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: 2 + Math.random() * 4,
                    color: color,
                    alpha: 1,
                    decay: 0.015 + Math.random() * 0.02
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -0.8 });
        }

        function getCanvasMousePos(e) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: (e.clientX - rect.left) * (canvas.width / rect.width),
                y: (e.clientY - rect.top) * (canvas.height / rect.height)
            };
        }

        // 실시간 마우스 움직임을 통한 각도 반영 조정
        window.addEventListener('mousemove', (e) => {
            mousePos = getCanvasMousePos(e);
            currentAngle = Math.atan2(mousePos.y - bowPos.y, mousePos.x - bowPos.x);
        });

        // 원래의 마우스 클릭 발사 시스템으로 복구 통합 완료
        window.addEventListener('mousedown', (e) => {
            if (!gameActive) return;
            
            // 인게임 영역 내부 클릭 시에만 발사
            let clickedPos = getCanvasMousePos(e);
            if (clickedPos.x >= 0 && clickedPos.x <= canvas.width && clickedPos.y >= 0 && clickedPos.y <= canvas.height) {
                let vx = Math.cos(currentAngle) * shootPower;
                let vy = Math.sin(currentAngle) * shootPower;

                if (vx > 0) {
                    let aWidth = currentArrow.isGiant ? 240 : 95;
                    activeArrows.push({
                        x: bowPos.x, y: bowPos.y,
                        vx: vx, vy: vy,
                        isApple: currentArrow.isApple,
                        isGiant: currentArrow.isGiant,
                        width: aWidth, height: 5,
                        collided: false,
                        handled: false 
                    });
                    rollNextArrow(); 
                }
            }
        });

        // 초기 실행 세팅
        drawPlanetButtonsVisual();
        initStars();
        initEnvParticles();

        function update() {
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            if (gameActive) {
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 40 || target.y + target.radiusD > canvas.height - 135) {
                        target.dir *= -1; 
                    }
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 80 + Math.random() * (canvas.height - 240);
                        target.visible = true;
                    }
                }

                if(currentArrow.isApple || currentArrow.isGiant) {
                    blinkTimer++;
                    if(blinkTimer % 45 === 0) {
                        arrowTrajectoryVisible = !arrowTrajectoryVisible;
                    }
                }

                if(meteor.active) {
                    meteor.x += meteor.vx;
                    meteor.y += meteor.vy;

                    if(meteor.x < bowPos.x - 20) {
                        meteor.active = false;
                        createExplosion(meteor.x, meteor.y, "#94a3b8", 30);
                        shakeIntensity = 10;
                    }
                }
            }

            // 렌더링 시작
            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // -------------------------------------------------------------
            // [1단계: 요청 동적 배경 및 기상 환경 렌더링]
            // -------------------------------------------------------------
            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB'; 
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505'; 
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#cda365'; 
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#dcb858'; 
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#b0e0e6'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.48)";
                stars.forEach(s => {
                    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
                });
            }

            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;

                if (currentPlanetKey === 'venus' && p.x < -p.w) {
                    p.x = canvas.width + p.w; p.y = Math.random() * (canvas.height - 120);
                } else if (p.x > canvas.width + 120) {
                    p.x = -120; p.y = Math.random() * (canvas.height - 120);
                } else if (p.x < -120) {
                    p.x = canvas.width + 120; p.y = Math.random() * (canvas.height - 120);
                }
                if (p.y > canvas.height - 120) {
                    p.y = -10; p.x = Math.random() * canvas.width;
                }

                if (currentPlanetKey === 'earth') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
                    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.w/2, p.h/2, 0, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x - p.w/4, p.y - p.h/3, p.h/1.4, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x + p.w/4, p.y - p.h/4, p.h/1.7, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = 'rgba(160, 82, 45, 0.45)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = 'rgba(150, 105, 15, 0.55)'; 
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.88)'; 
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.05)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // -------------------------------------------------------------
            // [2단계: 요청된 하단 지형 디자인]
            // -------------------------------------------------------------
            let groundHeight = 120;
            let gY = canvas.height - groundHeight;

            if (currentPlanetKey === 'earth') {
                ctx.fillStyle = '#654321'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
                ctx.fillStyle = '#228b22'; 
                ctx.fillRect(0, gY, canvas.width, 16);
            }
            else if (currentPlanetKey === 'moon') {
                ctx.fillStyle = '#444444'; 
                ctx.beginPath();
                ctx.moveTo(0, gY);
                for(let i=0; i<=canvas.width; i+=40) {
                    ctx.lineTo(i, gY + Math.sin(i * 0.025) * 16);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = '#8b4513'; 
                ctx.beginPath();
                ctx.moveTo(0, gY);
                for(let i=0; i<=canvas.width; i+=50) {
                    ctx.lineTo(i, gY + Math.cos(i * 0.02) * 22);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = '#b8860b'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
            }
            else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = '#e0ffff'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
                
                ctx.strokeStyle = '#87cefa'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(90, gY); ctx.lineTo(160, canvas.height - 50); ctx.lineTo(240, canvas.height - 15); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(430, gY); ctx.lineTo(390, canvas.height - 40); ctx.lineTo(490, canvas.height - 5); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(850, gY); ctx.lineTo(920, canvas.height - 60); ctx.lineTo(890, canvas.height - 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(canvas.width - 150, gY); ctx.lineTo(canvas.width - 90, canvas.height - 45); ctx.stroke();
            }

            // -------------------------------------------------------------
            // [3단계: 과녁 행성 자체 비주얼 디테일 커스텀화]
            // -------------------------------------------------------------
            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "rgba(40, 50, 70, 0.5)"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD); ctx.stroke();

                ctx.fillStyle = "rgba(0, 0, 0, 0.35)";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 4) * skewX, target.radiusD + 4, 0, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
                
                ctx.save();
                ctx.beginPath();
                ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2);
                ctx.clip(); 

                if (currentPlanetKey === 'earth') {
                    ctx.fillStyle = '#2b82c9'; 
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#228b22'; 
                    ctx.beginPath();
                    ctx.ellipse(target.x - 10, target.y - 20, 25, 45, Math.PI/6, 0, Math.PI*2);
                    ctx.ellipse(target.x + 20, target.y + 30, 20, 35, -Math.PI/4, 0, Math.PI*2);
                    ctx.ellipse(target.x - 15, target.y + 50, 15, 20, 0, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'moon') {
                    ctx.fillStyle = '#bbbbbb';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#555555'; 
                    ctx.beginPath();
                    ctx.arc(target.x - 12, target.y - 30, 14, 0, Math.PI*2);
                    ctx.arc(target.x + 15, target.y + 10, 18, 0, Math.PI*2);
                    ctx.arc(target.x - 8, target.y + 40, 10, 0, Math.PI*2);
                    ctx.arc(target.x + 8, target.y - 55, 9, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = '#e03e1d';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#8b4513';
                    ctx.beginPath();
                    ctx.ellipse(target.x - 15, target.y - 15, 16, 25, Math.PI/3, 0, Math.PI*2);
                    ctx.ellipse(target.x + 18, target.y + 35, 12, 20, -Math.PI/6, 0, Math.PI*2);
                    ctx.arc(target.x - 5, target.y + 55, 11, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = '#ffd166';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#b8860b';
                    ctx.beginPath();
                    ctx.ellipse(target.x - 5, target.y - 40, 25, 12, 0, 0, Math.PI*2);
                    ctx.ellipse(target.x + 10, target.y + 15, 22, 10, Math.PI/12, 0, Math.PI*2);
                    ctx.ellipse(target.x - 12, target.y + 45, 18, 9, -Math.PI/8, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = '#a5cad6';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.strokeStyle = '#4682b4'; ctx.lineWidth = 2.5;
                    ctx.beginPath();
                    ctx.moveTo(target.x - 30, target.y - 80); ctx.lineTo(target.x + 30, target.y + 80);
                    ctx.moveTo(target.x + 40, target.y - 50); ctx.lineTo(target.x - 40, target.y + 60);
                    ctx.stroke();
                }
                ctx.restore();

                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            if(meteor.active) {
                ctx.save();
                ctx.fillStyle = "rgba(239, 68, 68, 0.25)";
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius + 12 + Math.random()*6, 0, Math.PI*2); ctx.fill();

                let grad = ctx.createRadialGradient(meteor.x - 10, meteor.y - 10, 5, meteor.x, meteor.y, meteor.radius);
                grad.addColorStop(0, '#ff9e00'); grad.addColorStop(0.6, '#d946ef'); grad.addColorStop(1, '#450a0a');
                ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ff0055"; ctx.lineWidth = 3; ctx.stroke();
                ctx.restore();
            }

            ctx.save();
            ctx.translate(bowPos.x, bowPos.y);
            ctx.rotate(currentAngle);
            
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 6; 
            ctx.beginPath();
            ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.45)";
            ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-15, 65); ctx.stroke();
            ctx.restore();

            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, currentArrow.isApple, currentArrow.isGiant, currentArrow.isGiant ? 240 : 95);
            }

            if (arrowTrajectoryVisible && gameActive) {
                let tVx = Math.cos(currentAngle) * shootPower;
                if (tVx > 0) { 
                    ctx.save();
                    if(currentArrow.isGiant) {
                        ctx.strokeStyle = "rgba(255, 204, 0, 0.75)";
                        ctx.lineWidth = 5.5;
                    } else {
                        ctx.strokeStyle = currentArrow.isApple ? "#ff2222" : "rgba(255, 255, 255, 0.6)";
                        ctx.lineWidth = 2.5;
                    }
                    ctx.setLineDash([6, 6]);
                    ctx.beginPath();

                    let tX = bowPos.x; let tY = bowPos.y;
                    let tVy = Math.sin(currentAngle) * shootPower;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                }
            }

            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.isGiant, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                if (arrow.x > canvas.width + 150 || arrow.y > canvas.height + 150 || arrow.y < -150) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + (arrow.isGiant ? 30 : 10)) {
                        meteor.active = false;
                        meteor.destroyed = true;
                        activeArrows.splice(i, 1); 

                        createExplosion(meteor.x, meteor.y, "#ffcc00", 50);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        
                        activateAbilityBuff();
                        continue;
                    }
                }

                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + (arrow.isGiant ? 40 : 15) && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        target.visible = false;
                        target.respawnTimer = 45; 

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = 0;
                        let hColor = "#ffffff";
                        let targetColor = planets[currentPlanetKey].color;
                        
                        if (dy <= target.radiusA) { earnedPoints = 10; hColor = "#ffcc00"; }
                        else if (dy <= target.radiusB) { earnedPoints = 5;  hColor = "#ff3e3e"; }
                        else if (dy <= target.radiusC) { earnedPoints = 2;  hColor = targetColor; }
                        else { earnedPoints = 1;  hColor = "#e2e8f0"; }

                        if(arrow.isApple) { earnedPoints *= 2; hColor = "#ff2222"; }
                        else if(arrow.isGiant) { earnedPoints *= 3; hColor = "#ffcc00"; }

                        let totalEarned = earnedPoints + Math.floor(combo / 3);
                        score += totalEarned;
                        document.getElementById('score-disp').innerText = score;

                        createScoreText(arrowTipX - 25, arrowTipY - 15, `+${totalEarned}`, hColor);
                        
                        shakeIntensity = arrow.isGiant ? 22 : 7; 
                        createExplosion(arrowTipX, arrowTipY, hColor, arrow.isGiant ? 50 : 20);

                        activeArrows.splice(i, 1); 
                        continue;
                    }
                }
            }

            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 22px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            gameInterval = requestAnimationFrame(update);
        }

        function drawArrowIcon(x, y, angle, isApple, isGiant, customWidth) {
            ctx.save();
            ctx.translate(x, y); ctx.rotate(angle);
            let width = customWidth || 95; 
            
            if (isGiant) {
                ctx.strokeStyle = "#ffcc00";
                ctx.lineWidth = 11; 
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); ctx.stroke();

                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2 - 35, -20); ctx.lineTo(width/2 - 35, 20); ctx.closePath(); ctx.fill();

                ctx.fillStyle = "#e3a857";
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(-width/2 - 20, -22); ctx.lineTo(-width/2 + 10, -22); ctx.lineTo(-width/2 + 25, 0); ctx.lineTo(-width/2 + 10, 22); ctx.lineTo(-width/2 - 20, 22); ctx.closePath(); ctx.fill();
            } else {
                ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
                ctx.lineWidth = isApple ? 5.5 : 4.5; 
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); stroke();

                ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
                ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2 - 15, -8); ctx.lineTo(width/2 - 15, 8); ctx.closePath(); ctx.fill();

                ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(-width/2 - 8, -10); ctx.lineTo(-width/2 + 5, -10); ctx.lineTo(-width/2 + 12, 0); ctx.lineTo(-width/2 + 5, 10); ctx.lineTo(-width/2 - 8, 10); ctx.closePath(); ctx.fill();

                if(isApple) {
                    ctx.fillStyle = "#fa5252"; ctx.beginPath(); ctx.arc(0, -4, 11, 0, Math.PI*2); ctx.fill();
                    ctx.strokeStyle = "#868e96"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, -14); ctx.quadraticCurveTo(3, -19, 6, -17); ctx.stroke();
                }
            }
            ctx.restore();
        }

        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=720, scrolling=False)
