import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정 (화면을 넓게 쓰고 스크롤을 막기 위해 padding 최소화)
st.set_page_config(page_title="Gravity Arrow", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding: 0; }
    iframe { display: block; width: 100vw; height: 95vh; border: none; }
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
        /* 컴퓨터 화면에 맞춘 반응형 Cosmic 레이아웃 */
        body {
            margin: 0;
            padding: 0;
            background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }

        /* 16:9 비율을 유지하면서 컴퓨터 화면에 꽉 차게 조절 */
        #game-wrapper {
            position: relative;
            width: 90vw;
            max-width: 1200px;
            height: calc(90vw * 9 / 16);
            max-height: 675px;
            display: flex;
            flex-direction: column;
        }

        #game-container {
            position: relative;
            flex: 1;
            width: 100%;
            height: 100%;
        }

        #game-canvas {
            width: 100%;
            height: 100%;
            border: 2px solid #4a5568;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 150, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4);
            cursor: crosshair;
        }

        /* 화면 분리를 위한 섹션 정의 */
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
            background: rgba(9, 10, 15, 0.85);
            border-radius: 10px;
            z-index: 10;
        }

        .hidden {
            display: none !important;
        }

        h1 {
            font-size: 3.5rem;
            margin: 10px 0;
            text-shadow: 0 0 15px #00d2ff;
            font-weight: 800;
            letter-spacing: 3px;
        }

        .result-title {
            font-size: 3rem;
            color: #ffcc00;
            text-shadow: 0 0 10px #ffcc00;
            margin-bottom: 20px;
        }

        .score-report {
            font-size: 1.8rem;
            margin-bottom: 30px;
            font-weight: bold;
        }

        .ui-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 8px;
            box-sizing: border-box;
            margin-bottom: 10px;
            backdrop-filter: blur(5px);
        }

        .stats {
            font-size: 1.2rem;
            font-weight: bold;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 12px 28px;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 132, 255, 0.6);
        }

        .planet-selector {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .planet-circle {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000;
        }

        .planet-circle:hover {
            transform: scale(1.1);
        }

        .planet-circle.active {
            border-color: #fff;
            box-shadow: 0 0 15px currentColor;
        }

        #planet-earth { background: radial-gradient(circle at 30% 30%, #2b82c9, #053057); color: #00d2ff; }
        #planet-moon { background: radial-gradient(circle at 30% 30%, #ccc, #666); color: #ddd; }
        #planet-mars { background: radial-gradient(circle at 30% 30%, #e03e1d, #5c1303); color: #ff6b6b; }
        #planet-venus { background: radial-gradient(circle at 30% 30%, #e3a857, #6d3e00); color: #ffd166; }
        #planet-europa { background: radial-gradient(circle at 30% 30%, #a5cad6, #3a5d6b); color: #98e1f5; }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div id="start-screen" class="screen-overlay">
            <h1>Gravity Arrow</h1>
            <p style="font-size: 1.1rem; color: #a0aec0; margin-bottom: 30px;">행성을 선택하고 활을 당겨 과녁을 맞추세요!</p>
            <button class="btn" onclick="startGame()">Start Game</button>
        </div>

        <div id="result-screen" class="screen-overlay hidden">
            <div class="result-title" id="result-title-text">GAME OVER</div>
            <div class="score-report">
                최종 점수: <span id="final-score-disp" style="color: #00d2ff;">0</span> 점<br>
                <span id="highscore-message" style="font-size: 1.2rem; color: #4cdf50;"></span>
            </div>
            <button class="btn" onclick="backToMain()">메인으로 돌아가기</button>
        </div>

        <div id="game-ui" style="display: flex; flex-direction: column; width:100%; height:100%;">
            <div class="ui-panel">
                <div class="stats">
                    시간: <span id="time-disp">15</span>s | 
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

            <div id="game-container">
                <canvas id="game-canvas" width="800" height="450"></canvas>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');

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
        let timeLeft = 15;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        let gravityScale = 0.03; 
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 과녁 변수
        let target = {
            x: 720,
            y: 225,
            radiusD: 50, 
            radiusC: 35, 
            radiusB: 20, 
            radiusA: 8,  
            speed: 1.5,
            dir: 1
        };
        
        // 활 및 화살 변수
        const bowPos = { x: 80, y: 225 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };
        
        let activeArrows = [];
        let currentArrow = { isApple: false };
        
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        document.getElementById('high-disp').innerText = highScore;

        function selectPlanet(key) {
            if (gameActive) return; // 게임 중에는 행성 변경 불가
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
            timeLeft = 15;
            gameActive = true;
            activeArrows = [];
            rollNextArrow();

            // UI 제어 (시작화면 숨기기, 행성 선택 비활성화 비주얼)
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('planet-selector-bar').style.pointerEvents = "none";
            document.getElementById('planet-selector-bar').style.opacity = "0.5";

            document.getElementById('score-disp').innerText = score;
            document.getElementById('time-disp').innerText = timeLeft;

            let targetDirInterval = setInterval(() => {
                if(!gameActive) clearInterval(targetDirInterval);
                target.dir *= -1;
            }, 5000);

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

            // 결과 화면 표시
            document.getElementById('result-screen').classList.remove('hidden');
        }

        function backToMain() {
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('hidden');
            document.getElementById('planet-selector-bar').style.pointerEvents = "auto";
            document.getElementById('planet-selector-bar').style.opacity = "1";
            
            // 캔버스 초기화용 그리기
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            generateStars();
        }

        function rollNextArrow() {
            currentArrow = {
                isApple: Math.random() < 0.05
            };
            appleTimer = 0;
            appleTrajectoryVisible = true;
        }

        // 마우스 및 터치 좌표 캔버스 스케일 변환 함수 (반응형 대응 크기 보정)
        function getMousePos(e) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: (e.clientX - rect.left) * (canvas.width / rect.width),
                y: (e.clientY - rect.top) * (canvas.height / rect.height)
            };
        }

        canvas.addEventListener('mousedown', (e) => {
            if(!gameActive) return;
            const mousePos = getMousePos(e);

            if(Math.hypot(mousePos.x - bowPos.x, mousePos.y - bowPos.y) < 60) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mousePos.x, y: mousePos.y };
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const mousePos = getMousePos(e);
            dragEnd = { x: mousePos.x, y: mousePos.y };
        });

        canvas.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;

            const dx = dragStart.x - dragEnd.x;
            const dy = dragStart.y - dragEnd.y;
            
            if (dx <= 0) return; // 화살은 앞으로만 나가야함

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
                    width: canvas.width / 16,
                    height: 4,
                    collided: false,
                    stuckTimer: 0, 
                    targetOffsetY: 0,
                    stuckAngle: 0
                });
                rollNextArrow(); 
            }
        });

        let stars = [];
        function generateStars() {
            stars = [];
            for(let i=0; i<40; i++) {
                stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*1.5});
            }
        }
        generateStars();

        function update() {
            if(!gameActive) return;

            // 1. 물리 연산 - 과녁 이동
            target.y += target.speed * target.dir;
            if(target.y - target.radiusD < 0 || target.y + target.radiusD > canvas.height) {
                target.dir *= -1; 
            }

            if(currentArrow.isApple) {
                appleTimer++;
                if(appleTimer % 60 === 0) {
                    appleTrajectoryVisible = !appleTrajectoryVisible;
                }
            }

            // 2. 그리기 작업
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "rgba(255,255,255,0.3)";
            stars.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
                ctx.fill();
            });

            // 과녁 그리기 (왼쪽 시점 찌그러진 타원형태)
            const targetColor = planets[currentPlanetKey].color;
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.strokeStyle = targetColor;
            ctx.lineWidth = 2;
            
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * 0.2, target.radiusD, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "rgba(255,255,255,0.15)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * 0.2, target.radiusC, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "rgba(255,255,255,0.25)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * 0.2, target.radiusB, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "#ff007f";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * 0.2, target.radiusA, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();

            // 과녁 스탠드 지지대
            ctx.strokeStyle = "#4a5568";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(target.x + 5, target.y - target.radiusD);
            ctx.lineTo(target.x + 5, target.y + target.radiusD);
            ctx.stroke();

            // 활 그리기
            ctx.strokeStyle = "#00d2ff";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(bowPos.x - 10, bowPos.y, 35, -Math.PI/2, Math.PI/2);
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(bowPos.x - 10, bowPos.y - 35);
            if(isDragging) ctx.lineTo(dragEnd.x, dragEnd.y);
            else ctx.lineTo(bowPos.x - 10, bowPos.y);
            ctx.lineTo(bowPos.x - 10, bowPos.y + 35);
            ctx.stroke();

            if(!isDragging) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 조준 포물선 연산 (앞방향 추진 제한)
            if (isDragging && appleTrajectoryVisible) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.6)";
                    ctx.lineWidth = 2;
                    ctx.setLineDash([4, 4]);
                    ctx.beginPath();

                    let tX = bowPos.x;
                    let tY = bowPos.y;
                    let tVy = (dragStart.y - dragEnd.y) * 0.25;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 40; i++) {
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

            // 3. 날아가는 화살들 및 박힌 화살 제어
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

                if (!arrow.collided && (arrow.x > canvas.width + 100 || arrow.y > canvas.height + 100 || arrow.x < -100)) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 박힌 지 0.5초(30프레임) 지나면 소멸
                if (arrow.collided && arrow.stuckTimer <= 0) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 타원 판정 기반 가상 세로선 충돌 로직
                if (!arrow.collided) {
                    let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                    let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);
                    
                    let targetFrontX = target.x - (target.radiusD * 0.2);
                    
                    if (arrowTipX >= targetFrontX && arrowTipX <= target.x + 10 && arrow.vx > 0) {
                        let dy = Math.abs(arrowTipY - target.y);

                        if (dy <= target.radiusD) {
                            arrow.collided = true;
                            arrow.stuckTimer = 30; 
                            arrow.targetOffsetY = arrow.y - target.y; 
                            arrow.stuckAngle = arrowAngle; 

                            let earnedPoints = 0;
                            if (dy <= target.radiusA) {
                                earnedPoints = 10;
                            } else if (dy <= target.radiusB) {
                                earnedPoints = 5;
                            } else if (dy <= target.radiusC) {
                                earnedPoints = 2;
                            } else {
                                earnedPoints = 1;
                            }

                            if(arrow.isApple) {
                                earnedPoints *= 2;
                            }

                            score += earnedPoints;
                            document.getElementById('score-disp').innerText = score;
                        }
                    }
                }
            }

            gameInterval = requestAnimationFrame(update);
        }

        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);

            let width = customWidth || (canvas.width / 16);
            
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 4 : 3;
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(width/2, 0);
            ctx.stroke();

            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath();
            ctx.moveTo(width/2, 0);
            ctx.lineTo(width/2 - 10, -6);
            ctx.lineTo(width/2 - 10, 6);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(-width/2 - 6, -8);
            ctx.lineTo(-width/2 + 4, -8);
            ctx.lineTo(-width/2 + 10, 0);
            ctx.lineTo(-width/2 + 4, 8);
            ctx.lineTo(-width/2 - 6, 8);
            ctx.closePath();
            ctx.fill();

            if(isApple) {
                ctx.fillStyle = "#fa5252"; 
                ctx.beginPath();
                ctx.arc(0, -2, 8, 0, Math.PI*2);
                ctx.fill();
                ctx.strokeStyle = "#868e96";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, -10);
                ctx.quadraticCurveTo(3, -14, 5, -13);
                ctx.stroke();
            }

            ctx.restore();
        }
    </script>
</body>
</html>
"""

# 전체 모니터 반응형 크기를 극대화하기 위해 iframe 출력 크기 조절
components.html(game_html, height=730, scrolling=False)
