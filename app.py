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
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 25px;">활을 클릭하고 뒤로 당겼다 놓으세요! (앵그리버드 방식 조준)</p>
           
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

        let meteor = { x: 0, y: 0, vx: 0, vy: 0, radius: 45, active: false, destroyed: false, rotation: 0, rotSpeed: 0.02 };

        let target = {
            x: 1200 - 150, y: (675 - 120) / 2, radiusD: 115, radiusC: 84, radiusB: 51, radiusA: 20,  
            speed: 2.5, dir: 1, visible: true, respawnTimer: 0
        };

        let combo = 0; let maxCombo = 0; let shakeIntensity = 0;
        let particles = []; let scoreTexts = [];
        let gravityScale = 0.03; let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 드래그 조준 전용 변수 (기본 수평선 상태 0도 초기화)
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

        // 1. 요청에 따른 행성 아이콘 캔버스 렌더링 함수
        function drawPlanetButtonsVisual() {
            planetKeys.forEach(key => {
                const pCanvas = document.getElementById(`btn-canvas-${key}`);
                if (!pCanvas) return;
                const pCtx = pCanvas.getContext('2d');
                const cx = pCanvas.width / 2; const cy = pCanvas.height / 2; const r = pCanvas.width / 2 - 2;
                pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
                pCtx.save(); pCtx.beginPath(); pCtx.arc(cx, cy, r, 0, Math.PI * 2); pCtx.clip();

                if (key === 'earth') {
                    // 지구: 초록색 육지와 파란색 바다
                    pCtx.fillStyle = '#2b82c9'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#228b22';
                    pCtx.beginPath(); pCtx.arc(cx - 12, cy - 8, 14, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 10, cy + 10, 16, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 12, cy - 12, 10, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'moon') {
                    // 달: 회색깔에 검은색 자국들
                    pCtx.fillStyle = '#aaaaaa'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#444444';
                    pCtx.beginPath(); pCtx.arc(cx - 12, cy - 10, 6, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 8, cy - 6, 4, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx - 2, cy + 12, 7, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'mars') {
                    // 화성: 주황색에 갈색 반점
                    pCtx.fillStyle = '#e03e1d'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#8b4513';
                    pCtx.beginPath(); pCtx.arc(cx - 8, cy - 8, 8, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 12, cy + 8, 6, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'venus') {
                    // 금성: 노란색에 진노란색 반점
                    pCtx.fillStyle = '#ffd166'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.fillStyle = '#b8860b';
                    pCtx.beginPath(); pCtx.arc(cx - 10, cy + 5, 7, 0, Math.PI * 2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(cx + 8, cy - 10, 9, 0, Math.PI * 2); pCtx.fill();
                } else if (key === 'europa') {
                    // 유로파: 청백색 그대로
                    pCtx.fillStyle = '#b0e0e6'; pCtx.fillRect(0, 0, pCanvas.width, pCanvas.height);
                    pCtx.strokeStyle = '#5f9ea0'; pCtx.lineWidth = 2;
                    pCtx.beginPath(); pCtx.moveTo(cx - 20, cy - 15); pCtx.lineTo(cx + 15, cy + 20); pCtx.stroke();
                    pCtx.beginPath(); pCtx.moveTo(cx + 15, cy - 18); pCtx.lineTo(cx - 15, cy + 15); pCtx.stroke();
                }
                pCtx.restore();
            });
        }

        // 행성별 배경 전용 고유 환경 파티클 데이터 정의
        function initEnvParticles() {
            envParticles = [];
            let count = 0;
            if (currentPlanetKey === 'earth') count = 8;        // 구름 형태
            else if (currentPlanetKey === 'mars') count = 40;   // 노란 미세 먼지
            else if (currentPlanetKey === 'venus') count = 65;  // 오른쪽 -> 왼쪽 먼지 폭풍
            else if (currentPlanetKey === 'europa') count = 100; // 눈송이 효과

            for (let i = 0; i < count; i++) envParticles.push(createEnvParticle(true));
        }

        function createEnvParticle(randomY = true) {
            let p = { x: Math.random() * canvas.width, y: randomY ? Math.random() * (canvas.height - 120) : 0 };
            if (currentPlanetKey === 'earth') {
                p.w = 110 + Math.random() * 130; p.h = 45 + Math.random() * 35; p.vx = 0.2 + Math.random() * 0.4; p.vy = 0;
            } else if (currentPlanetKey === 'mars') {
                p.r = 1.5 + Math.random() * 2.5; p.vx = Math.random() * 0.4 - 0.2; p.vy = Math.random() * 0.3 - 0.15;
            } else if (currentPlanetKey === 'venus') {
                // 금성: 무조건 오른쪽에서 시작해서 왼쪽으로 빠르게 흐름
                p.x = Math.random() * canvas.width;
                p.w = 8 + Math.random() * 25; p.h = 2 + Math.random() * 2.5;
                p.vx = -3.0 - Math.random() * 4.0; p.vy = (Math.random() - 0.5) * 0.3;
            } else if (currentPlanetKey === 'europa') {
                p.r = 1.2 + Math.random() * 3.0; p.vx = Math.random() * 0.8 - 0.4; p.vy = 1.0 + Math.random() * 2.0;
            }
            return p;
        }

        function initStars() {
            stars = [];
            for(let i=0; i<120; i++) stars.push({ x: Math.random() * canvas.width, y: Math.random() * (canvas.height - 120), r: Math.random() * 1.5 });
        }

        function selectPlanet(key) {
            if (gameActive) return;
            currentPlanetKey = key;
            planetKeys.forEach(k => document.getElementById(`wrapper-${k}`).classList.remove('active'));
            document.getElementById(`wrapper-${key}`).classList.add('active');
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            currentAngle = 0; // 초기 각도화
            initStars(); initEnvParticles();
        }

        function startGame() {
            score = 0; timeLeft = totalDuration; combo = 0; maxCombo = 0; gameActive = true;
            activeArrows = []; particles = []; scoreTexts = []; currentAngle = 0;
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
            activeArrows = []; particles = []; scoreTexts = []; currentAngle = 0;
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

        // [핵심 변경] 활을 클릭 후 앵그리버드처럼 마우스 드래그 반대 방향으로 각도를 조절하는 리스너
        window.addEventListener('mousedown', (e) => {
            if (!gameActive) return;
            let pos = getCanvasMousePos(e);
            if (pos.x >= 0 && pos.x <= canvas.width && pos.y >= 0 && pos.y <= canvas.height) {
                // 활의 중심점을 감지하거나 클릭했을 때 작동
                if (Math.hypot(pos.x - bowPos.x, pos.y - bowPos.y) < 140) {
                    isDragging = true;
                    dragStart = { x: bowPos.x, y: bowPos.y }; // 활 위치 기준
                    dragCurrent = { x: pos.x, y: pos.y };
                    arrowTrajectoryVisible = true;
                }
            }
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return; // 드래그가 아닐 때는 마우스포인터를 절대 쳐다보지 않음
            let pos = getCanvasMousePos(e);
            dragCurrent = { x: pos.x, y: pos.y };
           
            // 앵그리버드 방식 조준: 마우스를 당긴 반대 방향 벡터 계산
            let dx = dragStart.x - dragCurrent.x;
            let dy = dragStart.y - dragCurrent.y;
            currentAngle = Math.atan2(dy, dx);
           
            let dist = Math.hypot(dx, dy);
            dynamicPower = Math.min(dist / maxDragDist, 1.0) * 23;
        });

        window.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;
            arrowTrajectoryVisible = false;

            if (dynamicPower > 3) {
                let vx = Math.cos(currentAngle) * dynamicPower;
                let vy = Math.sin(currentAngle) * dynamicPower;

                if (vx > 0) { // 오른쪽 방향 사격만 유효화
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

            // 2. 요청대로 정교하게 수정한 행성별 배경 그래픽 시스템 구현
            if (currentPlanetKey === 'earth') {
                ctx.fillStyle = '#87CEEB'; // 지구: 하늘색 배경
            } else if (currentPlanetKey === 'moon') {
                ctx.fillStyle = '#050505'; // 달: 검은색 배경
            } else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = '#f0d399'; // 화성: 뿌연 노란색 하늘 배경
            } else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = '#cca43b'; // 금성: 약간 흐려진 먼지 진노란색 배경
            } else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = '#b0e0e6'; // 유로파: 뿌연 하늘색 배경
            }
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 우주 별자리 그리기 (달, 지구 하늘만)
            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.5)";
                stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill(); });
            }

            // 행성별 특수 날씨 파티클 렌더링 시스템
            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
               
                if (currentPlanetKey === 'venus') {
                    // 오른쪽 -> 왼쪽 먼지바람 루프 처리
                    if (p.x < -40) { p.x = canvas.width + 40; p.y = Math.random() * (canvas.height - 120); }
                } else if (currentPlanetKey === 'europa') {
                    // 상단 -> 하단 눈 내림 지속 처리
                    if (p.y > canvas.height - 120) { p.y = 0; p.x = Math.random() * canvas.width; }
                } else {
                    if (p.x > canvas.width + 150) p.x = -150;
                }

                if (currentPlanetKey === 'earth') {
                    // 하늘에 구름 렌더링
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.65)';
                    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.w/2, p.h/2, 0, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x - p.w/4, p.y - p.h/4, p.h/1.4, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'mars') {
                    // 뿌연 황사 먼지 조금 효과
                    ctx.fillStyle = 'rgba(139, 69, 19, 0.35)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    // 가로로 길게 흐르는 진노란색 먼지바람
                    ctx.fillStyle = 'rgba(184, 134, 11, 0.45)';
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    // 지속적으로 계속 내리는 눈 효과
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            // 3. 요청에 따른 하단 행성별 독창적 지형 바닥(Ground) 렌더링
            let groundHeight = 120; let gY = canvas.height - groundHeight;
           
            if (currentPlanetKey === 'earth') {
                // 지구: 갈색 땅에 녹색 잔디 한 줄
                ctx.fillStyle = '#654321'; ctx.fillRect(0, gY, canvas.width, groundHeight);
                ctx.fillStyle = '#228b22'; ctx.fillRect(0, gY, canvas.width, 15);
            } else if (currentPlanetKey === 'moon') {
                // 달: 울퉁불퉁한 표면의 회색 땅
                ctx.fillStyle = '#555555'; ctx.beginPath();
                ctx.moveTo(0, gY);
                for(let i=0; i<=canvas.width; i+=40) {
                    ctx.lineTo(i, gY + Math.sin(i * 0.03) * 15);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            } else if (currentPlanetKey === 'mars') {
                // 화성: 갈색 바닥 지형
                ctx.fillStyle = '#8b4513'; ctx.fillRect(0, gY, canvas.width, groundHeight);
            } else if (currentPlanetKey === 'venus') {
                // 금성: 노란색 바닥 지형
                ctx.fillStyle = '#dcb858'; ctx.fillRect(0, gY, canvas.width, groundHeight);
            } else if (currentPlanetKey === 'europa') {
                // 유로파: 금이 가 있는 푸르스름한 빙판 바닥
                ctx.fillStyle = '#e0ffff'; ctx.fillRect(0, gY, canvas.width, groundHeight);
                ctx.strokeStyle = '#87cefa'; ctx.lineWidth = 3;
               
                ctx.beginPath(); ctx.moveTo(150, gY); ctx.lineTo(210, gY + 50); ctx.lineTo(340, canvas.height - 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(550, gY); ctx.lineTo(510, gY + 60); ctx.lineTo(620, canvas.height - 20); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(900, gY); ctx.lineTo(980, gY + 45); ctx.lineTo(1050, canvas.height); ctx.stroke();
            }

            // 운석 렌더링
            if(meteor.active) {
                ctx.save();
                let tailGrad = ctx.createLinearGradient(meteor.x, meteor.y, meteor.x + 80, meteor.y - 30);
                tailGrad.addColorStop(0, "rgba(239, 68, 68, 0.8)");
                tailGrad.addColorStop(1, "rgba(239, 68, 68, 0)");
                ctx.fillStyle = tailGrad; ctx.beginPath();
                ctx.moveTo(meteor.x, meteor.y - meteor.radius); ctx.lineTo(meteor.x + 90, meteor.y - 35); ctx.lineTo(meteor.x + 35, meteor.y + meteor.radius);
                ctx.closePath(); ctx.fill();

                ctx.translate(meteor.x, meteor.y); ctx.rotate(meteor.rotation);
                ctx.fillStyle = '#44403c'; ctx.beginPath(); ctx.arc(0, 0, meteor.radius, 0, Math.PI*2); ctx.fill();
                ctx.restore();
            }

            // 움직이는 리얼 과녁 과녁 시스템
            const skewX = 0.25;
            const frontX = target.x - (target.radiusD * skewX); const backX = target.x + (target.radiusD * skewX);

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "rgba(40, 50, 70, 0.4)"; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD); ctx.stroke();
                ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ff3e3e"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = "#ffcc00"; ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // 활 고무줄 구조 비주얼 드로우
            ctx.save(); ctx.translate(bowPos.x, bowPos.y); ctx.rotate(currentAngle);
            ctx.strokeStyle = "#00d2ff"; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); ctx.stroke();
           
            if(isDragging) {
                ctx.strokeStyle = "rgba(255,255,255,0.8)"; ctx.lineWidth = 2.5;
                ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-dynamicPower*3.5, 0); ctx.lineTo(-15, 65); ctx.stroke();
            } else {
                ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-15, 65); ctx.stroke();
            }
            ctx.restore();

            // 대기중 화살 드로우
            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, 95);
            }

            // 포물선 조준선 예측선 드로우
            if (arrowTrajectoryVisible && gameActive && dynamicPower > 3) {
                let tVx = Math.cos(currentAngle) * dynamicPower;
                if (tVx > 0) {
                    ctx.save();
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
                    ctx.lineWidth = 2.5; ctx.setLineDash([6, 5]); ctx.beginPath();
                    let tX = bowPos.x; let tY = bowPos.y; let tVy = Math.sin(currentAngle) * dynamicPower;
                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                }
            }

            // 발사된 투사체들의 역학 연산 시뮬레이션
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
                        createExplosion(meteor.x, meteor.y, "#ef4444", 30); score += 15;
                        document.getElementById('score-disp').innerText = score;
                        createScoreText(meteor.x, meteor.y, "+15 Meteor Clear!", "#ef4444"); continue;
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

            // 이펙트 연산 루프
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
