import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정
st.set_page_config(page_title="Gravity Arrow", layout="wide")

# 게임 HTML/CSS/JavaScript 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        /* 우주적인 디자인 컨셉 (Cosmic Theme) */
        body {
            margin: 0;
            padding: 0;
            background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow: hidden;
            user-select: none;
        }

        #game-container {
            position: relative;
            width: 800px;
            margin-top: 10px;
        }

        #game-canvas {
            border: 2px solid #4a5568;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 150, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4);
            cursor: crosshair;
        }

        .header {
            text-align: center;
            margin-bottom: 5px;
        }

        h1 {
            font-size: 2.5rem;
            margin: 5px 0;
            text-shadow: 0 0 10px #00d2ff;
            font-weight: 800;
            letter-spacing: 2px;
        }

        .ui-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 800px;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 8px;
            box-sizing: border-box;
            margin-bottom: 10px;
            backdrop-filter: blur(5px);
        }

        .stats {
            font-size: 1.1rem;
            font-weight: bold;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 8px 16px;
            font-size: 1rem;
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

        .btn:active {
            transform: translateY(1px);
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

    <div class="header">
        <h1>Gravity Arrow</h1>
        <button class="btn" id="start-btn" onclick="startGame()">Start Game</button>
    </div>

    <div class="ui-panel">
        <div class="stats">
            시간: <span id="time-disp">15</span>s | 
            중력: <span id="gravity-disp">9.8</span> $m/s^2$ | 
            점수: <span id="score-disp">0</span> | 
            최고기록: <span id="high-disp">0</span>
        </div>
        
        <div class="planet-selector">
            <button class="btn" onclick="cyclePlanet()">Change</button>
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

        // 게임 변수
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
            radiusD: 50, // 1점
            radiusC: 35, // 2점
            radiusB: 20, // 5점
            radiusA: 8,  // 10점
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
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`planet-${k}`).classList.remove('active');
            });
            document.getElementById(`planet-${key}`).classList.add('active');
            
            document.getElementById('gravity-disp').innerText = planets[key].gravity.toFixed(1);
            currentGravity = planets[key].gravity * gravityScale;
            
            generateStars(); 
        }

        function cyclePlanet() {
            let idx = planetKeys.indexOf(currentPlanetKey);
            idx = (idx + 1) % planetKeys.length;
            selectPlanet(planetKeys[idx]);
        }

        function startGame() {
            if(gameActive) return;
            score = 0;
            timeLeft = 15;
            gameActive = true;
            activeArrows = [];
            rollNextArrow();

            document.getElementById('score-disp').innerText = score;
            document.getElementById('time-disp').innerText = timeLeft;
            document.getElementById('start-btn').innerText = "게임 진행 중";
            document.getElementById('start-btn').disabled = true;

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
            
            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('high-disp').innerText = highScore;
                alert(`축하합니다! 최고기록 달성: ${score}점`);
            } else {
                alert(`게임 종료! 최종 점수: ${score}점`);
            }

            document.getElementById('start-btn').innerText = "Start Game";
            document.getElementById('start-btn').disabled = false;
        }

        function rollNextArrow() {
            currentArrow = {
                isApple: Math.random() < 0.05
            };
            appleTimer = 0;
            appleTrajectoryVisible = true;
        }

        canvas.addEventListener('mousedown', (e) => {
            if(!gameActive) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            if(Math.hypot(mouseX - bowPos.x, mouseY - bowPos.y) < 60) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mouseX, y: mouseY };
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            dragEnd = { x: e.clientX - rect.left, y: e.clientY - rect.top };
        });

        canvas.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;

            const dx = dragStart.x - dragEnd.x;
            const dy = dragStart.y - dragEnd.y;
            
            // 화살은 앞으로만 나가야함 (dx가 0 이하이면 무시)
            if (dx <= 0) return;

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
                    stuckTimer: 0, // 박힌 화살의 타이머 (0.5초 = 30프레임)
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

            // 과녁 그리기 (왼쪽을 바라보는 형태로 타원 사용)
            const targetColor = planets[currentPlanetKey].color;
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.strokeStyle = targetColor;
            ctx.lineWidth = 2;
            
            // ellipse: x, y, radiusX (얇게), radiusY (길게), rotation, startAngle, endAngle
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * 0.2, target.radiusD, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "rgba(255,255,255,0.15)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * 0.2, target.radiusC, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "rgba(255,255,255,0.25)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * 0.2, target.radiusB, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = "#ff007f";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * 0.2, target.radiusA, 0, 0, Math.PI*2); ctx.fill(); ctx.stroke();

            // 과녁 지지대 (선택적)
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

            // 조준선 앞으로만 그려지도록 제어
            if (isDragging && appleTrajectoryVisible) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { // 앞으로 당길 때만 조준선 표시
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

            // 3. 날아가는 화살들 및 과녁에 박힌 화살 처리
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                if (!arrow.collided) {
                    arrow.x += arrow.vx;
                    arrow.y += arrow.vy;
                    arrow.vy += currentGravity;
                } else {
                    // 과녁에 박혔을 때 과녁과 함께 이동
                    arrow.y = target.y + arrow.targetOffsetY;
                    arrow.stuckTimer--;
                }

                let arrowAngle = arrow.collided ? arrow.stuckAngle : Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                // 화면 이탈 검사
                if (!arrow.collided && (arrow.x > canvas.width + 100 || arrow.y > canvas.height + 100 || arrow.x < -100)) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 박힌 지 0.5초(30프레임) 지나면 사라짐
                if (arrow.collided && arrow.stuckTimer <= 0) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 충돌 판정 (과녁이 왼쪽을 바라보는 타원형태에 맞춤)
                if (!arrow.collided) {
                    let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                    let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);
                    
                    let targetFrontX = target.x - (target.radiusD * 0.2);
                    
                    // 화살촉이 과녁 정면을 통과했고 y축 기준 반경 안에 있는지 검사
                    if (arrowTipX >= targetFrontX && arrowTipX <= target.x + 10 && arrow.vx > 0) {
                        let dy = Math.abs(arrowTipY - target.y);

                        if (dy <= target.radiusD) {
                            arrow.collided = true;
                            arrow.stuckTimer = 30; // 60fps 기준 약 0.5초
                            arrow.targetOffsetY = arrow.y - target.y; // 박힌 Y 위치 고정
                            arrow.stuckAngle = arrowAngle; // 박힌 각도 고정

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

# 스트림릿 컴포넌트로 HTML 주입 (크기 조절)
components.html(game_html, height=620, width=850, scrolling=False)
