import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정 (여백 제거)
st.set_page_config(page_title="Gravity Arrow", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding: 0; }
    iframe { display: block; width: 100vw; height: 98vh; border: none; }
    body { margin: 0; }
    </style>
    """,
    unsafe_allow_html=True
)

# 게임 전체 HTML/CSS/JavaScript 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        /* 화면 전체를 가득 채우는 풀스크린 스타일 */
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: radial-gradient(circle, #161f2b 0%, #050608 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
        }

        #game-wrapper {
            position: relative;
            width: 100vw;
            height: 100vh;
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

        /* 화면 오버레이 (시작 및 결과 화면) */
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
            background: rgba(5, 6, 8, 0.85);
            z-index: 10;
            transition: all 0.3s ease;
        }

        .hidden {
            display: none !important;
        }

        h1 {
            font-size: 4rem;
            margin: 10px 0;
            text-shadow: 0 0 20px #00d2ff;
            font-weight: 800;
            letter-spacing: 3px;
        }

        .result-title {
            font-size: 3.5rem;
            color: #ffcc00;
            text-shadow: 0 0 15px #ffcc00;
            margin-bottom: 20px;
        }

        .score-report {
            font-size: 2rem;
            margin-bottom: 30px;
            text-align: center;
            line-height: 1.6;
        }

        /* 상단 UI 패널 */
        .ui-panel {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 90%;
            max-width: 1400px;
            background: rgba(255, 255, 255, 0.07);
            padding: 15px 30px;
            border-radius: 50px;
            box-sizing: border-box;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 5;
        }

        .stats {
            font-size: 1.3rem;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 15px 35px;
            font-size: 1.4rem;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 20px rgba(0, 102, 255, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 132, 255, 0.6);
        }

        .planet-selector {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .planet-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000;
        }

        .planet-circle:hover {
            transform: scale(1.15);
        }

        .planet-circle.active {
            border-color: #fff;
            box-shadow: 0 0 18px currentColor;
        }

        #planet-earth { background: radial-gradient(circle at 30% 30%, #2b82c9, #053057); color: #00d2ff; }
        #planet-moon { background: radial-gradient(circle at 30% 30%, #ccc, #666); color: #ddd; }
        #planet-mars { background: radial-gradient(circle at 30% 30%, #e03e1d, #5c1303); color: #ff6b6b; }
        #planet-venus { background: radial-gradient(circle at 30% 30%, #e3a857, #6d3e00); color: #ffd166; }
        #planet-europa { background: radial-gradient(circle at 30% 30%, #a5cad6, #3a5d6b); color: #98e1f5; }

        /* 화면 하단 콤보 표시기 */
        #combo-wrapper {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
            text-align: center;
            pointer-events: none;
            transition: all 0.1s ease;
        }
        
        .combo-text {
            font-size: 3rem;
            font-weight: 900;
            font-style: italic;
            color: #ff3e3e;
            text-shadow: 0 0 10px rgba(255, 62, 62, 0.8), 0 0 20px rgba(255, 200, 0, 0.5);
            margin: 0;
            animation: pulse 0.2s ease-in-out alternate;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.2); }
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div class="ui-panel">
            <div class="stats">
                시간: <span id="time-disp">30</span>s | 
                중력: <span id="gravity-disp">9.8</span> m/s² | 
                점수: <span id="score-disp">0</span> | 
                최고기록: <span id="high-disp">0</span>
            </div>
            
            <div class="planet-selector" id="planet-selector-bar">
                <div id="planet-earth" class="planet-circle active" onclick="selectPlanet('earth')">지구</div>
                <div id="planet-moon" class="planet-circle" onclick="selectPlanet('moon')">달</div>
                <div id="planet-mars" class="planet-circle" onclick="selectPlanet('mars')">화성</div>
                <div id="planet-venus" class="planet-circle" style="font-size: 0.65rem;" onclick="selectPlanet('venus')">금성</div>
                <div id="planet-europa" class="planet-circle" onclick="selectPlanet('europa')">유로파</div>
            </div>
        </div>

        <div id="combo-wrapper" class="hidden">
            <p class="combo-text" id="combo-disp">5 COMBO</p>
        </div>

        <div id="start-screen" class="screen-overlay">
            <h1 style="margin-top: 80px;">Gravity Arrow</h1>
            <p style="font-size: 1.3rem; color: #a0aec0; margin-bottom: 40px;">왼쪽에서 활을 당겨 오른쪽의 움직이는 과녁을 맞추세요!</p>
            <button class="btn" onclick="startGame()">Start Game</button>
        </div>

        <div id="result-screen" class="screen-overlay hidden">
            <div class="result-title" id="result-title-text">GAME OVER</div>
            <div class="score-report">
                최종 점수: <span id="final-score-disp" style="color: #00d2ff; font-weight: bold;">0</span> 점<br>
                최대 콤보: <span id="final-combo-disp" style="color: #ff3e3e; font-weight: bold;">0</span> 콤보<br>
                <span id="highscore-message" style="font-size: 1.4rem; color: #4cdf50;"></span>
            </div>
            <button class="btn" onclick="backToMain()">다시 하기</button>
        </div>

        <canvas id="game-canvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');

        // 반응형 전면 스크린 해상도 설정 함수
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            // [위치 변경] 활은 왼쪽, 과녁은 오른쪽 배치
            bowPos.x = 100; 
            bowPos.y = canvas.height / 2;
            target.x = canvas.width - 120; 
        }

        // 행성 데이터
        const planets = {
            earth: { name: '지구', gravity: 9.8, color: '#2b82c9' },
            moon: { name: '달', gravity: 1.6, color: '#ccc' },
            mars: { name: '화성', gravity: 3.7, color: '#e03e1d' },
            venus: { name: '금성', gravity: 8.9, color: '#e3a857' },
            europa: { name: '유로파', gravity: 1.3, color: '#a5cad6' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        // 게임 제어 변수
        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        let timeLeft = 30;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        // 콤보 및 이펙트 변수
        let combo = 0;
        let maxCombo = 0;
        let shakeIntensity = 0;
        let particles = [];
        let scoreTexts = [];

        let gravityScale = 0.03; 
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 과녁 변수 (반경 설정)
        let target = {
            x: window.innerWidth - 120,
            y: window.innerHeight / 2,
            radiusD: 55, 
            radiusC: 40, 
            radiusB: 25, 
            radiusA: 10,  
            speed: 2.3,
            dir: 1
        };
        
        // 활 및 화살 변수 (왼쪽 배치)
        const bowPos = { x: 100, y: window.innerHeight / 2 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };
        
        let activeArrows = [];
        let currentArrow = { isApple: false };
        
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        document.getElementById('high-disp').innerText = highScore;
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        function selectPlanet(key) {
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`planet-${k}`).classList.remove('active');
            });
            document.getElementById(`planet-${key}`).classList.add('active');
            
            document.getElementById('gravity-disp').innerText = planets[key].gravity.toFixed(1);
            currentGravity = planets[key].gravity * gravityScale;
            
            generateStars(); 
        }

        function startGame() {
            if(gameActive) return;
            score = 0;
            timeLeft = 30; 
            combo = 0;
            maxCombo = 0;
            gameActive = true;
            activeArrows = [];
            particles = [];
            scoreTexts = [];

            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');

            document.getElementById('score-disp').innerText = score;
            document.getElementById('time-disp').innerText = timeLeft;

            let targetDirInterval = setInterval(() => {
                if(!gameActive) clearInterval(targetDirInterval);
                target.dir *= -1;
            }, 4500);

            timerInterval = setInterval(() => {
                timeLeft--;
                document.getElementById('time-disp').innerText = timeLeft;
                if(timeLeft <= 0) {
                    endGame();
                }
            }, 1000);

            gameInterval = requestAnimationFrame(update);
        }

        function endGame() {
            gameActive = false;
            cancelAnimationFrame(gameInterval);
            clearInterval(timerInterval);
            
            document.getElementById('final-score-disp').innerText = score;
            document.getElementById('final-combo-disp').innerText = maxCombo;
            const msgElement = document.getElementById('highscore-message');
            const titleElement = document.getElementById('result-title-text');

            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('high-disp').innerText = highScore;
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

        function backToMain() {
            document.getElementById('result-screen').classList.add('hidden');
            startGame(); 
        }

        function rollNextArrow() {
            currentArrow = {
                isApple: Math.random() < 0.06
            };
            appleTimer = 0;
            appleTrajectoryVisible = true;
        }
        rollNextArrow();

        function createExplosion(x, y, color) {
            let count = 15; 
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = 1 + Math.random() * 4;
                particles.push({
                    x: x,
                    y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: 2 + Math.random() * 3,
                    color: color,
                    alpha: 1,
                    decay: 0.02 + Math.random() * 0.02
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({
                x: x,
                y: y,
                text: text,
                color: color,
                alpha: 1,
                vy: -0.8
            });
        }

        function getMousePos(e) {
            return { x: e.clientX, y: e.clientY };
        }

        // 왼쪽 조준 활쏘기용 마우스 드래그 로직 (오른쪽으로 당겨서 왼쪽으로 쏨)
        window.addEventListener('mousedown', (e) => {
            if(!gameActive) return;
            const mousePos = getMousePos(e);

            if(Math.hypot(mousePos.x - bowPos.x, mousePos.y - bowPos.y) < 80) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mousePos.x, y: mousePos.y };
            }
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const mousePos = getMousePos(e);
            dragEnd = { x: mousePos.x, y: mousePos.y };
        });

        window.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;

            const dx = dragStart.x - dragEnd.x; // 당긴 거리 벡터
            const dy = dragStart.y - dragEnd.y;
            
            if (dx <= 0) return; // 오른쪽(과녁 방향)으로 발사하려면 dragEnd가 dragStart보다 왼쪽이어야 함 (dx > 0)

            const speedScale = 0.25; 
            const vx = dx * speedScale; 
            const vy = dy * speedScale;

            if(vx > 0) {
                activeArrows.push({
                    x: bowPos.x,
                    y: bowPos.y,
                    vx: vx,
                    vy: vy,
                    isApple: currentArrow.isApple,
                    width: 95, // [크기 업그레이드] 화살 길이 상향 (70 -> 95)
                    height: 5,
                    collided: false,
                    stuckTimer: 45, 
                    targetOffsetY: 0,
                    stuckAngle: 0,
                    handled: false 
                });
                rollNextArrow(); 
            }
        });

        let stars = [];
        function generateStars() {
            stars = [];
            let count = Math.floor((window.innerWidth * window.innerHeight) / 25000);
            for(let i=0; i<count; i++) {
                stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*1.6});
            }
        }
        generateStars();

        function update() {
            if (gameActive) {
                target.y += target.speed * target.dir;
                if(target.y - target.radiusD < 100 || target.y + target.radiusD > canvas.height - 40) {
                    target.dir *= -1; 
                }

                if(currentArrow.isApple) {
                    appleTimer++;
                    if(appleTimer % 45 === 0) {
                        appleTrajectoryVisible = !appleTrajectoryVisible;
                    }
                }
            }

            ctx.save();
            if (shakeIntensity > 0) {
                let dx = (Math.random() - 0.5) * shakeIntensity;
                let dy = (Math.random() - 0.5) * shakeIntensity;
                ctx.translate(dx, dy);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 우주 배경
            ctx.fillStyle = "rgba(255,255,255,0.35)";
            stars.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
                ctx.fill();
            });

            // [과녁 수정] 오른쪽에 위치하면서 왼쪽을 바라보는 얇은 타원형 과녁 디자인
            const targetColor = planets[currentPlanetKey].color;
            const skewX = 0.25; // 타원 찌그러짐 비율 (왼쪽을 비스듬히 바라봄)
            const frontX = target.x - (target.radiusD * skewX); // 과녁의 왼쪽 표면 가상 X축

            ctx.save();
            // 뒷면 지지대 프레임
            ctx.strokeStyle = "#4a5568";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(target.x + 5, target.y - target.radiusD);
            ctx.lineTo(target.x + 5, target.y + target.radiusD);
            ctx.stroke();

            // 바깥 링 그림자 효과
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); ctx.fill();

            // 과녁 레이어 렌더링 (D -> C -> B -> A)
            ctx.fillStyle = "#ffffff";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
            
            ctx.fillStyle = targetColor;
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2); ctx.fill();
            
            ctx.fillStyle = "#ff3e3e";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
            
            ctx.fillStyle = "#ffcc00";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
            ctx.restore();

            // [활 크기 업그레이드] 활 그리기 (왼쪽 배치, 반경 35 -> 48 확대)
            ctx.save();
            ctx.strokeStyle = "#00d2ff";
            ctx.lineWidth = 5; // 두께 상향
            ctx.beginPath();
            ctx.arc(bowPos.x - 12, bowPos.y, 48, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(bowPos.x - 12, bowPos.y - 48);
            if(isDragging) ctx.lineTo(dragEnd.x, dragEnd.y);
            else ctx.lineTo(bowPos.x - 12, bowPos.y);
            ctx.lineTo(bowPos.x - 12, bowPos.y + 48);
            ctx.stroke();
            ctx.restore();

            if(!isDragging && gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 왼쪽 -> 오른쪽 궤적 포물선 가이드
            if (isDragging && appleTrajectoryVisible && gameActive) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.5)";
                    ctx.lineWidth = 2.5;
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();

                    let tX = bowPos.x;
                    let tY = bowPos.y;
                    let tVy = (dragStart.y - dragEnd.y) * 0.25;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx;
                        tY += tVy;
                        tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke();
                    ctx.restore();

                    let angle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
                    drawArrowIcon(dragEnd.x, dragEnd.y, angle, currentArrow.isApple);
                }
            }

            // 화살 물리 루프
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                if (!arrow.collided) {
                    arrow.x += arrow.vx;
                    arrow.y += arrow.vy;
                    arrow.vy += currentGravity;
                } else {
                    arrow.y = target.y + arrow.targetOffsetY;
                    arrow.stuckTimer--;
                }

                let arrowAngle = arrow.collided ? arrow.stuckAngle : Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                // 빗나감 처리
                if (!arrow.collided && (arrow.x > canvas.width + 50 || arrow.y > canvas.height + 50 || arrow.y < -50)) {
                    if(!arrow.handled) {
                        combo = 0; 
                        document.getElementById('combo-wrapper').classList.add('hidden');
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                if (arrow.collided && arrow.stuckTimer <= 0) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 타원형 과녁 정면 충돌 판정 (오른쪽 과녁 기준)
                if (!arrow.collided) {
                    let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                    let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);
                    
                    if (arrowTipX >= frontX && arrowTipX <= target.x + 10 && arrow.vx > 0) {
                        let dy = Math.abs(arrowTipY - target.y);

                        if (dy <= target.radiusD) {
                            arrow.collided = true;
                            arrow.handled = true;
                            arrow.stuckTimer = 45; 
                            arrow.targetOffsetY = arrow.y - target.y; 
                            arrow.stuckAngle = arrowAngle; 

                            combo++;
                            if(combo > maxCombo) maxCombo = combo;
                            
                            const comboContainer = document.getElementById('combo-wrapper');
                            const comboTxt = document.getElementById('combo-disp');
                            comboTxt.innerText = `${combo} COMBO`;
                            comboContainer.classList.remove('hidden');

                            let earnedPoints = 0;
                            let hColor = "#ffffff";
                            if (dy <= target.radiusA) {
                                earnedPoints = 10; hColor = "#ffcc00";
                            } else if (dy <= target.radiusB) {
                                earnedPoints = 5;  hColor = "#ff3e3e";
                            } else if (dy <= target.radiusC) {
                                earnedPoints = 2;  hColor = targetColor;
                            } else {
                                earnedPoints = 1;  hColor = "#e2e8f0";
                            }

                            if(arrow.isApple) {
                                earnedPoints *= 2;
                                hColor = "#ff2222";
                            }

                            let totalEarned = earnedPoints + Math.floor(combo / 3);
                            score += totalEarned;
                            document.getElementById('score-disp').innerText = score;

                            createScoreText(arrowTipX - 25, arrowTipY - 15, `+${totalEarned}`, hColor);
                            shakeIntensity = 6; 
                            createExplosion(arrowTipX, arrowTipY, hColor);
                        }
                    }
                }
            }

            // 파티클 렌더링
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= p.decay;
                
                if (p.alpha <= 0) {
                    particles.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.globalAlpha = p.alpha;
                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2);
                ctx.fill();
                ctx.restore();
            }

            // 둥둥 텍스트 렌더링
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy;
                stx.alpha -= 0.015;

                if(stx.alpha <= 0) {
                    scoreTexts.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.globalAlpha = stx.alpha;
                ctx.fillStyle = stx.color;
                ctx.font = "bold 26px 'Segoe UI'";
                ctx.shadowColor = "rgba(0,0,0,0.5)";
                ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y);
                ctx.restore();
            }

            ctx.restore(); 
            gameInterval = requestAnimationFrame(update);
        }

        // [화살 크기 업그레이드] 두께 및 촉 크기 비율 확대 적용 함수
        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);

            let width = customWidth || 95; // 기본 화살 길이 상향
            
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 5.5 : 4.5; // 화살대 두께 확대
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(width/2, 0);
            ctx.stroke();

            // 삼각형 촉 크기 상향
            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath();
            ctx.moveTo(width/2, 0);
            ctx.lineTo(width/2 - 15, -8);
            ctx.lineTo(width/2 - 15, 8);
            ctx.closePath();
            ctx.fill();

            // 깃털 꼬리 크기 상향
            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(-width/2 - 8, -10);
            ctx.lineTo(-width/2 + 5, -10);
            ctx.lineTo(-width/2 + 12, 0);
            ctx.lineTo(-width/2 + 5, 10);
            ctx.lineTo(-width/2 - 8, 10);
            ctx.closePath();
            ctx.fill();

            if(isApple) {
                ctx.fillStyle = "#fa5252"; 
                ctx.beginPath();
                ctx.arc(0, -4, 11, 0, Math.PI*2);
                ctx.fill();
                ctx.strokeStyle = "#868e96";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, -14);
                ctx.quadraticCurveTo(3, -19, 6, -17);
                ctx.stroke();
            }

            ctx.restore();
        }

        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
